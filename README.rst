Motion Corrected Silent Neuroimaging with MERLIN
=======================================================
Code to accompany paper on MERLIN recently submitted.

- ``notebooks/Phyllotaxis_Figures.ipynb`` reproduces Figure 1, and SI Figures 1 and 2.
- ``notebooks/NoiseTrajectory.ipynd`` reproduces Figure 4.
- Due to privacy reasons we are not able to share a full in vivo dataset for demonstrating the MERLIN workflow. As a substitute, we provide a demo using a simulated Shepp Logan phantom with motion which uses the same motion correction framework as the in vivo data. See the ``demo`` folder.

Dependencies
--------------------

1. `pymerlin <https://github.com/emilljungberg/pyMERLIN>`_ 
2. `riesling <https://github.com/spinicist/riesling>`_ (Tested with version X)

Python packages required

- ``h5py``
- ``numpy``
- ``matplotlib``
- ``scipy``
