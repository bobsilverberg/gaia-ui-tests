# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.base import Base


class FullscreenVideo(Base):

    _video_controls_locator = ('id', 'videoControls')
    _video_title_locator = ('id', 'video-title')
    _elapsed_text_locator = ('id', 'elapsed-text')
    _video_player_locator = ('id', 'player')
    _video_frame_locator = ('css selector', "iframe[src^='app://video'][src$='view.html']")
    _video_player_frame_locator = ('id', 'fullscreen-view')
    _video_loaded_locator = ('css selector', 'video[style]')

    def wait_for_player_frame_displayed(self):
        self.wait_for_element_displayed(*self._video_player_frame_locator)

    def display_controls_with_js(self):
        self.marionette.execute_script("window.wrappedJSObject.showVideoControls(true);")
        self.wait_for_element_displayed(*self._video_controls_locator)

    @property
    def elapsed_time(self):
        # Convert it to a real time so we can accurately assert
        text = self.marionette.find_element(*self._elapsed_text_locator).text
        return time.strptime(text, '%M:%S')

    @property
    def name(self):
        return self.marionette.find_element(*self._video_title_locator).text

    @property
    def is_video_playing(self):
        return self.marionette.find_element(*self._video_player_locator).get_attribute('paused') == 'false'

    def switch_to_video_frame(self):
        self.marionette.switch_to_frame(self.marionette.find_element(*self._video_frame_locator))
        self.wait_for_element_displayed(*self._video_loaded_locator)
