from typing import Tuple

from PIL import Image  # type: ignore
import wx  # type: ignore


def load(img_path) -> Image:
    return Image.open(img_path)


def resize_image(im: Image, size: Tuple[int, int]):
    im.thumbnail(size)
    return im


def to_bitmap(im: Image):
    try:
        rgba = im.convert('RGBA').tobytes()
    except AttributeError:
        rgba = im.convert('RGBA').tostring()

    return wx.Bitmap.FromBufferRGBA(im.size[0], im.size[1], rgba)
