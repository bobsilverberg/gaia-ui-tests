# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.base import Base
from gaiatest.apps.base import PageRegion


class Clock(Base):

    name = 'Clock'

    _alarm_create_new_locator = ('id', 'alarm-new')
    _analog_clock_display_locator = ('id', 'analog-clock-svg')
    _digital_clock_display_locator = ('id', 'digital-clock-display')
    _clock_day_date_locator = ('id', 'clock-day-date')
    _digital_clock_hour24_state_locator = ('id', 'clock-hour24-state')
    _all_alarms_locator = ('css selector', '#alarms li')
    _banner_countdown_notification_locator = ('id', 'banner-countdown')

    def launch(self):
        Base.launch(self)
        self.wait_for_new_alarm_button()

    @property
    def is_digital_clock_displayed(self):
        return self.is_element_displayed(*self._digital_clock_display_locator)

    @property
    def is_analog_clock_displayed(self):
        return self.is_element_displayed(*self._analog_clock_display_locator)

    @property
    def is_day_and_date_displayed(self):
        return self.is_element_displayed(*self._clock_day_date_locator)

    @property
    def is_24_hour_state_displayed(self):
        return self.is_element_displayed(*self._digital_clock_hour24_state_locator)

    @property
    def banner_countdown_notification(self):
        return self.marionette.find_element(*self._banner_countdown_notification_locator).text

    @property
    def alarms(self):
        return [self.Alarm(self.marionette, alarm) for alarm in self.marionette.find_elements(*self._all_alarms_locator)]

    def wait_for_new_alarm_button(self):
        self.wait_for_element_displayed(*self._alarm_create_new_locator)

    def wait_for_banner_not_visible(self):
        self.wait_for_element_not_displayed(*self._banner_countdown_notification_locator)

    def wait_for_banner_displayed(self):
        self.wait_for_element_displayed(*self._banner_countdown_notification_locator)

    def tap_analog_display(self):
        self.wait_for_element_displayed(*self._analog_clock_display_locator)
        self.marionette.find_element(*self._analog_clock_display_locator).tap()
        self.wait_for_element_displayed(*self._digital_clock_display_locator)

    def tap_digital_display(self):
        self.wait_for_element_displayed(*self._digital_clock_display_locator)
        self.marionette.find_element(*self._digital_clock_display_locator).tap()
        self.wait_for_element_displayed(*self._analog_clock_display_locator)

    def tap_new_alarm(self):
        self.marionette.find_element(*self._alarm_create_new_locator).tap()

        from gaiatest.apps.clock.regions.alarm import NewAlarm
        new_alarm = NewAlarm(self.marionette)
        new_alarm.wait_for_picker_to_be_visible()
        return new_alarm

    class Alarm(PageRegion):

        _label_locator = ('css selector', 'div.label')
        _time_locator = ('css selector', 'div.alarmList-time')
        _tap_locator = ('id', 'alarm-item')
        _check_box_locator = ('id', 'input-enable')
        _enable_button_locator = ('css selector', 'label.alarmList')

        @property
        def label(self):
            return self.root_element.find_element(*self._label_locator).text

        @property
        def time(self):
            return self.root_element.find_element(*self._time_locator).text

        @property
        def is_alarm_active(self):
            return self.root_element.find_element(*self._check_box_locator).is_selected()

        def tap_checkbox(self):
            self.root_element.find_element(*self._enable_button_locator).tap()

        def tap(self):
            self.wait_for_element_displayed(*self._tap_locator)
            self.root_element.find_element(*self._tap_locator).tap()
            from gaiatest.apps.clock.regions.alarm import EditAlarm
            return EditAlarm(self.marionette)
