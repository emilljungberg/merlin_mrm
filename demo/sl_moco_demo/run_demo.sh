#!/bin/bash

# 1. Create a new riesling file with the desired trajectory to use as a template
function make_traj() {
    if [ -e trajectory.h5 ]; then
        rm -I trajectory.h5
    fi
    python3 make_trajectory_h5.py
}
# make_traj

# 2. Create phantom k-space data based on the generated trajectory
# riesling phantom --traj trajectory.h5 --info trajectory.h5 --shepp_logan -v static_phantom.h5

# 3. Now we apply motion to the phantom in k-space
function apply_motion() {
    if [ -e "moving_phantom.h5" ]; then
        rm -I moving_phantom.h5
    fi
    python3 apply_motion.py
}
# apply_motion

# 4. Now we run motion correction
function run_moco() {
    nspokes=2000
    cgit=8
    fov=230
    ds=3
    step=1000
    options="--nspokes $nspokes --its $cgit --step $step --fov $fov --ds $ds"
    options="${options} --batchitk 10 --batchries 10  --threaditk 2 --threadries 2"

    run_merlin_sw -i $1.h5 ${options} --out ${1}_mocodir -v
}
# run_moco moving_phantom

# 5. Reconstruct data with and without motion correction
riesling cg --mag --fast-grid -i 4 --kb --os=1.3 --sdc=pipe static_phantom.h5 -v
riesling cg --mag --fast-grid -i 4 --kb --os=1.3 --sdc=pipe moving_phantom.h5 -v
riesling cg --mag --fast-grid -i 4 --kb --os=1.3 --sdc=pipe moving_phantom_mocodir/moving_phantom_moco.h5 -v

# 6. Show results
python3 difference_plot.py
pymerlin report --reg moving_phantom_mocodir/all_reg_param.p
pymerlin animation --reg moving_phantom_mocodir/all_reg_param.p --nav moving_phantom_mocodir/navigators --out reg_animation.gif
