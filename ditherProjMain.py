import cv2
import numpy as np
import imageio
import errorSchemes as er
from importlib import reload
import colorsys
reload(er)

img_fname = 'landscape.png'
output_fname = 'output.gif'
num_frames = 64
fps = 10
size = 0.5
unsize = 3
norm = 1

img = cv2.imread(img_fname)
img = cv2.resize(img, (0,0), fx=size, fy=size)

# floyd-steinberg dithering
pallet_bw = np.array([
    [255, 255, 255],
    [0, 0, 0]
])

pallet = np.array([
    [255, 1, 2],
    [0, 255, 250],
    # [1, 0, 255]
])

def rotate_color(color, amt):
    color = color / 255
    color = colorsys.rgb_to_hsv(color[0], color[1], color[2])
    new_hue = (color[0] + amt) % 1
    color = colorsys.hsv_to_rgb(new_hue, color[1], color[2])
    color = np.array(color) * 255
    return color

def nudge_color(color, amt):
    for n in range(len(color)):
        color[n] += np.random.randint(-1*amt, amt)
    color = np.clip(color, 0, 255)
    return color

img_width = len(img)
img_height = len(img[0])
# coordinates = [(x, y) for x in range(img_width) for y in range(img_height)]
coordinates = [(x, y) for y in range(img_height) for x in range(img_width)]

frames = []
for fn in range(num_frames):
    print('dithering frame {}...'.format(fn))

    frame = np.array(img).astype('float')

    # get the pallet to use for this frame
    for n in range(len(pallet)):
        pallet[n] = rotate_color(pallet[n], 0.02)
    frame_pallet = np.concatenate([pallet, pallet_bw])
    print(frame_pallet)
    # frame_pallet = pallet[np.random.choice(pallet.shape[0], 6, replace=False), :]

    # get the error scheme to use for this frame
    #frame_err_scheme = er.fade_between_schemes(er.scheme_diag_large, er.scheme_uniform_small, float(fn) / num_frames)
    frame_err_scheme = er.normalize_scheme(er.scheme_floyd_steinberg)

    for c in coordinates:
        x, y = c[0], c[1]

        cur_pix = frame[x, y]

        # distance in color space from current pixel to all other pixels
        distances = [np.sum(np.abs(cur_pix - p)) for p in frame_pallet]
        use_color = frame_pallet[distances.index(min(distances))]

        difference = (cur_pix - use_color)
        frame[x, y] = np.array(use_color)

        for key in frame_err_scheme.keys():
            nx, ny = (x + key[0], y + key[1])
            if not (0 <= nx < img_width and 0 <= ny < img_height):
                continue

            correction = frame_err_scheme[key] * difference
            frame[nx, ny] += correction

    frames.append(np.round(frame).astype('uint8'))

# img = np.round(img).astype('uint8')
# img = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=0)
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

with imageio.get_writer(output_fname, mode='I', fps=fps) as writer:
    for frame in frames:
        frame = cv2.resize(frame, (0,0), fx=unsize, fy=unsize, interpolation=0)
        writer.append_data(frame)
