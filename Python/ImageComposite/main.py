import sys
import os
from PIL import Image
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm

SOURCE_IMAGE = sys.argv[1]
IMAGES_DIR = sys.argv[2]


@dataclass
class ImageAsPixel:
    image: Image
    r: float
    g: float
    b: float


def iterpixels(image: Image.Image) -> tuple[float, float, float]:
    for y in range(image.height):
        for x in range(image.width):
            yield image.getpixel((x, y))


def load_images(images_dir: str) -> list[ImageAsPixel]:
    out = []

    for image_file in tqdm(list(os.listdir(images_dir))):
        image = Image.open(os.path.join(images_dir, image_file))

        r, g, b = zip(*iterpixels(image))

        out.append(ImageAsPixel(
            image=image,
            r=np.mean(r),
            g=np.mean(g),
            b=np.mean(b)
        ))

    return out


def transform_space(images: list[ImageAsPixel]) -> list[ImageAsPixel]:
    max_r, max_g, max_b = 0, 0, 0
    min_r, min_g, min_b = 256, 256, 256

    for image in images:
        max_r = max(max_r, image.r)
        min_r = min(min_r, image.r)

        max_g = max(max_g, image.g)
        min_g = min(min_g, image.g)

        max_b = max(max_b, image.b)
        min_b = min(min_b, image.b)

    range_r, range_g, range_b = max_r - min_r, max_g - min_g, max_b - min_b

    return [
        ImageAsPixel(
            image=iap.image,
            r=(iap.r - min_r)*255/range_r,
            g=(iap.g - min_g)*255/range_g,
            b=(iap.b - min_b)*255/range_b,
        )
        for iap in images
    ]


def closest_image(pixel: tuple[float, float, float], images: list[ImageAsPixel]) -> Image.Image:
    closest = None
    min_dist = 1000
    r, g, b = pixel

    for image in images:
        dist = ((r - image.r)**2 + (g - image.g)**2 + (b - image.b)**2)**.5
        if dist < min_dist:
            min_dist = dist
            closest = image

    return closest.image


def make_composite(src: Image.Image, images: list[ImageAsPixel], size: int = 32) -> Image.Image:
    out = Image.new(mode="RGB", size=(src.width*size, src.height*size))
    for x in tqdm(list(range(src.width))):
        for y in range(src.height):
            pixel = src.getpixel((x, y))

            closest = closest_image(pixel, images)

            out.paste(closest, (x*size, y*size, (x+1)*size, (y+1)*size))

    return out


if __name__ == "__main__":
    print("Loading images")
    images = transform_space(load_images(IMAGES_DIR))

    print("Opening")
    src = Image.open(SOURCE_IMAGE)
    src = src.resize((256, 256))

    print("Converting")
    composite = make_composite(src, images)
    composite.save("out.png")
