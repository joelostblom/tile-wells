import os
import argparse
from glob import iglob
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
from joblib import Parallel, delayed

'''Place the well images of tiled fields in a layout similar to a multiwell
plate. This makes it easy to get an overview of the different conditions in
the plate.
'''
def main():
    parser = argparse.ArgumentParser(description='Place the well images of '
        'tiled fields in a layout similar to a multiwell plate. This makes it '
        'easy to get an overview of the different conditions in the plate.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('path', default='./sorted-well-images', nargs='?',
        help='path to well images (default: %(default)s)')
    parser.add_argument('-i', '--input-format', default='jpg',
        help='format for images to be tiled (default: %(default)s)')
    parser.add_argument('-o', '--output-format', default='jpg',
        help='format for the tiled output image (default: %(default)s)')

    args = parser.parse_args()
    output_format = args.output_format.lower()
    input_format = args.input_format.lower()
    # Prevent figure windows from showing up
    plt.ioff()
    channels = [2,3]
    img_dir = Path(args.path)
    path_match_string = '{}' + '*.{}'.format(input_format)
    well_dir = img_dir.joinpath(path_match_string)
    tiled_img_dir = img_dir.resolve().parent.joinpath('tiled-well-images')
    tiled_img_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    timestamp_dir = tiled_img_dir.joinpath(timestamp)
    timestamp_dir.mkdir()
    # Process each channel in parallel
    results = Parallel(n_jobs=-2)(delayed(tile_wells) # Function
        (img_dir, channel, input_format, output_format, timestamp_dir) # Arguments
        for channel in channels) # Loop to parallelize


def tile_wells(img_dir, channel, input_format, output_format, timestamp_dir):
    '''Layout the well images in a grid representing the multiwell plate'''
    print(channel)
    img_names = sorted(list(img_dir.glob('{}-*.{}'.format(channel, input_format))))
    rows = set([img.name[2] for img in img_names])
    cols = set([int(img.name[3:5]) for img in img_names])
    fig, axes = plt.subplots(len(rows), len(cols), figsize=(len(cols)*4, len(rows)*4))
    for ax, img_name in zip(axes.ravel(), img_names):
        print(img_name.name)
        ax.axis('off')
        ax.imshow(plt.imread(img_name), cmap='gray', vmin=0, vmax=256)
#         ax.set_title(img_name.name, fontsize=20, color='white', y=0.5)
#     fig.tight_layout(pad=20, w_pad=50, h_pad=50, rect=[0, 0, 0.992, 0.993])
    fig.tight_layout(pad=0, w_pad=-3.7, h_pad=-2.7, rect=[0, 0, 0.992, 0.993])
    # Pyplot can't handle Path object yet, lands in 2.1
    # https://github.com/matplotlib/matplotlib/pull/8481
    print('Saving image...')
    fig.savefig(timestamp_dir.joinpath('ch{}.{}'.format(
        channel, output_format)).as_posix(), dpi=200)#, bbox_inches='tight', pad_inches=0)
    return None


if __name__ == '__main__':
    main()
