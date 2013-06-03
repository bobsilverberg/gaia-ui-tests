# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase


class TestCamera(GaiaTestCase):

    _capture_button_locator = ('id', 'capture-button')
    # This is a workaround for the Bug 832045
    _capture_button_enabled_locator = ('css selector', '#capture-button:not([disabled])')
    _switch_source_button_locator = ('id', 'switch-button')
    _video_mode_locator = ('css selector', 'body.video')
    _film_strip_image_locator = ('css selector', '#filmstrip > img.thumbnail')
    _video_capturing_locator = ('css selector', 'body.capturing')
    _video_timer_locator = ('id', 'video-timer')

    def setUp(self):
        GaiaTestCase.setUp(self)

        # Turn off geolocation prompt
        self.apps.set_permission('Camera', 'geolocation', 'deny')

        # launch the Camera app
        self.app = self.apps.launch('camera')

        self.wait_for_element_present(*self._capture_button_enabled_locator)

    def test_capture_a_video(self):
        # https://moztrap.mozilla.org/manage/case/2477/

        switch_source_button = self.marionette.find_element(*self._switch_source_button_locator)

        switch_source_button.tap()
        self.wait_for_element_present(*self._capture_button_enabled_locator)

        capture_button = self.marionette.find_element(*self._capture_button_locator)
        capture_button.tap()

        self.wait_for_element_present(*self._video_capturing_locator)

        # Wait for 3 seconds of recording
        self.wait_for_condition(lambda m: m.find_element(
            *self._video_timer_locator).text == '00:03')

        # Stop recording
        capture_button.tap()
        self.wait_for_element_not_displayed(*self._video_timer_locator)

        # Wait for image to be added in to filmstrip
        self.wait_for_element_displayed(*self._film_strip_image_locator)

        # Find the new film thumbnail in the film strip
        self.assertTrue(self.marionette.find_element(*self._film_strip_image_locator).is_displayed())
