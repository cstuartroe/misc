from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math

from just_chords import chords_with_dissonance, closest_approximation, get_chord_name, cents, MAJOR_EDOS, euler_dissonance, vogel_dissonance, gill_purves_dissonance


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
    gill_purves_dissonance: "Gill-Purves",
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


def flatten(l):
    if type(l) is list:
        out = []
        for e in l:
            out += flatten(e)
        return out
    else:
        return [l]


def launchpad_infographic(edo_steps=31, diag_steps=(8, 9, 10, 11,)):
    boards = []

    for down in range(1, max(diag_steps)):
        for right in range(down+1, max(diag_steps)):
            if math.gcd(down, right) == 1 and (down + right in diag_steps):
                boards.append([
                    [
                        right*x + down*y
                        for x in range(8)
                    ]
                    for y in range(8)
                ])

    boards.sort(key=lambda board: board[0][1] + board[1][0])

    block_size = 30
    margin = 30
    diatonic_degrees = {
        12: [0, 2, 4, 5, 7, 9, 11],
        19: [0, 3, 6, 8, 11, 14, 17],
        31: [0, 5, 10, 13, 18, 23, 28],
    }[edo_steps]

    image_width = block_size*8 + margin*2
    image_height = (block_size*8 + margin)*len(boards) + margin

    img = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    corbert32 = ImageFont.truetype(CORBERT_FILENAME, 16)

    for i, board in enumerate(boards):
        top = (block_size*8 + margin)*i + margin

        for y, row in enumerate(board):
            for x, deg in enumerate(row):
                bgcolor = "#ffffff" if (deg % edo_steps) in diatonic_degrees else "#cccccc"
                text_color = "#000000" if len([e for e in flatten(board) if e == deg]) == 1 else "#ff0000"

                draw.rectangle(
                    xy=[
                        margin + (block_size * x),
                        top + (block_size * y),
                        margin + (block_size * (x + 1)),
                        top + (block_size * (y + 1)),
                    ],
                    fill=hex_to_rgb(bgcolor)
                )

                draw.text(
                    xy=(margin + (block_size * (x + .5)), top + (block_size * (y + .5))),
                    anchor='mm',
                    text=str(deg % edo_steps),
                    fill=hex_to_rgb(text_color),
                    font=corbert32,
                )

    img.save(f"launchpad_{edo_steps}.png")


def cents_bar_infographic(edo_steps, total_cents=1200):
    bar_width = 2400
    side_padding = 200
    image_height = 300
    vertical_line_height = 80
    bar_top = 150
    bottom_padding = 50

    img = Image.new('RGBA', (bar_width + 2*side_padding, image_height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    num_steps = edo_steps if type(edo_steps) == int else len(edo_steps)
    corbert_scaled = ImageFont.truetype(CORBERT_FILENAME, bar_width//int(num_steps**.5 * 12))

    draw.rectangle(
        xy=[
            side_padding,
            bar_top,
            bar_width + side_padding,
            image_height - bottom_padding,
        ],
        fill=(0, 0, 0, 0),
        outline="white",
        width=5,
    )

    if type(edo_steps) == int:
        intervals = [step/total_cents for step in range(edo_steps + 1)]
    else:
        intervals = [math.log2(r) for r in edo_steps]

    for interval in intervals:
        cents = round(interval*total_cents)
        x = side_padding + round(interval*bar_width)
        draw.text(
            xy=(x, bar_top - (vertical_line_height // 2)),
            anchor="md",
            text=str(cents),
            fill="white",
            font=corbert_scaled,
        )
        draw.line(
            xy=[
                x,
                bar_top - (vertical_line_height // 2),
                x,
                bar_top + (vertical_line_height // 2),
            ],
            fill="white",
            width=5,
        )

    img.save(f"cents_bar_{edo_steps}_steps_{total_cents}_cents.png")


if __name__ == "__main__":
    # intervals_infographic(2, dissonance_function=gill_purves_dissonance)
    # intervals_infographic(3, dissonance_function=gill_purves_dissonance)
    # intervals_infographic(4, dissonance_function=gill_purves_dissonance)
    # launchpad_infographic(12, (2, 3, 4, 5, 6, 7,))
    # launchpad_infographic(19, (2, 3, 4, 5, 6, 7, 8, 9, 10, 11,))
    # launchpad_infographic(31, (5,))
    cents_bar_infographic(12)
    cents_bar_infographic(17)
    cents_bar_infographic(19)
    cents_bar_infographic(22)
    cents_bar_infographic(24)
    cents_bar_infographic(31)
    cents_bar_infographic(13, 1800)
    cents_bar_infographic([1, 9/8, 7/6, 5/4, 4/3, 7/5, 3/2, 13/8, 7/4, 15/8, 2])
