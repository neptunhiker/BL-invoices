# Class of AVGS Gutschein

import datetime


class AVGSCoupon:

    def __init__(self, avgs_nr: str, time_period_start: datetime.date, time_period_end: datetime.date):
        """
        :param avgs_nr: Gutscheinnummer
        :type avgs_nr: str
        :param time_period_start: Starting date of AVGS Gutschein (Bewilligungszeitraum)
        :type time_period_start: datetime.date
        :param time_period_end: Ending date of AVGS Gutschein (Bewilligungszeitraum)
        :type time_period_end: datetime.date
        """
        self.nr = avgs_nr
        self._time_period_start = time_period_start
        self._time_period_end = time_period_end
        self._time_period_length = (time_period_end - time_period_start).days

    @property
    def time_period_start(self):
        return self._time_period_start

    @property
    def time_period_end(self):
        return self._time_period_end

    @property
    def time_period_length(self):
        return self._time_period_length

    @time_period_start.setter
    def time_period_start(self, value):
        self._time_period_start = value
        self._time_period_length = (self._time_period_end - self._time_period_start).days

    @time_period_end.setter
    def time_period_end(self, value):
        self._time_period_end = value
        self._time_period_length = (self._time_period_end - self._time_period_start).days

    def __str__(self):
        return f"AVGS-Gutscheinnummer: {self.nr}\n" \
               f"Bewilligungszeitraum: {self._time_period_start.strftime('%d. %b %Y')} " \
               f"bis {self._time_period_end.strftime('%d. %b %Y')}\n" \
               f"Länge des Bewilligungszeitraums: {self._time_period_length} Tage"

def main():
    coupon = AVGSCoupon(avgs_nr="lkjsdfas-5", time_period_start=datetime.date(2021, 11, 23),
                        time_period_end=datetime.date(2022, 1, 22))

    print(coupon.__str__())



if __name__ == '__main__':
    main()