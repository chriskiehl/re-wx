import threading
import wx
import wx.lib.inspection
from pip._vendor.contextlib2 import contextmanager
from unittest import TestCase

from rewx import create_element, wsx, render, patch
import rewx.components as c
from tests import images

class TestStaticBitmap(TestCase):

    image_size = (32, 32)

    def test_gauge(self):
        cases  = [
            # {'uri': None},
            {},
            {'uri': images.red_uri},
            {'uri': images.red_uri, 'size': (64, 64)},
            {'uri': images.red_uri, 'size': (16, 16)}
        ]
        # expected_state = {
        #     'uri': images.kirbs_uri
        # }
        app = wx.App()
        for props in cases:
            with self.subTest(props):
                component = wsx(
                    [c.Frame, {'show': True, 'size': (100,100)},
                     [c.Block, {},
                      [c.StaticBitmap, {**props, 'proportion': 0}]]])
            frame = render(component, None)
            bitmap = frame.Children[0].Children[0]

            if 'uri' in props:
                self.assertIsNotNone(bitmap.GetBitmap().RefData)
            else:
                # when no URI is defined, there should similarly
                # be no bitmap data present
                self.assertEqual(bitmap.GetBitmap().RefData, None)

    def testUriUpdatesChangeImage(self):
        """
        Testing that swapping URI leads to the
        new images being loaded.
        """
        app = wx.App()

        with self.subTest("initializing with no URI"):
            component = wsx(
                [c.Frame, {'show': True, 'size': (100, 100)},
                 [c.StaticBitmap, {}]])
            frame = render(component, None)
            bitmap = frame.Children[0]
            # no images loaded
            self.assertEqual(bitmap.GetBitmap().RefData, None)

        with self.subTest('Adding a URI loads the image'):
            patch(bitmap, create_element(c.StaticBitmap, {'uri': images.red_uri}))
            original_rgb = self.get_rgb(bitmap)
            self.assertEqual(original_rgb, images.red_rgb)

        with self.subTest("updating props with new URI"):
            patch(bitmap, create_element(c.StaticBitmap, {'uri': images.pink_uri}))
            updated_rgb = self.get_rgb(bitmap)
            # colors should now be different because the image was updated
            self.assertNotEqual(original_rgb, updated_rgb)
            # and we should have our pink color:
            self.assertEqual(updated_rgb, images.pink_rgb)


    def get_rgb(self, bitmap: wx.StaticBitmap):
        """Grab the rgb value of the first color in the image"""
        bytes = wx.ImageFromBitmap(bitmap.GetBitmap()).GetData()
        return tuple([x for x in bytes][:3])
