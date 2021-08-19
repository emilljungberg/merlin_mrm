import numpy as np
import matplotlib.pyplot as plt
from pymerlin.recon import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import SphericalVoronoi, geometric_slerp
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import colors
import scipy
from matplotlib import cm


def fibonacci(k):
    """
    Calculates the kth Fibonacci number
    """

    if k == 0:
        return 0
    elif k == 1 or k == 2:
        return 1
    else:
        return fibonacci(k-1)+fibonacci(k-2)


def voronoi_area(traj, aref=None, vmin=None, vmax=None):
    nspokes, _ = traj.shape
    radius = 1
    center = np.array([0, 0, 0])
    sv = SphericalVoronoi(traj, radius, center)

    if not aref:
        Asphere = 4*np.pi
        aref = Asphere/nspokes

    areas = sv.calculate_areas()
    Amax = max(areas)
    areas /= aref

    if vmax:
        areas[areas > vmax] = vmax
    if vmin:
        areas[areas < vmin] = vmin

    return sv, areas


def voronoi_3D(traj, ax=None, aref=None, cmap='RdBu_r', vmin=0.7, vmax=1.3, title=''):
    """
    Make a 3D voronoi diagram with patch color based on path area
    relative to area for perfectly even sampled
    """

    sv, areas = voronoi_area(traj, aref=aref, vmin=vmin, vmax=vmax)
    m = cm.ScalarMappable(cmap=cm.get_cmap(
        cmap), norm=plt.Normalize(vmin=vmin, vmax=vmax))

    sv.sort_vertices_of_regions()
    if not ax:
        ax = plt.gca()

    fig = plt.gcf()
    for n in range(0, len(sv.regions)):
        region = sv.regions[n]
        random_color = colors.rgb2hex(scipy.rand(3))
        ax.scatter(traj[n, 0], traj[n, 1], traj[n, 2], c='k', alpha=0)
        polygon = Poly3DCollection([sv.vertices[region]], alpha=1.0)
        polygon.set_color(m.to_rgba(areas[n]))
        ax.add_collection3d(polygon)

    ax.set_xlabel(r'$k_x$')
    ax.set_ylabel(r'$k_y$')
    ax.set_zlabel(r'$k_z$')
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])
    cbar = fig.colorbar(m, shrink=0.75, pad=0.15, label='Relative Area [a.u.]')
    ax.set_title(title)


def gm_3D_trajectory(n):
    """
    3D Golden means trajectory as proposed by Chan et al.

    Input:
        n: Number of spokes
    """
    # Find the eigen values in equation [5]
    A = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 0, 1]])
    w, v = np.linalg.eig(A)
    ea = np.real(v[:, 0])
    # Normalise the eigen vector
    ea /= max(ea)
    v1 = ea[0]
    v2 = ea[1]
    print("v1: {}, v2: {}".format(v1, v2))
    m = np.arange(n)
    phi = 2*np.pi*m*v2
    theta = np.arccos(np.mod(m*v1, 1))

    traj = np.zeros((n, 3))
    traj[:, 0] = np.cos(phi)*np.sin(theta)
    traj[:, 1] = np.sin(phi)*np.sin(theta)
    traj[:, 2] = np.cos(theta)

    return traj
