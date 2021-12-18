Motion Corrected Silent ZTE Neuroimaging
=======================================================
Code to accompany paper on MERLIN recently submitted.

- `notebooks/Phyllotaxis_Figures.ipynb <https://github.com/emilljungberg/merlin_mrm/blob/main/notebooks/Phyllotaxis_Figures.ipynb>`_ reproduces Figure 1, and SI Figures 1 and 2.
- `notebooks/NoiseTrajectory.ipynb <https://github.com/emilljungberg/merlin_mrm/blob/main/notebooks/NoiseTrajectory.ipynb>`_ reproduces Figure 4.
- Due to privacy reasons we are not able to share a full in vivo dataset for demonstrating the MERLIN workflow. As a substitute, we provide a demo using a simulated Shepp Logan phantom with motion which uses the same motion correction framework as the in vivo data. See the ``demo`` folder.

Dependencies
--------------------

1. `pymerlin <https://github.com/emilljungberg/pyMERLIN>`_ 
2. `riesling <https://github.com/spinicist/riesling>`_

Python packages required

- ``h5py``
- ``numpy``
- ``matplotlib``
- ``scipy``
