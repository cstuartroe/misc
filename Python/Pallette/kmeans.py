from sklearn.cluster import KMeans
from PIL import Image
import sys

Color = tuple[int, int, int]


def kmeans_posterize(img: Image) -> Image:
    img = img.convert("RGB")

    kmeans = KMeans(n_clusters=16, n_init=1, max_iter=20)

    pixels = [
        img.getpixel((x, y))
        for y in range(img.height)
        for x in range(img.width)
    ]

    pixel_labels = kmeans.fit_predict(pixels)

    cluster_centers = [
        tuple(map(round, cc))
        for cc in kmeans.cluster_centers_
    ]

    for x in range(img.width):
        for y in range(img.height):
            img.putpixel((x, y), cluster_centers[pixel_labels[x + y*img.width]])

    return img


if __name__ == "__main__":
    image_filename = sys.argv[1]

    img = Image.open(image_filename)

    poster = kmeans_posterize(img)

    poster.save(image_filename + ".png")

