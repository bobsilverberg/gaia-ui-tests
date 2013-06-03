# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCamera(GaiaTestCase):

    _capture_button_locator = ('id', 'capture-button')
    _focus_ring = ('id', 'focus-ring')
    _video_mode_locator = ('css selector', 'body.video')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')
    # This is a workaround for the Bug 832045
    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        # launch the Camera app
        self.app = self.apps.launch('camera')

        self.wait_for_element_present(*self._capture_button_enabled_locator)

    def test_capture_a_photo(self):
        # https://moztrap.mozilla.org/manage/case/1325/

        capture_button = self.marionette.find_element(*self._capture_button_locator)
        capture_button.tap()

        # Wait to complete focusing
        self.wait_for_condition(lambda m: m.find_element(*self._focus_ring).get_attribute('data-state') == 'focused',
            message="Camera failed to focus")

        # Wait for image to be added in to filmstrip
        # TODO investigate lowering this timeout in the future
        self.wait_for_element_displayed(*self._film_strip_image_locator, timeout=20)

        # Find the new picture in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())
