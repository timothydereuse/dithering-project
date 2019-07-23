from PIL import Image
import numpy as np

class VidSlice(object):
    __slots__ = ['img', 'grid_pos', 'features', 'paired']
    def __init__(self, crop_img, grid_pos):
        self.img = crop_img
        self.grid_pos = grid_pos
        self.features = self._get_features(crop_img)
        self.paired = False

    def _get_features(self, imgs, size=2, out_len=2):
        # first downsample each frame with PIL's resize
        downsampled = []
        for img in imgs:
            down_frame = Image.fromarray(img).resize((size, size), Image.BILINEAR)
            down_frame = np.array(down_frame).ravel() # all values in flat sequence
            downsampled.append(down_frame)
        downsampled = np.array(downsampled)

        # then average together nearby frames to end up with only @outlen
        result = np.array([], dtype='uint8')
        split_indices = np.array_split(np.arange(imgs.shape[0]), out_len)
        for inds in split_indices:
            x = downsampled[inds]
            means = np.round(np.mean(x, 1)).astype('uint8')
            result = np.concatenate([result, means])

        return result
