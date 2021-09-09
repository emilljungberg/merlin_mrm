import h5py
import numpy as np
from pymerlin.utils import rotmat
from pymerlin.moco import calc_H


def rot_traj(traj, i0, i1, rotang):
    R = rotmat(np.deg2rad(rotang))
    traj[i0:i1, :, :] = np.matmul(traj[i0:i1, :, :], R)

    return traj


def phase_kspace(data, traj, i0, i1, delta, spacing, ncoils):
    H = calc_H(traj[i0:i1, :, :], {'dx': delta[0],
               'dy': delta[1], 'dz': delta[2]}, spacing)

    for ircv in range(ncoils):
        data[0, i0:i1, :, ircv] = data[0, i0:i1, :, ircv] * H

    return data


def main():
    print("Reading static_phantom.h5")
    ref_h5 = h5py.File('static_phantom.h5', 'r')
    ref_data = ref_h5['noncartesian'][:]
    ref_traj = ref_h5['trajectory'][:]

    print("Opening moving_phantom.h5")
    move_h5 = h5py.File('moving_phantom.h5', 'w')
    ref_h5.copy('info', move_h5)
    ref_h5.close()

    move_trajp = np.copy(ref_traj)
    move_data = np.copy(ref_data)

    # Apply translation motion as phase ramp in k-space
    print("Applying translational motion")
    move_data = phase_kspace(move_data, move_trajp, 12000, 18000, [
        0, -10, 0],  [1, 1, 1], move_h5['info']['channels'][0])
    move_data = phase_kspace(move_data, move_trajp, 22000, 28000, [10, 0, 0],  [
        1, 1, 1], move_h5['info']['channels'][0])

    # Apply rotation to trajectory
    print("Applying rotation")
    move_trajp = rot_traj(move_trajp, 42000, 48000, [0, -10, 0])
    move_trajp = rot_traj(move_trajp, 52000, 58000, [0, 0, 10])

    # Save data
    print("Saving data to moving_phantom.h5")
    traj_chunk_dims = list(move_trajp.shape)
    if traj_chunk_dims[0] > 1024:
        traj_chunk_dims[0] = 1024

    move_h5.create_dataset("trajectory", data=move_trajp,
                           chunks=tuple(traj_chunk_dims), compression='gzip')

    data_chunk_dims = list(move_data.shape)
    if data_chunk_dims[1] > 1024:
        data_chunk_dims[1] = 1024

    move_h5.create_dataset("noncartesian", dtype='c8', data=move_data,
                           chunks=tuple(data_chunk_dims), compression='gzip')

    move_h5.close()
    print("Done")


if __name__ == "__main__":
    main()
