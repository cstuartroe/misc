import sys
from colorsys import hls_to_rgb, rgb_to_hls
from PIL import Image, ImageDraw
from tqdm import tqdm
from random import randrange


def gen_colors16():
    colors = set()

    for h in range(6):
        for l in range(4):
            for s in range(2):
                rgb = hls_to_rgb(h/6, l/3, s)
                colors.add(tuple(round(n*255) for n in rgb))

    return sorted(colors)


def pallette16(colors, square_width=20):
    p = Image.new("RGB", (square_width * 4, square_width * 4))
    d = ImageDraw.Draw(p)

    for i in range(4):
        for j in range(4):
            color = colors[i*4 + j]

            d.rectangle(
                (
                    square_width * i,
                    square_width * j,
                    square_width * (i+1),
                    square_width * (j+1),
                ),
                fill=color,
            )

    p.save('pallette.png')


def color_distance(rgb1, rgb2):
    return sum(abs(n1 - n2) for n1, n2 in zip(rgb1, rgb2))**.5


def approximate_closeness(initial_color, colors):
    closest_color = None
    shortest_distance = 10**5

    for color in colors:
        d = color_distance(initial_color, color)
        if d < shortest_distance:
            shortest_distance = d
            closest_color = color

    return closest_color


def approximate_hsl(initial_color, increase_saturation=.5):
    r, g, b = initial_color

    r = r / 255
    g = g / 255
    b = b / 255

    h, l, s = rgb_to_hls(r, g, b)

    h = (round(h * 6) % 6) / 6
    l = round(l * 3) / 3
    s = round(s**(1 - increase_saturation))

    r, g, b = hls_to_rgb(h, l, s)

    return round(r * 255), round(g * 255), round(b * 255)


def cast_to_colorspace(image_filename, colors):
    f = Image.open(image_filename).convert("RGB")

    for x in tqdm(list(range(f.width))):
        for y in range(f.height):
            initial_color = f.getpixel((x, y))
            closest_color = approximate_hsl(initial_color, increase_saturation=.3)

            f.putpixel((x, y), closest_color)

    f.save(image_filename + ".png")


if __name__ == "__main__":
    pallette16(gen_colors16())

    cast_to_colorspace(sys.argv[1], gen_colors16())
