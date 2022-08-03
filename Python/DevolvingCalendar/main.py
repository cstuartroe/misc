import ephem
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def nearest_weekday(dt: datetime, weekday=6):
    before = datetime(dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=dt.tzinfo)
    after = before + timedelta(days=1)

    while before.weekday() != weekday:
        before -= timedelta(days=1)

    while after.weekday() != weekday:
        after += timedelta(days=1)

    if (dt - before) < (after - dt):
        return before
    else:
        return after


def get_party_start(year: int, count_forward=True):
    if count_forward:
        summer_solstice = ephem.next_summer_solstice(f"{year}/1/1")
        fm1 = ephem.next_full_moon(summer_solstice)
        fm2 = ephem.next_full_moon(fm1)
        fm3 = ephem.next_full_moon(fm2)

    else:
        autumnal_equinox = ephem.next_autumnal_equinox(f"{year}/1/1")
        fm3 = ephem.previous_full_moon(autumnal_equinox)

    dt = ephem.to_timezone(fm3, ZoneInfo('US/Eastern'))

    return nearest_weekday(dt) - timedelta(hours=6)


if __name__ == "__main__":
    for year in range(2022, 2031):
        party_start = get_party_start(year)

        print(party_start.strftime("%A, %d %b %Y"))
