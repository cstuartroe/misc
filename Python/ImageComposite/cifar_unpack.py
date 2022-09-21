import pickle
import sys
import os
from PIL import Image
from tqdm import tqdm


CIFAR_DIR = sys.argv[1]
DEST_DIR = "cifar"

LABELS = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def load_images(batch_filename):
    with open(batch_filename, 'rb') as fo:
        d = pickle.load(fo, encoding='bytes')

    filenames = [
        f.decode('utf-8')
        for f in d[b'filenames']
    ]
    labels = d[b'labels']
    data = d[b'data']

    for i in tqdm(list(range(len(filenames)))):
        pixels = data[i, :]

        image = Image.new(mode="RGB", size=(32, 32), color="black")

        for x in range(32):
            for y in range(32):
                index = x + y*32
                rgb = (pixels[index], pixels[index+1024], pixels[index+2048])
                image.putpixel((x, y), rgb)

        filepath = os.path.join(DEST_DIR, LABELS[labels[i]], filenames[i])

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as fh:
            image.save(fh)


CIFAR_FILES = [
    *(f"data_batch_{i}" for i in range(1, 6)),
    "test_batch",
]

if __name__ == "__main__":
    for filename in CIFAR_FILES:
        print("Unpacking", filename)
        load_images(os.path.join(CIFAR_DIR, filename))
