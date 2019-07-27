# import moviepy
from moviepy.editor import *
import numpy as np
import itertools as iter
import VidSlice
from PIL import Image, ImageOps

from importlib import reload
reload(VidSlice)


def get_video_slices(clip, square_size):
    fps = clip.fps
    nframes = int(clip.fps * clip.duration)
    x_grid_size = int(clip.size[0] / square_size)
    y_grid_size = int(clip.size[1] / square_size)
    coordinates = list(iter.product(range(x_grid_size), range(y_grid_size)))

    vidslices = {}
    for x_off, y_off in coordinates:
        vidslices[(x_off, y_off)] = np.zeros([nframes, square_size, square_size, 3], dtype='uint8')

    # assemble individual bits
    for t in range(nframes):
        frame = clip.get_frame(t / fps)
        frame = frame.transpose((1, 0, 2))
        for x_off, y_off in coordinates:
            square = frame[
                x_off*square_size:(x_off+1)*square_size,
                y_off*square_size:(y_off+1)*square_size,
                :]
            vidslices[(x_off, y_off)][t] = square

    for pair in coordinates:
        vidslices[pair] = VidSlice.VidSlice(vidslices[pair], pair)

    return vidslices


if __name__ == '__main__':
    movies_dir = "C:/Users/Tim/Documents/goprofootage"
    image_fname = 'GOPR0066.MP4'
    image_target_fname = 'GOPR0067.MP4'

    square_size = 120
    clip = VideoFileClip('{}/{}'.format(movies_dir, image_fname)).without_audio().subclip(1,2)
    vidslices = get_video_slices(clip, square_size)

    # txt_clip = TextClip("OOGH",fontsize=90,color='white')
    # txt_clip = txt_clip.set_pos('center').set_duration(1)
    # video = CompositeVideoClip([clip, txt_clip])
    #
    # # Write the result to a file (many options available !)
    # video.write_videofile("test_imgexport.webm")
