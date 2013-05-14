# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from marionette.errors import ElementNotVisibleException


class FullscreenVideo(Base):

    _video_controls_locator = ('id', 'videoControls')
    _video_title_locator = ('id', 'video-title')
    _elapsed_text_locator = ('id', 'elapsed-text')
    _video_title_locator = ('id', 'video-title')
    _video_player_locator = ('id', 'player')
    _video_frame_locator = ('css selector', "iframe[src^='app://video'][src$='view.html']")
    _video_player_frame_locator = ('id', 'videoFrame')
    _video_loaded_locator = ('css selector', 'video[style]')

    def tap_control_bar(self):
        self.wait_for_element_displayed(*self._video_controls_locator)
        video_controls_locator = self.marionette.find_element(*self._video_controls_locator)
        try:
            self.marionette.tap(video_controls_locator)
        except ElementNotVisibleException:
            self.marionette.find_element(*self._video_player_locator).tap()

        self.wait_for_element_displayed(*self._elapsed_text_locator)

    @property
    def elapsed_time(self):
        return self.marionette.find_element(*self._elapsed_text_locator).text

    @property
    def name(self):
        return self.marionette.find_element(*self._video_title_locator).text

    @property
    def is_video_playing(self):
        return self.marionette.find_element(*self._video_player_locator).get_attribute('paused') == 'false'

    def switch_to_video_frame(self):
        self.marionette.switch_to_frame(self.marionette.find_element(*self._video_frame_locator))
        self.wait_for_element_displayed(*self._video_player_frame_locator)
        self.wait_for_element_displayed(*self._video_loaded_locator)
