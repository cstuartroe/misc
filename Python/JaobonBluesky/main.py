import datetime
import urllib.request
import json
from dataclasses import dataclass


with open("roots.json", "r") as fh:
    ROOTS = json.load(fh)


with open("days.json", "r") as fh:
    DAYS = json.load(fh)


def post(url: str, data: dict[str, str], headers: dict[str, str] = None):
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(
        url,
        data=params,
        headers = {
            'content-type': 'application/json',
            **(headers or {}),
        },
    )
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf8'))


FIRST_DAY = datetime.date(2025, 2, 4)


@dataclass
class PostSegment:
    text: str
    href: str | None = None
    tag: str | None = None


BLUESKY_LENGTH_LIMIT = 300


@dataclass
class PostData:
    text: str
    facets: list[dict]

    def __post_init__(self):
        if len(self.text) > BLUESKY_LENGTH_LIMIT:
            raise ValueError(f"Post too long (length is {len(self.text)}, max is {BLUESKY_LENGTH_LIMIT}):\n\n{self.text}")


def facet(facet_type: str, content: dict, start: int, length: int):
    return {
      "index": {
        "byteStart": start,
        "byteEnd": start + length,
      },
      "features": [
        {
          "$type": f"app.bsky.richtext.facet#{facet_type}",
          **content,
        }
      ]
    }


def stitch_segments(segments: list[PostSegment]) -> PostData:
    post_text = ""
    facets = []

    for segment in segments:
        start = len(post_text.encode())
        length = len(segment.text.encode())

        if segment.href is not None:
            facets.append(facet("link",{"uri": segment.href}, start, length))
        if segment.tag is not None:
            facets.append(facet("tag", {"tag": segment.tag}, start, length))

        post_text += segment.text

    return PostData(
        text=post_text,
        facets=facets,
    )


def post_data(date: datetime.date) -> PostData:
    day_of_year = (date - FIRST_DAY).days
    daily_root = ROOTS[day_of_year]

    segments: list[PostSegment] = [
        PostSegment(f"Today is "),
        PostSegment(
            DAYS[day_of_year],
            href="http://celestial-cards.conorstuartroe.com/calendar/birthday?back=5&forward=5&date=" + date.strftime("%Y-%m-%d"),
        ),
        PostSegment(".\n\n"),
        PostSegment("The Jaobon root for the day is "),
        PostSegment(
            f"{daily_root["root"]["CJK"]} {daily_root["root"]["syllable"]}",
            href=f"http://jaobon.conorstuartroe.com/roots#{daily_root["root"]["syllable"]}",
        ),
        PostSegment(f" ({", ".join(daily_root["root"]["pos"])}) \"{daily_root["root"]["definition"]}\"\n\n"),
        PostSegment(daily_root["example_sentence"]["Jaobon"]["CJK"] + "\n"),
        PostSegment(daily_root["example_sentence"]["Jaobon"]["roman"] + "\n"),
        PostSegment(daily_root["example_sentence"]["English"] + "\n\n"),
        PostSegment("#conlang", tag="conlang"),
    ]

    return stitch_segments(segments)


def preview_all_posts():
    for i in range(len(ROOTS)):
        if ROOTS[i] is None:
            continue

        d = FIRST_DAY + datetime.timedelta(days=i)
        print(f"({d.strftime("%Y-%m-%d")})")
        data = post_data(d)
        print(data.text)
        # print(json.dumps(data.facets, indent=2))
        print("----------")


with open("credentials.json", "r") as fh:
    CREDENTIALS = json.load(fh)


def send_post():
    session = post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        data=CREDENTIALS,
    )
    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    data = post_data(datetime.date.today())
    post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        data={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": data.text,
                "createdAt": now,
                "langs": ["en-US"],
                "facets": data.facets,
            },
        },
    )


def lambda_handler(event, context):
    send_post()
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }


# print(lambda_handler(None, None))
preview_all_posts()
