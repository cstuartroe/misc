import requests
from bs4 import BeautifulSoup
import json
import datetime
import pdb


def pageid(year):
    return "team" if year > 2020 else "about"


def get_year_dates(year: int):
    uri = (f"https://web.archive.org/__wb/calendarcaptures/2"
           f"?url=https%3A%2F%2Fwww.academia.edu%2F{pageid(year)}&date={year}&groupby=day")

    data = requests.get(uri).json()

    for date_num, _, _ in data["items"]:
        month, day = date_num // 100, date_num % 100
        yield month, day


def get_year_times(year: int):
    for month, date in get_year_dates(year):
        uri = (f"https://web.archive.org/__wb/calendarcaptures/2"
               f"?url=https%3A%2F%2Fwww.academia.edu%2F{pageid(year)}&date={year}{month:02d}{date:02d}")

        data = requests.get(uri).json()

        for time_num, _, _ in data["items"]:
            hour, minute, second = time_num // 10000, (time_num % 10000) // 100, time_num % 100

            yield datetime.datetime(year, month, date, hour, minute, second)


PAGE_SWITCH_DATE = datetime.datetime(2020, 10, 17)
START_YEAR = 2020


def get_all_times():
    for year in range(START_YEAR, 2021):
        for dt in get_year_times(year):
            if dt < PAGE_SWITCH_DATE:
                yield dt

    for year in range(2021, datetime.datetime.now().year + 1):
        yield from get_year_times(year)


def people_names(people_dict):
    for section in people_dict["team"]:
        for p in section["people"]:
            yield p["name"]


class PageFormatError(Exception):
    pass


def get_page_people(dt: datetime.datetime):
    if dt < PAGE_SWITCH_DATE:
        return get_page_people_about(dt)
    else:
        return get_page_people_team(dt)


def get_page_people_about(dt: datetime.datetime):
    uri = (f"https://web.archive.org/web/{dt.strftime('%Y%m%d%H%M%S')}/"
           f"https://www.academia.edu/about")

    res = requests.get(uri)
    soup = BeautifulSoup(res.text, features="html.parser")

    people_section = soup.find("section", {"id": "team"})

    if people_section is None:
        raise PageFormatError("No people section found")

    for w in people_section.find_all("div", {"class": "static-team-member-wrapper"}):
        yield w.img["alt"]


def get_page_people_team(dt: datetime.datetime):
    uri = (f"https://web.archive.org/web/{dt.strftime('%Y%m%d%H%M%S')}/"
           f"https://www.academia.edu/team")

    res = requests.get(uri)
    soup = BeautifulSoup(res.text, features="html.parser")

    people_dict_str = (soup.find("div", "js-react-on-rails-component")
                       ["data-props"])

    people_dict = json.loads(people_dict_str)

    return people_names(people_dict)


FORMAT = "%Y-%m-%d"


def get_epitaphs():
    current_date, current_people = None, None

    for dt in get_all_times():
        if (current_date is not None) and ((dt - current_date) < datetime.timedelta(days=7)):
            continue

        try:
            new_people = set(get_page_people(dt))
        except PageFormatError:
            continue

        if current_date is not None:
            epitaphs = current_people - new_people
            hires = new_people - current_people

            if len(epitaphs) > 0 or len(hires) > 0:
                print(f"left between {current_date.strftime(FORMAT)} and {dt.strftime(FORMAT)}")
                for name in sorted(list(epitaphs)):
                    print(f"    {name}")

                print(f"hired between {current_date.strftime(FORMAT)} and {dt.strftime(FORMAT)}")
                for name in sorted(list(hires)):
                    print(f"    {name}")

                print()

        current_date = dt
        current_people = new_people


if __name__ == "__main__":
    get_epitaphs()

    print("Warning: not all listed departures/hires are genuine; some may be due to name changes")
