import string


class Calender:
    def __init__(self, days_year: int, days_month: int, days_week: int):
        if not (days_year > 0 and days_month > 0 and days_week > 0):
            raise ValueError('all arguments must be natural number')

        if days_week > 26:
            raise ValueError('days_week must be a integer from 1 to 26')

        if not (days_year >= days_month >= days_week):
            raise ValueError('invalid argument order')

        self._days_year = days_year
        self._days_month = days_month
        self._days_week = days_week

        self._month = int(days_year / days_month)
        self._leap_diff = days_year % days_month
        self._leap = 0 if self._leap_diff == 0 else int(days_month / self._leap_diff)

    def calc(self, date_string: str) -> str:
        year, month, day = map(int, date_string.split('-'))

        if not (year > 0 and month > 0 and day > 0):
            raise ValueError('all arguments must be natural number')

        if day > self._days_month:
            raise ValueError('invalid day: maximum day exceeded')

        if month > self._month + 1:
            raise ValueError('invalid month: maximum month exceeded')

        year -= 1
        month -= 1
        leap_years = []

        if self._leap == 0:
            if self._month == month:
                raise ValueError('invalid month: there is no leap year')

            days = year * self._days_year + month * self._days_month + day
        else:
            days = 0
            stock = 0

            for _ in range(year):
                days += self._days_year - self._leap_diff

                stock += self._leap_diff

                if stock >= self._days_month:
                    stock -= self._days_month
                    days += self._days_month
                    leap_years.append(_)

            stock += self._leap_diff
            if stock >= self._days_month:
                leap_years.append(year)

            if month + 1 > self._month and year not in leap_years:
                raise ValueError('invalid month: this year is not leap year')

            days += month * self._days_month + day

        return string.ascii_uppercase[(days - 1) % self._days_week]
