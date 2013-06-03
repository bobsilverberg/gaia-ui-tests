# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCameraMultipleShots(GaiaTestCase):

    # Camera application locators
    _capture_button_locator = ('id', 'capture-button')
    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')
    _focus_ring_locator = ('id', 'focus-ring')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')
    _film_strip_locator = ('id', 'filmstrip')
    _camera_button_locator = ('id', 'camera-button')
    _image_preview_locator = ('css selector', '#media-frame > img')
    _view_finder_locator = ('id', 'viewfinder')
    _body_locator = ('tag name', 'body')

    def setUp(self):

        GaiaTestCase.setUp(self)

        # Turn off Geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        # Launch the Camera application
        self.app = self.apps.launch('camera')

        self.wait_for_element_present(*self._capture_button_enabled_locator)

    def test_capture_multiple_shots(self):
        # https://moztrap.mozilla.org/manage/case/1325/

        # Take several pictures and preview each thumbnail
        self.take_photo()
        self.preview_image(thumbnail=0)

        self.take_photo()
        self.preview_image(thumbnail=1)

        self.take_photo()
        self.preview_image(thumbnail=2)

    def preview_image(self, thumbnail):

        # Tap the view-finder, wait for the film-strip to appear
        # The event is on the id=viewFinder but marionette won't let us tap that
        body = self.marionette.find_element(*self._body_locator)
        body.tap()

        self.wait_for_element_displayed(*self._film_strip_image_locator)

        # Check that there are available thumbnails to select
        images = self.marionette.find_elements(*self._film_strip_image_locator)

        self.assertGreater(len(images), 0, 'No images found')
        images[thumbnail].tap()

        # Wait for image preview
        self.wait_for_element_displayed(*self._image_preview_locator)

        # Switch back to the camera
        camera_button = self.marionette.find_element(*self._camera_button_locator)
        camera_button.tap()

    def take_photo(self):

        # Tap the capture button
        capture_button = self.marionette.find_element(*self._capture_button_locator)
        capture_button.tap()

        # Wait to complete focusing
        self.wait_for_condition(lambda m: m.find_element(*self._focus_ring_locator).get_attribute('data-state') == 'focused')

        # Wait for image to be added in to filmstrip
        self.wait_for_element_displayed(*self._film_strip_image_locator)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())

        # Wait for the camera's focus state to 'ready' for the next shot
        self.wait_for_condition(lambda m: m.find_element(*self._focus_ring_locator).get_attribute('data-state') is None)

        # Wait for the filmstrip to hide
        self.wait_for_element_not_displayed(*self._film_strip_locator)
