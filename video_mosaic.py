from PIL import Image, ImageOps
from moviepy.editor import *
import numpy as np
import itertools as iter
from importlib import reload
import diffPairs as dp
import get_video_slices as gvs
import os
import datetime
import video_source_schemes as vss
import os

reload(vss)
reload(dp)
reload(gvs)

proj_name = 'FORESHORTENED2'
sourcefunc = vss.foreshortened_loud_load
cwd = os.getcwd()
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
out_fname = f"{proj_name}_{timestamp}"
wkdr = f'{cwd}/{out_fname}'
os.mkdir(wkdr)

full_raw_sources, full_raw_target, timings, offsets = sourcefunc()
max_intervals = np.inf
square_size = 60
fps_out = 29
target_size = full_raw_target.size

num_intervals = min(len(timings), max_intervals)

for i in range(num_intervals):
    print(f'processing interval {i} of {num_intervals}...')

    clip_start, clip_length = timings[i]

    source_clips = []
    target_clips = []

    # get source slices
    for source, offset in zip(full_raw_sources, offsets):

        new_clip_start = (clip_start + offset)
        new_clip_end = (new_clip_start + clip_length)

        clip = source.subclip(new_clip_start, new_clip_start+clip_length)
        vidslices = gvs.get_video_slices(clip, square_size, fps_out)
        source_clips += list(vidslices.values())

    # get target slices
    clip = full_raw_target.subclip(clip_start, clip_start + clip_length)
    print(f'{clip.duration}')
    vidslices = gvs.get_video_slices(clip, square_size, fps_out)
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
        frame_idx = np.clip(frame_idx, 0, reassembled.shape[0] - 1, dtype='uint8')
        frame = reassembled[frame_idx]
        return frame

    final_clip = VideoClip(make_frame, duration=clip_length).rotate(-90)
    final_clip.write_videofile(f"{wkdr}/{out_fname}_{i}.mp4", fps=fps_out, bitrate="30000k")

full_raw_target.close()
for x in full_raw_sources:
    x.close()


def merge_video_files(fnames, output_fname, fps_out):
    load_clips = [VideoFileClip(f) for f in fnames]
    final_clip = concatenate_videoclips(load_clips)
    final_clip.write_videofile(output_fname, fps=fps_out, bitrate="40000k")
    for fname in fnames:
        try:
            os.remove(fname)
        except OSError:
            pass


chunk_names = [f"{out_fname}_{i}.mp4" for i in range(num_intervals)]
with open(f"{wkdr}/{out_fname}_fnames.txt", mode="w") as f:
    for c in chunk_names:
        f.write(f"file {c}\n")

print(f'ffmpeg -f concat -i {out_fname}_fnames.txt -c copy output.mp4')


