
import h5py
import numpy as np
from pymerlin.trajectory import linear_phyllotaxis, wong_roos_traj


def create_info(matrix, voxel_size, read_points, read_gap, spokes_hi, spokes_lo, lo_scale,
                channels, volumes, tr, origin, direction):
    D = np.dtype({'names': [
        'matrix', 'voxel_size', 'read_points', 'read_gap',
        'spokes_hi', 'spokes_lo', 'lo_scale', 'channels',
        'volumes', 'tr', 'origin', 'direction', 'type'],
        'formats': [
        ('<i8', (3,)), ('<f4', (3,)), '<i8', '<i8', '<i8',
        '<i8', '<f4', '<i8', '<i8', '<f4', ('<f4', (3,)), ('<f4', (9,)), '<i8']
    })

    info = np.array([(matrix, voxel_size, read_points, read_gap, spokes_hi, spokes_lo, lo_scale,
                      channels, volumes, tr, origin, direction, 1)], dtype=D)

    return info


def main():
    print("Creating a new riesling file")
    # Creating a new riesling file
    spokes_hi = 64000
    spokes_lo = 2000
    nint = 32
    lo_scale = 8
    matrix = [192, 192, 192]
    voxel_size = [1.0, 1.0, 1.0]
    read_points = 192
    channels = 8
    direction = [1, 0, 0, 0, 1, 0, 0, 0, 1]
    read_gap = 0
    tr = 0
    origin = [0, 0, 0]
    volumes = 1
    smooth_factor = 10
    info = create_info(matrix, voxel_size, read_points, read_gap,
                       spokes_hi, spokes_lo, lo_scale, channels, volumes, tr, origin, direction)

    traj = linear_phyllotaxis(spokes_hi, nint, smooth_factor)
    traj_p = traj2points(traj, read_points, OS=2)
    traj_p /= np.max(np.abs(traj_p[:]))

    traj_low = wong_roos_traj(spokes_lo)
    traj_low_p = traj2points(traj_low, read_points, OS=2)
    traj_low_p /= np.max(np.abs(traj_low_p[:]))

    combined_trajectory = np.zeros((spokes_lo + spokes_hi, read_points, 3))
    combined_trajectory[0:spokes_lo, ...] = traj_low_p
    combined_trajectory[spokes_lo:, ...] = traj_p

    fname = "trajectory.h5"
    my_h5 = h5py.File(fname, 'w')

    my_h5.create_dataset("info", data=info)

    traj_chunk_dims = list(combined_trajectory.shape)
    if traj_chunk_dims[0] > 1024:
        traj_chunk_dims[0] = 1024

    my_h5.create_dataset("trajectory", data=combined_trajectory, chunks=tuple(
        traj_chunk_dims), compression='gzip')
    my_h5.close()

    print("Data saved to {}".format(fname))


if __name__ == "__main__":
    main()
