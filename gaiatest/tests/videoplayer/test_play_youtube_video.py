# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest import GaiaTestCase
from gaiatest.apps.browser.app import Browser
from gaiatest.apps.videoplayer.regions.fullscreen_video import FullscreenVideo


class TestYouTube(GaiaTestCase):

    video_URL = 'http://m.youtube.com/watch?v=5MzuGWFIfio'
    # YouTube video
    _video_container_locator = ('id', 'koya_elem_0_6')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.connect_to_network()

    def test_play_youtube_video(self):
        """ Confirm YouTube video playback

        https://moztrap.mozilla.org/manage/case/6073/

        """
        browser = Browser(self.marionette)
        browser.launch()

        browser.go_to_url(self.video_URL)
        browser.switch_to_content()

        # Tap the video
        self.wait_for_element_present(*self._video_container_locator)
        self.marionette.find_element(*self._video_container_locator).tap()
        self.marionette.switch_to_frame()
        fullscreen_video = FullscreenVideo(self.marionette)

        # Switch to video player
        fullscreen_video.switch_to_video_frame()

        # Check for playback
        self.assertTrue(fullscreen_video.is_video_playing)
