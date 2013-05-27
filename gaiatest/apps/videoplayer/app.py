# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base


class VideoPlayer(Base):

    name = 'Video'

    _progress_bar_locator = ('id', 'progress')

    # Video list/summary view
    _video_items_locator = ('css selector', 'ul#thumbnails li[data-name]')
    _video_name_locator = ('css selector', 'div.details')

    _empty_video_title_locator = ('id', 'overlay-title')
    _empty_video_text_locator = ('id', 'overlay-text')

    def launch(self):
        Base.launch(self)
        self.wait_for_element_not_displayed(*self._progress_bar_locator)

    @property
    def total_video_count(self):
        return len(self.marionette.find_elements(*self._video_items_locator))

    @property
    def first_video_name(self):
        return self.marionette.find_element(*self._video_name_locator).get_attribute('data-title')

    def tap_first_video_item(self):
        first_video_item = self.marionette.find_elements(*self._video_items_locator)[0]
        first_video_item.tap()
        from gaiatest.apps.videoplayer.regions.fullscreen_video import FullscreenVideo
        fullscreen = FullscreenVideo(self.marionette)
        fullscreen.wait_for_player_frame_displayed()
        return fullscreen

    @property
    def empty_video_title(self):
        return self.marionette.find_element(*self._empty_video_title_locator).text

    @property
    def empty_video_text(self):
        return self.marionette.find_element(*self._empty_video_text_locator).text
