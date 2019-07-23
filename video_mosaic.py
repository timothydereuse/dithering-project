from PIL import Image, ImageOps
from moviepy.editor import *
import numpy as np
import itertools as iter
from importlib import reload
import diffPairs as dp
import get_video_slices as gvs
reload(dp)
reload(gvs)

movies_dir = "C:/Users/Tim/Documents/goprofootage"
image_fname = 'GOPR0065.MP4'
interval = 2
square_size = 120
full_raw_source = VideoFileClip('{}/{}'.format(movies_dir, image_fname)).without_audio()
source_clips = []
target_clips = []
for i in [5,15,25,45,55]:
    clip = full_raw_source.subclip(i, i+interval)
    vidslices = gvs.get_video_slices(clip, square_size)
    source_clips += list(vidslices.values())
clip = full_raw_source.subclip(30, 30+interval)
vidslices = gvs.get_video_slices(clip, square_size)
target_clips += list(vidslices.values())

X = [c.features for c in target_clips]
Y = [c.features for c in source_clips]
ind_map = dp.min_diff_pair_mapping(X, Y, finish_early_factor=0.1)
