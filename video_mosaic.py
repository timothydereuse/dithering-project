from PIL import Image, ImageOps
from moviepy.editor import *
import numpy as np
import itertools as iter
from importlib import reload
import diffPairs as dp
import get_video_slices as gvs
import os
reload(dp)
reload(gvs)

movies_dir = "C:/Users/Tim/Documents/goprofootage"
image_fname = 'GOPR0063.MP4'
out_fname = 'textexport2'
interval_length = 1
square_size = 60
full_raw_source = VideoFileClip('{}/{}'.format(movies_dir, image_fname)).without_audio()
fps_out = 29
target_size = full_raw_source.size

num_intervals = 30

for i in range(num_intervals):
    print(f'processing interval {i} of {num_intervals}...')

    source_clips = []
    target_clips = []

    # get source slices
    for j in [i + 30, i + 60]:
        clip = full_raw_source.subclip(j, j+interval_length)
        vidslices = gvs.get_video_slices(clip, square_size)
        source_clips += list(vidslices.values())

    # get target slices
    clip = full_raw_source.subclip(i, i+interval_length)
    vidslices = gvs.get_video_slices(clip, square_size)
    target_clips += list(vidslices.values())

    frames_per_interval = target_clips[0].clip.shape[0]

    X = [c.features for c in target_clips]
    Y = [c.features for c in source_clips]
    ind_map = dp.min_diff_pair_mapping(X, Y, finish_early_factor=0.1)

    reassembled = np.zeros([
        frames_per_interval,
        target_size[0],
        target_size[1],
        3], dtype='uint8')

    for n, ind in enumerate(ind_map):
        # get data from source at current frame
        source = source_clips[ind].clip
        # get position from target
        target = target_clips[n]
        reassembled[:, target.ulx:target.lrx, target.uly:target.lry, :] = source

    def make_frame(t):
        frame_idx = int(np.round(t * fps_out))
        return reassembled[frame_idx]

    final_clip = VideoClip(make_frame, duration=interval_length).rotate(-90)
    final_clip.write_videofile(f"{out_fname}_{i}.mp4", fps=fps_out, bitrate="60000k")

load_clips = [VideoFileClip(f"{out_fname}_{i}.mp4") for i in range(num_intervals)]
final_clip = concatenate_videoclips(load_clips)
final_clip.write_videofile(f"{out_fname}_together.mp4",fps=fps_out, bitrate="60000k")

for i in range(num_intervals):
    try:
        os.remove(f"{out_fname}_{i}.mp4")
    except OSError:
        pass
