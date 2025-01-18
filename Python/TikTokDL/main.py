import datetime
import json
import os
import brotli
from dataclasses import dataclass

from tqdm import tqdm
import requests


HEADERS = {
    # ":authority": "www.tiktok.com",
    # ":method": "GET",
    # ":path": "/api/user/following/request/list/?WebIdLastTime=1736617325&aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28iPhone%3B%20CPU%20iPhone%20OS%2016_6%20like%20Mac%20OS%20X%29%20AppleWebKit%2F605.1.15%20%28KHTML%2C%20like%20Gecko%29%20Version%2F16.6%20Mobile%2F15E148%20Safari%2F604.1&channel=tiktok_web&cookie_enabled=true&count=20&data_collection_enabled=true&device_id=7458714572704400927&device_platform=web_mobile&focus_state=false&from_page=fyp&history_len=2&is_fullscreen=false&is_page_visible=true&max_time=0&odinId=6812009848424563718&os=ios&priority_region=US&referer=&region=US&screen_height=896&screen_width=414&tz_name=America%2FNew_York&user_id=6812009848424563718&user_is_login=true&verifyFp=verify_lzosocv0_CENgYNEl_tern_4GP3_Bxiq_Uji2wJRIQJWZ&webcast_language=en&msToken=BblIrJI5t4yOh1kLu9mas9v5hQW5AqHQZA9-WPKPw8m9o1pNWtNYaPgdyxoQg_cB3fh50U_nXsutdFuPx4j1pQbzxfzJgVBfQ_m61COCtjT4Fp-WC3rCnwbfYtIGtgKrqGe6leVQpZu4fO1HJF5Plkw=&X-Bogus=DFSzswVYj4JANGA-tpV8fELNKBO-&_signature=_02B4Z6wo00001X619VgAAIDCLErVQk9HI7l-tfHAADgrf5",
    # ":scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9,nl;q=0.8,ar;q=0.7",
    "cookie": "tt_csrf_token=hYcgrfwQ-uf_10umVakyLeQ6Rh4wRJFKu22A; s_v_web_id=verify_lzosocv0_CENgYNEl_tern_4GP3_Bxiq_Uji2wJRIQJWZ; csrf_session_id=39d053a62ed840469b018b115f58e62e; _ttp=2rSRIvSpZdyN9pmQDf910OQccbl; tt_chain_token=6/BWx3xzItgYdQtIw7OgGw==; tiktok_webapp_theme=light; passport_csrf_token=a706194331919ed2564198bdd029b333; passport_csrf_token_default=a706194331919ed2564198bdd029b333; multi_sids=6812009848424563718%3A36a1fd9402f7b95b240fda12a46fe2cc; cmpl_token=AgQQAPPzF-RO0o638Hod_d0__eM0UWSMf53ZYNo98g; passport_auth_status=874f6d1fe37c799271e76e28f4c16ac2%2C; passport_auth_status_ss=874f6d1fe37c799271e76e28f4c16ac2%2C; uid_tt=513441d43861be0beef5b03c64fb9358e5582832bc3d3746d3902b487cc0154b; uid_tt_ss=513441d43861be0beef5b03c64fb9358e5582832bc3d3746d3902b487cc0154b; sid_tt=36a1fd9402f7b95b240fda12a46fe2cc; sessionid=36a1fd9402f7b95b240fda12a46fe2cc; sessionid_ss=36a1fd9402f7b95b240fda12a46fe2cc; store-idc=useast5; store-country-code=us; store-country-code-src=uid; tt-target-idc=useast8; tt-target-idc-sign=z8FmzsVBIEA3rQU_pn3V6OWzrrS5JFNrH-vi77Iid_av2t6zbzX9QwsKFjIWonB0GxMZE02ZONiTcWqMgFmeSTZvsD-k4Ptonb9jLzyNuEoxEXvGIqVWFEf1aFtUruPJsENwnYwKqFBQ8Q9V9q6zJU4caXAUrppsURBYpML74HbtpoULfcrhu2IFUElMGaj17raAKlsPckgJaIYtAoOJ5iFYL0VSGL66j2-BNz1SnTssdlrO1_Rc0BFVLnUnrZW-vu5Irz1rwK3o8P4aOC-VVVvF0ICyV4zQQVzmBtPTxmjZf0dpuyEE-EcnHm3CIwHt5IjOFHtCcrW2jm_pr-WM78sJuXUtRYMHsDQoDf86JzwsKA6M-YiHwHUv-6aKv2CMtPSiq_X90EiLxUbnFufSGIWHV83q0XBIHPLDnPmJLODibDpTgO6hncKQ3TlGmGatOmPj4izkKjGXhP5PBxkbRUs1IS4SVebIlhvE9v3jxYMqOCJXGCRikXTkwZ2OFjcW; last_login_method=google; tiktok_webapp_theme_source=system; sid_guard=36a1fd9402f7b95b240fda12a46fe2cc%7C1736617355%7C15551997%7CThu%2C+10-Jul-2025+17%3A42%3A32+GMT; sid_ucp_v1=1.0.0-KGQ3NzIxMGEwM2JiZmY1NzA2ODg2NTQ2MDVhZjdmOGNjNjA2OWQxMWIKGQiGiLyu2dvHxF4Qi9uKvAYYsws4CEASSAQQBBoHdXNlYXN0OCIgMzZhMWZkOTQwMmY3Yjk1YjI0MGZkYTEyYTQ2ZmUyY2M; ssid_ucp_v1=1.0.0-KGQ3NzIxMGEwM2JiZmY1NzA2ODg2NTQ2MDVhZjdmOGNjNjA2OWQxMWIKGQiGiLyu2dvHxF4Qi9uKvAYYsws4CEASSAQQBBoHdXNlYXN0OCIgMzZhMWZkOTQwMmY3Yjk1YjI0MGZkYTEyYTQ2ZmUyY2M; odin_tt=b231760254dc0806ce6e4f393cf22f2955246e0e3a6e6c3624c57fd4eacfc64054b77eaba0f4934fe1bf66a147b554a5c01be5a5d0471ae0821d74289d36526c8aa32c70bf0c54e7028fb8f13bbcab14; delay_guest_mode_vid=5; cookie-consent={%22optional%22:true%2C%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22reddit%22:true%2C%22hubspot%22:true%2C%22version%22:%22v10%22}; ak_bmsc=2E703C6CF0AB167EEBF0942724948F6D~000000000000000000000000000000~YAAQC+M+F5LWAHKUAQAAqyMddhoNLb8nxE3stDHDhHEQGKvQquOQoworfrRP7wIfR4NjwaUlifid0w64D7A62T50Tf/ZfcRaMGWM+gkS+d2/UphxhKgvDWfc2c4QdgBCThPb6N6D/S3nHhBc1vxiBB6k4JW8oEKs1sKDGVTJp1rTYNGpmzScsPRMKT3n1g+X54gk4Upk6oHCRuRN5Xt2R3/nTSI0yxUwDg7EfxzdSlDePPQ2mcJ4MDk+VKvbKquR5rIzJWKvJDHqRFkFYHeCC6cxx+O0jVQIDI7DEm59U3zuZ1CSbWlS/NZpkhu/VEXzxDE63mu/Kc6IYC9UaNUDakhkq/rRY6WKdM7zep81BwVx1fSvfWXX/jnn30PZ4LHRBD/Za3ky8f3RmS4=; ttwid=1%7Cskot1lOgVsCTeG8ETJQ4xGiBzc7xeveLxV4AhzA6rzc%7C1737148409%7C2b8d0f69aee74e267882c735c0d56b49a88ded8f13d6dec81dbb590c3fea566b; passport_fe_beating_status=true; msToken=BblIrJI5t4yOh1kLu9mas9v5hQW5AqHQZA9-WPKPw8m9o1pNWtNYaPgdyxoQg_cB3fh50U_nXsutdFuPx4j1pQbzxfzJgVBfQ_m61COCtjT4Fp-WC3rCnwbfYtIGtgKrqGe6leVQpZu4fO1HJF5Plkw=; msToken=0cxWZD0DBMHgn0BayroypETUaJwLfQc4JhHVPdRHcuf8ZjGv_A17hz15hWYSQSooAC-mga_EskSdEcVcDCEAO-dsEM8_u0lZb5lEKuNqclxHTff7mkcL-TD9A_FbWdhYbU2mzwk2zXNkzD766oS1eZY=; perf_feed_cache={%22expireTimestamp%22:1737320400000%2C%22itemIds%22:[%227460585025621216530%22%2C%227460892887203466526%22%2C%227460625976280534315%22]}; bm_sv=20CA800A6957A4952CB72A788A4507C6~YAAQGOM+F2HN52+UAQAApzkddhqZAlqedWx7t+eRmzAL9ESNS+auvaipU5dpq7Bfpk0ncZwR89IgICQrriLHfObS+rqUwdaV+q78G9yQDX4Z+jMYhxpM7azv6r9zWAcD0ma1JFwmSVc9v8im+lwW7ild/GWj93HS4MazeVF1bNljAcHDZTWrHMumd+t4MPxGzzBz2BD+3cC/2YoGu8ngx1Gpr8C0KZalzeUG71W1T7mnMbGnTgMHNNQh/0ePdIN3~1",
    "dnt": "1",
    "priority": "u=1, i",
    "referer": "https://www.tiktok.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
}


ITEM_LIST_PARAMS = {
    "WebIdLastTime": "1736617325",
    "aid": "1988",
    "app_language": "en",
    "app_name": "tiktok_web",
    "browser_language": "en-US",
    "browser_name": "Mozilla",
    "browser_online": "true",
    "browser_platform": "MacIntel",
    "browser_version": "5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36",
    "channel": "tiktok_web",
    "cookie_enabled": "true",
    "count": "35",
    "coverFormat": "2",
    "data_collection_enabled": "true",
    "device_id": "7458714572704400927",
    "device_platform": "web_pc",
    "focus_state": "true",
    "history_len": "3",
    "is_fullscreen": "false",
    "is_page_visible": "true",
    "language": "nl-NL",
    "odinId": "6812009848424563718",
    "os": "mac",
    "priority_region": "US",
    "referer: "","
    "region": "US",
    "screen_height": "1117",
    "screen_width": "1728",
    "secUid": "MS4wLjABAAAAIFiDqa2Yj_WbpyS5VJ6BV1eM3Q4jnTfZy95NJ82rWkQ5YJ2KNZTHAP0WH9fThjqI",
    "tz_name": "America%2FNew_York",
    "user_is_login": "true",
    "verifyFp": "verify_lzosocv0_CENgYNEl_tern_4GP3_Bxiq_Uji2wJRIQJWZ",
    "webcast_language": "en",
    "msToken": "BblIrJI5t4yOh1kLu9mas9v5hQW5AqHQZA9-WPKPw8m9o1pNWtNYaPgdyxoQg_cB3fh50U_nXsutdFuPx4j1pQbzxfzJgVBfQ_m61COCtjT4Fp-WC3rCnwbfYtIGtgKrqGe6leVQpZu4fO1HJF5Plkw=",
    "X-Bogus": "DFSzswSO9L0ANy35tpV0XjLNKBYP",
    "_signature": "_02B4Z6wo0000107Gm3gAAIDAHDm7YpnW0WdOxp.AALRGfe",
}


@dataclass
class Author:
    id: str
    unique_id: str
    nickname: str
    signature: str
    avatar_link: str
    verified: bool
    followers: int
    following: int
    video_count: int
    deleted: bool

    def __hash__(self):
        return hash(self.unique_id)

    def __eq__(self, other):
        return self.unique_id == other.unique_id

    def download_avatar(self):
        filepath = f"avatars/{self.unique_id}.jpg"
        if os.path.exists(filepath):
            return

        res = requests.get(
            self.avatar_link,
            headers=HEADERS,
        )

        ct = res.headers["Content-Type"]
        if ct != "image/jpeg":
            raise ValueError(f"Unknown image format: {ct}")

        with open(filepath, "wb") as fh:
            fh.write(res.content)

    def to_json(self):
        return {
            "id": self.id,
            "unique_id": self.unique_id,
            "nickname": self.nickname,
            "signature": self.signature,
            # skip avatar link
            "verified": self.verified,
            "followers": self.followers,
            "following": self.following,
            "video_count": self.video_count,
            "deleted": self.deleted,
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data["id"],
            unique_id=data["unique_id"],
            nickname=data["nickname"],
            signature=data["signature"],
            avatar_link=None,
            verified=data["verified"],
            followers=data["followers"],
            following=data["following"],
            video_count=data["video_count"],
            deleted=data["deleted"],
        )


@dataclass
class Video:
    id: str
    author: Author
    description: str
    create_time: int
    download_link: str
    duration: int
    deleted: bool

    def download(self):
        filepath = f"videos/{self.id}.mp4"
        if os.path.exists(filepath):
            return

        unofficial_filepath = f"videos/unofficial/{self.id}.mp4"
        if os.path.exists(unofficial_filepath):
            return

        if self.download_link is None or len(self.download_link) == 0:
            print("Video needs to be manually downloaded:")
            print(f"https://www.tiktok.com/@{self.author.unique_id}/video/{self.id}")
            return

        res = requests.get(
            self.download_link,
            headers=HEADERS,
        )

        ct = res.headers["Content-Type"]
        if ct != "video/mp4":
            raise ValueError(f"Unknown video format: {ct}")

        with open(filepath, "wb") as fh:
            fh.write(res.content)

    def to_json(self):
        return {
            "id": self.id,
            "author": self.author.unique_id,
            "description": self.description,
            "create_time": self.create_time,
            # skip download link
            "duration": self.duration,
            "deleted": self.deleted,
        }

    @classmethod
    def from_json(cls, data, authors_by_unique_id: dict[str, Author]):
        return cls(
            id=data["id"],
            author=authors_by_unique_id[data["author"]], # TODO
            description=data["description"],
            create_time=data["create_time"],
            download_link="",
            duration=data["duration"],
            deleted=data["deleted"],
        )


def download_unofficial(data):
    filename = f"videos/unofficial/{data["id"]}.mp4"

    if os.path.exists(f"videos/unofficial/{data["id"]}.mp4"):
        return True

    if "bitrateInfo" not in data["video"]:
        return False
    print("attempting unofficial download...")
    for bitrate in sorted(data["video"]["bitrateInfo"], key=lambda d: -d["PlayAddr"]["Height"]):
        for url in bitrate["PlayAddr"]["UrlList"]:
            res = requests.get(
                url,
                headers=HEADERS,
            )
            if res.status_code == 200:
                with open(filename, "wb") as fh:
                    fh.write(res.content)
                return True
    return False


def video_json_to_dataclass(data: dict) -> Video:
    author = Author(
        id=data["author"]["id"],
        unique_id=data["author"]["uniqueId"],
        nickname=data["author"]["nickname"],
        signature=data["author"]["signature"],
        avatar_link=data["author"]["avatarLarger"],
        verified=data["author"]["verified"],
        followers=data["authorStats"]["followerCount"],
        following=data["authorStats"]["followingCount"],
        video_count=data["authorStats"]["videoCount"],
        deleted=False,
    )

    if "downloadAddr" not in data["video"]:
        if not download_unofficial(data):
            print(f"Really cannot download https://www.tiktok.com/@{author.unique_id}/video/{data["id"]}")

    return Video(
        id=data["id"],
        author=author,
        description=data["desc"],
        create_time=data["createTime"],
        download_link=data["video"].get("downloadAddr", None),
        duration=data["video"]["duration"],
        deleted=False,
    )


def load_videos():
    with open("authors.json", "r") as fh:
        authors_json = json.load(fh)

    authors_by_unique_id = {
        a["unique_id"]: Author.from_json(a)
        for a in authors_json
    }

    with open("videos.json", "r") as fh:
        videos_json = json.load(fh)

    return [
        Video.from_json(data, authors_by_unique_id)
        for data in videos_json
    ]


def get_videos():
    video_json = []
    cursor = "0"
    has_more = True

    while has_more:
        res = requests.get(
            "https://www.tiktok.com/api/favorite/item_list/",
            params={
                **ITEM_LIST_PARAMS,
                "cursor": cursor,
            },
            headers=HEADERS,
        )

        print(res.status_code)

        data = json.loads(res.text)

        video_json += data["itemList"]
        cursor = data["cursor"]
        has_more = data["hasMore"]

    videos = [
        video_json_to_dataclass(v)
        for v in video_json
    ]

    authors = list(set(
        video.author
        for video in videos
    ))
    authors.sort(key=lambda author: author.unique_id)
    author_by_id = {
        a.id: a
        for a in authors
    }

    new_video_ids = {v.id for v in videos}
    for video in load_videos():
        if video.id not in new_video_ids:
            video.deleted = True
            if video.author.id in author_by_id:
                video.author = author_by_id[video.author.id]
            else:
                print(f"Creator {video.author.unique_id} deleted.")
                video.author.deleted = True
                authors.append(video.author)
            videos.append(video)

    print(f"{len(videos)} videos liked.")

    print(f"{len(authors)} total authors.")

    with open("authors.json", "w") as fh:
        json.dump([a.to_json() for a in authors], fh, indent=2)

    with open("videos.json", "w") as fh:
        json.dump([v.to_json() for v in videos[::-1]], fh, indent=2)

    print("Downloading author avatars...")
    for author in tqdm(authors):
        author.download_avatar()

    print("Downloading videos...")
    for video in tqdm(videos):
        video.download()


def print_stats():
    videos = load_videos()

    total_video_length = 0
    longest = videos[0]
    shortest = videos[0]
    for video in videos:
        total_video_length += video.duration
        if video.duration > longest.duration:
            longest = video
        if video.duration < shortest.duration:
            shortest = video

    print(f"{len(videos)} videos")
    print(f"Total video length: {total_video_length//3600}:{(total_video_length%3600)//60}:{total_video_length%60}")
    print(f"Shortest video: {shortest.id} at {shortest.duration} seconds")
    print(f"Longest video: {longest.id} at {longest.duration} seconds")

    for video in videos:
        if not os.path.exists(f"videos/{video.id}.mp4"):
            print(f"Video does not exist: {video.download_link}")


get_videos()
# print_stats()
