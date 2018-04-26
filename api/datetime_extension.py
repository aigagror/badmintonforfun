from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)
ONE = timedelta(1)
HOUR = timedelta(hours=1)

# A UTC class.

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

class CST(tzinfo):
    """CST"""

    def utcoffset(self, dt):
        return -6*HOUR

    def tzname(self, dt):
        return "CST"

    def dst(self, dt):
        return ONE

cst = CST()
