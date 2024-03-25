import json
import os
from dataclasses import dataclass

from tqdm import tqdm
import requests


HEADERS = {
    # Just grab these from Chrome devtools
}


ITEM_LIST_PARAMS = {
    # Just grab these from Chrome devtools
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
        }


@dataclass
class Video:
    id: str
    author: Author
    description: str
    create_time: int
    download_link: str
    duration: int

    def download(self):
        filepath = f"videos/{self.id}.mp4"
        if os.path.exists(filepath):
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
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            id=data["id"],
            author=data["author"], # TODO
            description=data["description"],
            create_time=data["create_time"],
            download_link="",
            duration=data["duration"],
        )


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
    )

    return Video(
        id=data["id"],
        author=author,
        description=data["desc"],
        create_time=data["createTime"],
        download_link=data["video"]["downloadAddr"],
        duration=data["video"]["duration"],
    )


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

        data = json.loads(res.text)

        video_json += data["itemList"]
        cursor = data["cursor"]
        has_more = data["hasMore"]

    videos = [
        video_json_to_dataclass(v)
        for v in video_json
    ]

    print(f"{len(videos)} videos liked.")

    authors = list(set(
        video.author
        for video in videos
    ))
    authors.sort(key=lambda author: author.unique_id)

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
    with open("videos.json", "r") as fh:
        videos_json = json.load(fh)

    videos = [
        Video.from_json(data)
        for data in videos_json
    ]

    total_video_length = 0
    longest = videos[0]
    shortest = videos[0]
    for video in videos:
        total_video_length += video.duration
        if video.duration > longest.duration:
            longest = video
        if video.duration < shortest.duration:
            shortest = video

    print(f"Total video length: {total_video_length//3600}:{(total_video_length%3600)//60}:{total_video_length%60}")
    print(f"Shortest video: {shortest.id} at {shortest.duration} seconds")
    print(f"Longest video: {longest.id} at {longest.duration} seconds")


# get_videos()
print_stats()
