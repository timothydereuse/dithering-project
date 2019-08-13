
from moviepy.editor import *
import csv
import itertools as iter
from importlib import reload

vids_dir = "C:/Users/Tim/Documents/rawfootage"
csv_dir = "./csv"


def parse_csv(csv_fname):
    starts = []
    with open(csv_fname, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            starts.append(int(row[0]))

    timings = []
    for i in range(len(starts) - 1):
        timings.append((starts[i] / 1000, (starts[i+1] - starts[i]) / 1000 ))
    return timings


def lost_civ_load():
    square_size = 90
    offsets = [0, 1, 2]
    timings = parse_csv(f"{csv_dir}/lostcivtiming.csv")

    dorval_rev_fname = f"{vids_dir}/dorvalisland_rev.mp4"
    dorval_fname = f"{vids_dir}/dorvalisland.mp4"
    waterfall_fname = f"{vids_dir}/gaywaterfall.mp4"

    clip1 = VideoFileClip(dorval_rev_fname).without_audio()
    clip2 = VideoFileClip(dorval_fname).without_audio().resize(0.8).fx(vfx.rotate, 180)
    clip3 = VideoFileClip(waterfall_fname).without_audio().resize(0.5)

    target = VideoFileClip(dorval_fname).without_audio().fx(vfx.speedx, 0.81)

    return [clip1, clip2, clip3], target, square_size, timings, offsets


def foreshortened_quiet_load():
    square_size = 60
    timings = [(i * 1.5, 1.5) for i in range(120)]
    offsets = [60, 90]
    target_fname = f"{vids_dir}/longnight.mp4"
    source_fname = f"{vids_dir}/longnight.mp4"

    target = VideoFileClip(source_fname).without_audio().fx(vfx.invert_colors).fx(vfx.lum_contrast, 70, 70)

    clip1 = VideoFileClip(source_fname).without_audio().fx(vfx.invert_colors).resize(1.1).fx(vfx.rotate, 180)
    clip2 = VideoFileClip(source_fname).without_audio().fx(vfx.invert_colors).fx(vfx.lum_contrast, 40, 40).resize(0.5)

    return [clip1, clip2], target, square_size, timings, offsets


def foreshortened_loud_load():
    square_size = 60
    timings = [(i * 1.5, 1.5) for i in range(90)]
    offsets = [2, 11, 29, 37]

    clips = [f"{vids_dir}/ph{i}_bent-converted.mp4" for i in [1, 4, 3, 5]]
    sims = [f"{vids_dir}/simothy{i}_bent-converted.mp4" for i in [2, 5]]

    sources = [VideoFileClip(f) for f in [clips[2], clips[3], sims[1], clips[4], clips[1]]]
    sources = concatenate_videoclips(sources).without_audio().set_fps(29)
    target = [VideoFileClip(f) for f in [clips[3], clips[2], sims[0]]]
    target = concatenate_videoclips(target).without_audio().set_fps(29)

    target = target.fx(vfx.loop).fx(vfx.rotate, 90).resize([1920, 1080])
    clip1 = sources.fx(vfx.loop).resize([960, 560])
    clip2 = sources.fx(vfx.loop).fx(vfx.rotate, 270).resize([1060.0, 560])
    clip3 = sources.fx(vfx.loop).fx(vfx.rotate, 90).resize([1060, 560])
    clip4 = sources.fx(vfx.loop).fx(vfx.rotate, 180).resize([960.0, 560])

    return [clip1, clip2, clip3, clip4], target, square_size, timings, offsets


def light_up_load():
    square_size = 60
    offsets = [0, 0, 4]
    timings = parse_csv(f"{csv_dir}/lightuptiming.csv")

    source1_fname = f"{vids_dir}/values.mp4"
    source2_fname = f"{vids_dir}/widespread2.mp4"
    target_fname = f"{vids_dir}/village.mp4"

    print('clip1')
    clip1 = VideoFileClip(source1_fname).without_audio()\
        .fx(vfx.loop).resize([1920, 1080])\
        .fx(vfx.rotate, 180)\
        .set_fps(29)
    print('clip2')
    clips2 = concatenate_videoclips([
        VideoFileClip(source2_fname),
        VideoFileClip(source2_fname).fx(vfx.invert_colors),
    ])
    clip2 = clips2.without_audio()\
        .fx(vfx.loop).resize([1920, 1080])\
        .set_fps(29)
    print('clip3')
    clip3 = VideoFileClip(target_fname).without_audio()\
        .fx(vfx.loop).resize(0.5)\
        .set_fps(29)
    print('clip4')
    target = VideoFileClip(target_fname).without_audio()\
        .fx(vfx.loop)\
        .fx(vfx.lum_contrast, 0, 20)\
        .set_fps(29)

    return [clip1, clip2, clip3], target, square_size, timings, offsets


def angels_load():
    square_size = 80
    offsets = [0, 29, 15]
    timings = parse_csv(f"{csv_dir}/angelstiming.csv")

    target_name = f"{vids_dir}/angelsrawsource.mp4"
    mainsource_fname = f"{vids_dir}/angelsbroll.mp4"
    source2_fname =  f"{vids_dir}/angelsbroll.mp4"

    target = VideoFileClip(target_name).without_audio().fx(vfx.loop)
    clip1 = VideoFileClip(mainsource_fname)\
        .without_audio()\
        .fx(vfx.loop).set_fps(29)
    clip2 = VideoFileClip(mainsource_fname)\
        .without_audio()\
        .fx(vfx.loop)\
        .fx(vfx.mirror_x)\
        .fx(vfx.lum_contrast, -30, 2).set_fps(29)
    clip3 = VideoFileClip(source2_fname)\
        .without_audio()\
        .fx(vfx.loop)\
        .resize(0.8).set_fps(29)

    return [clip1, clip2, clip3], target, square_size, timings, offsets


def smut_load():
    square_size = 80
    offsets = [0, 40, 70]
    timings = parse_csv(f"{csv_dir}/smuttiming.csv")

    target_name = f"{vids_dir}/musclestarget.mp4"
    source_name = f"{vids_dir}/musclesource.mp4"

    target = VideoFileClip(target_name).without_audio().fx(vfx.loop).set_fps(29)
    clip1 = VideoFileClip(source_name)\
        .without_audio()\
        .fx(vfx.loop).set_fps(29)
    clip2 = VideoFileClip(source_name)\
        .without_audio()\
        .fx(vfx.loop)\
        .fx(vfx.mirror_y)\
        .fx(vfx.lum_contrast, -30, 2).set_fps(29)
    clip3 = VideoFileClip(source_name)\
        .without_audio()\
        .fx(vfx.rotate, 90)\
        .resize(0.8) \
        .fx(vfx.loop).set_fps(29)

    return [clip1, clip2, clip3], target, square_size, timings, offsets

def sour_load():
    square_size = 90
    offsets = [0, 60, 120, 180]
    timings = parse_csv(f"{csv_dir}/sourtiming.csv")

    target_name = f"{vids_dir}/sourdeathsource.mp4"

    target = VideoFileClip(target_name).without_audio().fx(vfx.loop).set_fps(29)
    clip1 = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.loop).\
        resize(0.70).set_fps(29)\

    clip2 = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.loop)\
        .fx(vfx.mirror_y)\
        .resize(0.75).set_fps(29)
    clip3 = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.rotate, 90)\
        .resize(0.50) \
        .fx(vfx.loop).set_fps(29)
    clip4 = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.rotate, 270)\
        .resize(0.60) \
        .fx(vfx.loop).set_fps(29)

    return [clip1, clip2, clip3, clip4], target, square_size, timings, offsets


def monstrous_load():
    square_size = 120
    offsets = [0, 15, 2]
    timings = [(i * 3, 3) for i in range(60)]

    target_name = f"{vids_dir}/gaywaterfall.mp4"
    forest_edit_name = f"{vids_dir}/MONSTROUS source.mp4"
    forest_name = f"{vids_dir}/forest1.mp4"

    target = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.loop)\
        .set_fps(29)\
        .fx(vfx.lum_contrast, 1, 1)
    clip1 = VideoFileClip(forest_edit_name)\
        .without_audio()\
        .fx(vfx.loop)\
        .set_fps(29)
    clip2 = VideoFileClip(target_name)\
        .without_audio()\
        .fx(vfx.loop)\
        .fx(vfx.mirror_y)\
        .resize(0.7).set_fps(29)
    clip3 = VideoFileClip(forest_name)\
        .without_audio()\
        .fx(vfx.loop).set_fps(29)

    return [clip1, clip2, clip3], target, square_size, timings, offsets
