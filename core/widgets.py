from durationwidget.widgets import TimeDurationWidget, LabeledNumberInput


class CustomTimeDurationWidget(TimeDurationWidget):
    def __init__(self, attrs=None, show_days=True, show_hours=True,
                 show_minutes=True, show_seconds=True):
        self.show_days = show_days
        self.show_hours = show_hours
        self.show_minutes = show_minutes
        self.show_seconds = show_seconds
        _widgets = []
        if show_days:
            _widgets.append(LabeledNumberInput(label='дни', type='days'))
        if show_hours:
            _widgets.append(LabeledNumberInput(label='часы', type='hours'))
        if show_minutes:
            _widgets.append(LabeledNumberInput(label='минуты', type='minutes'))
        if show_seconds:
            _widgets.append(LabeledNumberInput(label='секунды', type='seconds'))
        super(TimeDurationWidget, self).__init__(_widgets, attrs)
