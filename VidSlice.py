from PIL import Image
import numpy as np

class VidSlice(object):
    __slots__ = ['clip', 'grid_pos', 'features', 'paired', 'square_size', 'ulx', 'uly', 'lrx', 'lry']
    def __init__(self, crop_img, grid_pos):

        if len(crop_img.shape) != 4 or crop_img.shape[1] != crop_img.shape[2]:
            raise ValueError(f'Clip passed into VidSlice() must be a 4d matrix '
                             f'with the middle two dimensions equal. given shape: {crop_img.shape}')
        if crop_img.shape[0] == 0:
            raise ValueError(f'Clip with shape {crop_img.shape} has no frames!')

        self.clip = crop_img
        self.grid_pos = grid_pos
        self.features = self._get_features(crop_img)
        self.paired = False
        self.square_size = self.clip.shape[1]
        self.ulx = grid_pos[0] * self.square_size
        self.uly = grid_pos[1] * self.square_size
        self.lrx = (grid_pos[0] + 1) * self.square_size
        self.lry = (grid_pos[1] + 1) * self.square_size


    def _get_features(self, clip, size=2, out_len=2):
        # first downsample each frame with PIL's resize
        downsampled = []
        for img in clip:
            down_frame = Image.fromarray(img).resize((size, size), Image.BILINEAR)
            down_frame = np.array(down_frame).ravel() # all values in flat sequence
            downsampled.append(down_frame)
        downsampled = np.array(downsampled)
        # then average together nearby frames to end up with only @outlen
        result = np.array([], dtype='uint8')
        split_indices = np.array_split(np.arange(clip.shape[0]), out_len)
        for inds in split_indices:
            x = downsampled[inds]
            means = np.round(np.mean(x, 1)).astype('uint8')
            result = np.concatenate([result, means])

        return result
