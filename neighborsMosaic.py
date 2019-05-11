from PIL import Image, ImageOps
import numpy as np
import itertools as iter
from importlib import reload
from sklearn.neighbors import NearestNeighbors
import diffPairs as dp
reload(dp)

img_fname = 'selfie1.jpg'
other_imgs_fnames = ['selfie2.jpg', 'selfie3.jpg', 'selfie4.jpg', 'selfie5.jpg', 'selfie6.jpg']
output_fname = 'output.png'
square_size = 70
stretch_amt = 1.2
dwnspl_others = 0.5
diffusion_amt = 0

def avg_color(img):
    arr = [j[:3] for sub in np.array(img) for j in sub]
    sum_pix = np.sum(arr, 0)
    sum_pix = sum_pix / len(arr)
    return sum_pix


def downsample_difference(img, size=3):
    down = np.array(img.resize((size,size), Image.BILINEAR))
    return down.ravel()


class CropImg(object):
    __slots__ = ['img', 'orig_box', 'val', 'paired']
    def __init__(self, crop_img, box):
        self.img = crop_img
        self.orig_box = box
        self.val = downsample_difference(crop_img)
        # self.val = avg_color(crop_img)
        self.paired = False


def get_squares_from_img(img_in, square_size=square_size):
    grid_size_x = (img_in.size[0] // square_size) - 1
    grid_size_y = (img_in.size[1] // square_size) - 1

    squares = [[0 for j in range(grid_size_y)] for i in range(grid_size_x)]
    for i in range(grid_size_x):
        for j in range(grid_size_y):
            box = (i * square_size, j * square_size, (i + 1)*square_size, (j + 1)*square_size)
            region = img_in.crop(box)
            squares[i][j] = CropImg(region, box)
    return squares


def closest_square_match(match, sq_list):
    points = [x.val for x in sq_list]
    neigh = NearestNeighbors(1)
    neigh.fit(points)
    best_ind = neigh.kneighbors([match.val], 1, return_distance=False)[0][0]
    best_square = sq_list[best_ind]

    # best_diff = 10e10
    # best_square = 0
    # best_ind = 0
    # for i, x in enumerate(sq_list):
    #     diff = np.sum(np.abs(x.val - match.val)**2)
    #     if diff < best_diff:
    #         best_diff = diff
    #         best_square = x
    #         best_ind = i
    return best_square, (match.val - best_square.val), best_ind


def get_neighboring_squares(center, main_squares):
    x_size = len(main_squares[0])
    y_size = len(main_squares)
    free_squares = []
    for shift in list(iter.product([-1, 0, 1], [-1, 0, 1])):
        idxs = (center[0] + shift[0], center[1] + shift[1])
        try:
            sq = main_squares[idxs[0]][idxs[1]]
        except IndexError:
            continue
        if not sq.paired:
            free_squares.append(idxs)
    return free_squares

main_img = Image.open(img_fname).convert('RGB')
new_size = (int(main_img.size[0] * stretch_amt), int(main_img.size[1] * stretch_amt))
match_img = main_img.resize(new_size)

# other_imgs = [
#     # main_img.transpose(Image.FLIP_LEFT_RIGHT),
#     # main_img.transpose(Image.FLIP_TOP_BOTTOM),
#     # main_img.transpose(Image.ROTATE_180)
# ]

other_imgs = [Image.open(fname) for fname in other_imgs_fnames]

print('slicing images into squares...')
main_squares = get_squares_from_img(match_img)
other_squares = np.array([get_squares_from_img(x) for x in other_imgs]).ravel()

coordinates = list(iter.product(range(len(main_squares)), range(len(main_squares[0]))))
# np.random.shuffle(coordinates)

print('matching images...')
pairs = []
X = []
for c in coordinates:
    X.append(main_squares[c[0]][c[1]].val)
Y = np.array([sq.val for sq in other_squares])
ind_map = dp.min_diff_pair_mapping(X, Y, finish_early_factor=0.3)

# for i, coord in enumerate(coordinates):
#
#     if not i % 500:
#         print('   {} of {}...'.format(i, len(coordinates)))
#
#     cx, cy = coord
#     square_to_match = main_squares[cx][cy]
#     match, diff, best_ind = closest_square_match(square_to_match, other_squares)
#     square_to_match.paired = True
#     pairs.append((square_to_match, match))
#     other_squares = np.delete(other_squares, best_ind)
#
#     # diffuse error to neighboring cells
#     if not diffusion_amt:
#         continue
#     free_squares = get_neighboring_squares((cx, cy), main_squares)
#     if not free_squares:
#         continue
#     for s in free_squares:
#         edit_val = main_squares[s[0]][s[1]].val
#         main_squares[s[0]][s[1]].val = edit_val + (diff * diffusion_amt / len(free_squares))

# reassemble image from scraps
for x, y in enumerate(ind_map):
    cx, cy = coordinates[x]
    matched_square = other_squares[y]
    orig_square = main_squares[cx][cy]
    match_img.paste(matched_square.img, orig_square.orig_box)

match_img.save(output_fname)
