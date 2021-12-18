#!/bin/bash

# 1. Create phantom k-space data based on the generated trajectory
NEX=4.21875
riesling phantom --phyllo --shepp_logan --lores=8 -v --spi=3 --smoothness=10 --sps=384 --nex=$NEX static_phantom.h5

# 2. Apply motion to the phantom in k-space
function apply_motion() {
    if [ -e "moving_phantom.h5" ]; then
        rm -I moving_phantom.h5
    fi
    python3 apply_motion.py
}
apply_motion

# 3. Now we run motion correction
function run_moco() {
    parfile=par_file.txt

    nspokes=1152
    nlores=1152
    cgit=8
    fov=230
    ds=3
    step=1152
    options="--nspokes $nspokes --nlores $nlores --spoke_step $step --cg_its $cgit --fov $fov --ds $ds"
    options="${options} --batch_itk 8 --batch_riesling 8  --threads_itk 2 --threads_riesling 2"

    pymerlin param $parfile $options
    run_merlin_sw -i $1.h5 -o ${1}_mocodir -p $parfile -v
}
run_moco moving_phantom

# 4. Reconstruct data with and without motion correction
function recon() {
    riesling cg --mag -i 4 --kernel=KB3 --sdc=pipenn -v -o $2 $1
}
recon static_phantom.h5 static_phantom
recon moving_phantom.h5 moving_phantom
recon moving_phantom_mocodir/moving_phantom_moco.h5 moving_phantom_moco

# 5. Show results
python3 difference_plot.py
pymerlin report --reg moving_phantom_mocodir/all_reg_param.p
pymerlin animation --reg moving_phantom_mocodir/all_reg_param.p --nav moving_phantom_mocodir/navigators --out reg_animation.gif
