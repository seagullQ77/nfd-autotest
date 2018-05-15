from faker.providers.date_time import Provider as FakerProvider
from datetime import datetime
from  datetime import timedelta


class Provider(FakerProvider):
    def date_today(cls, pattern='%Y-%m-%d', tzinfo=None):
        """
        Get today string
        :param pattern format
        :example '2008-11-27'
        """
        return datetime.now(tzinfo).strftime(pattern)

    def date_today_next(cls, pattern='%Y-%m-%d', tzinfo=None):
        """
        Gets a DateTime object for the current month, include days in current month after today.
        :param tzinfo: timezone, instance of datetime.tzinfo subclass
        :example DateTime('2012-04-04')
        :return DateTime
        """
        now = datetime.now(tzinfo)
        day_start = now + timedelta(days=1)
        day_end = now + timedelta(days=30)
        today_next = cls.date_time_between_dates(day_start, day_end, tzinfo)
        return today_next.strftime(pattern)

    def date_today_before(cls, pattern='%Y-%m-%d', tzinfo=None):
        """
        Gets a DateTime object for the current month, include days in current month after today.
        :param tzinfo: timezone, instance of datetime.tzinfo subclass
        :example DateTime('2012-04-04')
        :return DateTime
        """
        day_next = cls.date_time_this_month(before_now=True, after_now=False, tzinfo=tzinfo)
        return day_next.strftime(pattern)