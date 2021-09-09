Shepp Logan MOCO Demo
=======================

This is a simple demo to demonstrate the pymerlin motion correction framework using simulated data. Requires pymerlin and riesling to be installed and in your path. The performance of this demo is not optimal, partly due to the symetric shape of the Shepp Logan phantom, it is purely meant to give a demo for how to use the tools and how to adapt your own data to be used with pymerlin. Note that this example does not use the automatically extracted brain mask since HD-BET used for that in the in vivo examples is optimised for brain data and not a Shepp Logan phantom.

To run the demo, simply execute the shell script and grab a cup of coffee, it takes a while (especially the navigator reconstruction)

.. code:: shell

    $ bash run_demo.sh

The script will also produce several outputs for studying the effects of the motion correction, similar to in the paper.