from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math

from just_chords import chords_with_dissonance, closest_approximation, get_chord_name, cents, MAJOR_EDOS, euler_dissonance, vogel_dissonance


CORBERT_FILENAME = "../../../storyweb/static/fonts/Corbert-Regular.ttf"


COLORS = {
    "light blue": "#1bb9d7",
    "grass green": "#7ed957",
    "orange": "#ff914d",
    "yellow": "#ffde59",
}


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


DISSONANCE_FUNCTION_NAMES = {
    euler_dissonance: "Euler",
    vogel_dissonance: "Vogel",
}


CHORD_SIZE_NAMES = [
    None,
    None,
    "interval",
    "trichord",
    "tetrachord",
]


def intervals_infographic(notes=2, dissonance_function=euler_dissonance, min_to_describe=30):
    c_w_d = chords_with_dissonance(notes, dissonance_function=dissonance_function)

    _, max_dissonance = c_w_d[min_to_describe]
    num_to_describe = min_to_describe
    while c_w_d[num_to_describe][1] == max_dissonance:
        num_to_describe += 1
    intervals_to_describe = c_w_d[:num_to_describe]

    bumper_height = 80
    header_height = 300
    interval_block_height = 250 if (notes == 2) else 100
    image_height = 2*bumper_height + header_height + (interval_block_height * len(intervals_to_describe))

    image_width = 1200
    margin_width = 100

    img = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    corbert32 = ImageFont.truetype(CORBERT_FILENAME, 32)
    corbert48 = ImageFont.truetype(CORBERT_FILENAME, 48)
    corbert64 = ImageFont.truetype(CORBERT_FILENAME, 64)

    # bumpers

    draw.rectangle([0, 0, image_width, bumper_height], fill=COLORS["light blue"])
    draw.rectangle([0, image_height - bumper_height, image_width, image_height], fill=COLORS["light blue"])

    # header

    draw.text(
        xy=(image_width // 2, bumper_height + 20),
        anchor='ma',
        text=f"The {len(intervals_to_describe)} most consonant {CHORD_SIZE_NAMES[notes]}s",
        fill=(0, 0, 0),
        font=corbert64,
    )

    draw.multiline_text(
        xy=(image_width // 2, bumper_height + 110),
        anchor='ma',
        text=f"and their approximation error (in cents)\nin selected equal temperament tunings",
        fill=(0, 0, 0),
        font=corbert32,
        align='left',
    )

    # intervals info

    for i, (chord, dissonance) in enumerate(intervals_to_describe):
        block_y = bumper_height + header_height + (interval_block_height * i)

        # line

        circle_radius = 6

        draw.line(
            xy=[
                margin_width + circle_radius,
                block_y,
                image_width - margin_width - circle_radius,
                block_y,
            ],
            fill=(0, 0, 0),
            width=2,
        )

        draw.arc(
            xy=[
                margin_width - circle_radius,
                block_y - circle_radius,
                margin_width + circle_radius,
                block_y + circle_radius,
            ],
            start=0,
            end=360,
            fill=(0, 0, 0),
            width=2,
        )

        draw.arc(
            xy=[
                image_width - margin_width - circle_radius,
                block_y - circle_radius,
                image_width - margin_width + circle_radius,
                block_y + circle_radius,
            ],
            start=0,
            end=360,
            fill=(0, 0, 0),
            width=2,
        )

        # first row

        first_row_y = block_y + 0

        draw.text(
            xy=(margin_width, first_row_y),
            anchor='la',
            text=get_chord_name(chord),
            fill=(0, 0, 0),
            font=corbert32,
        )

        draw.text(
            xy=(image_width - margin_width, first_row_y),
            anchor='ra',
            text=f"{DISSONANCE_FUNCTION_NAMES[dissonance_function]} dissonance: {dissonance}",
            fill=(0, 0, 0),
            font=corbert32,
        )

        draw.text(
            xy=(image_width//2, first_row_y),
            anchor='ma',
            text=' : '.join(map(str, (chord[1], chord[0]) if len(chord) == 2 else chord)),
            fill=(0, 0, 0),
            font=corbert48,
        )

        if notes > 2:
            continue

        # second row

        second_row_y = first_row_y + 80

        draw.text(
            xy=(image_width // 2, second_row_y),
            anchor='ma',
            text=', '.join(map(str, [cents(tone/chord[0]) for tone in chord[1:]])) + " cents",
            fill=(0, 0, 0),
            font=corbert32,
        )

        # third + fourth row

        third_row_y = second_row_y + 60

        edo_spacing = 150

        for i, edo_steps in enumerate(MAJOR_EDOS):
            edo_x = (image_width // 2) + (edo_spacing * (i - len(MAJOR_EDOS)/2 + .5))

            draw.text(
                xy=(edo_x, third_row_y),
                anchor='ma',
                text=f"{edo_steps}EDO",
                fill=(0, 0, 0),
                font=corbert32,
            )

            fourth_row_y = third_row_y + 35

            for tone in chord[1:]:
                error = closest_approximation(tone/chord[0], edo_steps)
                if math.fabs(error) < 3.0:
                    color = COLORS["grass green"]
                elif math.fabs(error) < 10.0:
                    color = COLORS["yellow"]
                else:
                    color = COLORS["orange"]

                draw.text(
                    xy=(edo_x, fourth_row_y),
                    anchor='ma',
                    text=f"{'+' if error > 0 else ''}{error}",
                    fill=hex_to_rgb(color),
                    font=corbert48,
                )

                fourth_row_y += 50

    img.save(f"{CHORD_SIZE_NAMES[notes]}s.png")


if __name__ == "__main__":
    intervals_infographic(2)
    intervals_infographic(3)
    intervals_infographic(4)