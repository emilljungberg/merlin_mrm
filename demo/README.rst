Shepp Logan MOCO Demo
=======================

This is a simple demo to demonstrate the pymerlin motion correction framework using simulated data. Requires pymerlin and riesling to be installed and in your path. The performance of this demo is not optimal, partly due to the symetric shape of the Shepp Logan phantom, it is purely meant to give a demo for how to use the tools and how to adapt your own data to be used with pymerlin. Note that this example does not use the automatically extracted brain mask since HD-BET used for that in the in vivo examples is optimised for brain data and not a Shepp Logan phantom.

To run the demo, simply execute the shell script and grab a cup of coffee, it takes a while (especially the navigator reconstruction). I recommend that you look through this script to see what is happening behind the scnes.

.. code:: shell

    $ bash run_demo.sh

The script will run the same pipeline as for in vivo experiment. The results are saved in the folder ``moving_phantom_mocodir`` which contains the motion corrected k-space data, as well as the separate interleaves and navigators. The motion corrected reconstructed image is ``moving_phantom_moco-cg.h5`` which can be viewed with the ``h5viewer`` tool included in ``pymerlin``. Alternatively you can convert it to Nifti using ``h52nii`` (also included in ``pymerlin``).

The script will also produce several outputs for studying the motion correction results

- ``moco_diff_plot.png``: Difference image of the uncorrected and corrected image
- ``reg_animation.png``: Timeseries animation of the navigator images and estimated motion. (Same as used for supplemental videos for paper)
