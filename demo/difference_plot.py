import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import h5py
import numpy as np
plt.style.use('dark_background')


def main():
    static_img = h5py.File('static_phantom-cg.h5', 'r')['image'][0, ...]
    moving_img = h5py.File('moving_phantom-cg.h5', 'r')['image'][0, ...]
    moco_img = h5py.File(
        'moving_phantom_mocodir/moving_phantom_moco-cg.h5', 'r')['image'][0, ...]

    fig = plt.figure(constrained_layout=True, figsize=(12, 8))
    spec = gridspec.GridSpec(ncols=3, nrows=2, figure=fig)

    ax = fig.add_subplot(spec[0, 0])
    static_slice = np.rot90(abs(static_img[80, :, :]), 2)
    static_slice /= np.quantile(static_slice[:], 0.99)

    plt.imshow(static_slice, cmap='gray', vmin=0, vmax=1)
    plt.axis('off')
    plt.title("Static Ref", size=20)

    ax = fig.add_subplot(spec[0, 1])
    moving_slice = np.rot90(abs(moving_img[80, :, :]), 2)
    moving_slice /= np.quantile(moving_slice[:], 0.99)
    plt.imshow(moving_slice, cmap='gray', vmin=0, vmax=1)
    plt.axis('off')
    plt.title("Moving", size=20)

    ax = fig.add_subplot(spec[0, 2])
    moco_slice = np.rot90(abs(moco_img[80, :, :]), 2)
    moco_slice /= np.quantile(moco_slice[:], 0.99)
    plt.imshow(moco_slice, cmap='gray', vmin=0, vmax=1)
    plt.axis('off')
    plt.title("Corrected", size=20)

    ax = fig.add_subplot(spec[1, 1])
    plt.imshow(static_slice - moving_slice, cmap='gray', vmin=-0.1, vmax=0.1)
    plt.axis('off')

    ax = fig.add_subplot(spec[1, 2])
    plt.imshow(static_slice - moco_slice, cmap='gray', vmin=-0.1, vmax=0.1)
    plt.axis('off')

    plt.savefig('moco_diff_plot.png')
    plt.show()


if __name__ == "__main__":
    main()
