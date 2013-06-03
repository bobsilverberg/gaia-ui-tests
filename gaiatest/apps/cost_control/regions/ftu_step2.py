# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from gaiatest.apps.cost_control.app import CostControl
from gaiatest.apps.cost_control.regions.ftu_step3 import FTUStep3


class FTUStep2(CostControl):

    _data_report_title_locator = ('css selector', 'h1[data-l10n-id="fte-onlydata2-title"]')
    _reset_report_period_select_locator = ('css selector', '#non-vivo-step-1 ul li:nth-child(1) span')
    _next_button_locator = ('css selector', '#non-vivo-step-1 span[data-l10n-id="next"]')

    def __init__(self, marionette):
        CostControl.__init__(self, marionette)
        self.wait_for_element_displayed(*self._data_report_title_locator)
        # Wait for the <script defer> to complete
        time.sleep(1)

    def select_reset_report_value(self, value):
        self.wait_for_element_displayed(*self._reset_report_period_select_locator)
        reset_time = self.marionette.find_element(*self._reset_report_period_select_locator)
        # TODO: Switch to using tap() when bug #869041 is fixed
        reset_time.tap()
        self.select(value)

    def tap_next(self):
        self.wait_for_element_displayed(*self._next_button_locator)
        self.marionette.find_element(*self._next_button_locator).tap()
        return FTUStep3(self.marionette)
