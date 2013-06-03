# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from marionette.marionette import Actions


class TestCameraUnlockWithPasscode(GaiaTestCase):

    # Input data
    _input_passcode = '7931'

    _camera_button_locator = ('id', 'lockscreen-area-camera')

    _camera_frame_locator = ('css selector', 'iframe[src^="./camera/index.html"]')
    _capture_button_locator = ('css selector', '#capture-button:not([disabled])')
    _gallery_button_locator = ('id', 'gallery-button')

    _switch_source_button_locator = ('id', 'switch-button')

    def setUp(self):
        GaiaTestCase.setUp(self)

        self.data_layer.set_setting('lockscreen.passcode-lock.code', self._input_passcode)
        self.data_layer.set_setting('lockscreen.passcode-lock.enabled', True)

        # this time we need it locked!
        self.lockscreen.lock()

    def test_unlock_to_camera_with_passcode(self):
        # https://github.com/mozilla/gaia-ui-tests/issues/479

        # TODO: This currently does not work due to Touch failures,
        # but this being a high priority test I am taking advantage of bug 813561 to tap the camera button
        # self._swipe_and_unlock()

        # Tap does not work here
        camera_button = self.marionette.find_element(*self._camera_button_locator)
        camera_button.click()

        self.wait_for_element_present(*self._camera_frame_locator)
        camera_frame = self.marionette.find_element(*self._camera_frame_locator)
        self.marionette.switch_to_frame(camera_frame)

        # Wait fot the capture button displayed. no need to take a photo.
        self.wait_for_element_displayed(*self._capture_button_locator)

        self.assertFalse(self.is_element_displayed(*self._gallery_button_locator))

        switch_source_button = self.marionette.find_element(*self._switch_source_button_locator)
        switch_source_button.tap()

        self.wait_for_element_present(*self._capture_button_locator)

        self.assertFalse(self.is_element_displayed(*self._gallery_button_locator))

    def _swipe_and_unlock(self):

        unlock_handle = self.marionette.find_element(*self._lockscreen_handle_locator)
        unlock_handle_x_centre = int(unlock_handle.size['width'] / 2)
        unlock_handle_y_centre = int(unlock_handle.size['height'] / 2)

        # Get the end position from the demo animation
        lockscreen_area = self.marionette.find_element(*self._lockscreen_area_locator)
        end_animation_position = lockscreen_area.size['height'] - unlock_handle.size['height']

        # Flick from unlock handle to (0, -end_animation_position) over 800ms duration
        Actions(self.marionette).flick(unlock_handle, unlock_handle_x_centre, unlock_handle_y_centre, 0, 0 - end_animation_position, 800).perform()

        # Wait for the svg to animate and handle to disappear
        # TODO add assertion that unlock buttons are visible after bug 813561 is fixed
        self.wait_for_condition(lambda m: not self.marionette.find_element(*self._lockscreen_handle_locator).is_displayed())
