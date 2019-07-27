from PIL import Image, ImageOps
from moviepy.editor import *
import numpy as np
import itertools as iter
from importlib import reload
import diffPairs as dp
import get_video_slices as gvs
import os
import datetime
reload(dp)
reload(gvs)

movies_dir = "C:/Users/Tim/Documents/goprofootage"
image_sources = [f"{movies_dir}/{f}" for f in
                 ['GOPR0063.MP4', 'GOPR0064.MP4', 'GOPR0064.MP4']
                 ]
image_target = 'GOPR0064.MP4'

timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
out_fname = f'textexport {timestamp}'


def interval_length_generator():
    start = 0
    while True:
        length = 0.1 + np.abs(np.random.normal(1, 1))
        yield start, length
        start = start + length


square_size = 120
full_raw_sources = [
    VideoFileClip(image_sources[0]).without_audio().resize(0.60),
    VideoFileClip(image_sources[0]).without_audio().resize(0.70),
    VideoFileClip(image_sources[0]).without_audio().resize(0.60)
]
full_raw_target = VideoFileClip(f"{movies_dir}/{image_target}").without_audio()
fps_out = 29
target_size = full_raw_target.size

num_intervals = 220

interval_gen = interval_length_generator()

for i in range(num_intervals):
    print(f'processing interval {i} of {num_intervals}...')

    clip_start, clip_length = interval_gen.__next__()

    source_clips = []
    target_clips = []

    # get source slices
    for source, offset in zip(full_raw_sources, [1, 2, 3, 4]):

        new_clip_start = (clip_start + offset) % source.duration
        new_clip_end = (new_clip_start + clip_length) % source.duration
        if new_clip_start > new_clip_end: # necessary if clip crosses ending
            new_clip_start = new_clip_end
            new_clip_end = new_clip_start + clip_length

        clip = source.subclip(new_clip_start, new_clip_start+clip_length)
        print(f'{new_clip_start}, {new_clip_start+clip_length}, {source.duration}')
        vidslices = gvs.get_video_slices(clip, square_size)
        source_clips += list(vidslices.values())

    # get target slices
    clip = full_raw_target.subclip(clip_start, clip_start + clip_length)
    vidslices = gvs.get_video_slices(clip, square_size)
    target_clips += list(vidslices.values())

    frames_this_interval = target_clips[0].clip.shape[0]

    X = [c.features for c in target_clips]
    Y = [c.features for c in source_clips]
    ind_map = dp.min_diff_pair_mapping(X, Y, finish_early_factor=0.1)

    reassembled = np.zeros([
        frames_this_interval,
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
        try:
            frame = reassembled[frame_idx]
        except IndexError:
            new_idx = np.clip(frames_this_interval - frame_idx, 0, np.inf)
            frame = reassembled[int(new_idx)]
        return frame

    final_clip = VideoClip(make_frame, duration=clip_length).rotate(-90)
    final_clip.write_videofile(f"{out_fname}_{i}.mp4", fps=fps_out, bitrate="60000k")

full_raw_target.close()
for x in full_raw_sources:
    x.close()

load_clips = [VideoFileClip(f"{out_fname}_{i}.mp4") for i in range(num_intervals)]
final_clip = concatenate_videoclips(load_clips)
final_clip.write_videofile(f"{out_fname}_together.mp4",fps=fps_out, bitrate="60000k")

for i in range(num_intervals):
    try:
        os.remove(f"{out_fname}_{i}.mp4")
    except OSError:
        pass
