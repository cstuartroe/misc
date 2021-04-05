from PIL import Image, ImageDraw

max_x = 200
max_y = 200
block_width = 10


for modulus in range(3, 20):
    for v in range(modulus):

        img = Image.new('RGB', (block_width*(max_x + 1), block_width*(max_y + 1)), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        for x in range(max_x + 1):
            for y in range(max_y + 1):
                img_x = x*block_width
                img_y = y*block_width
                draw.rectangle(
                    xy=[img_x, img_y, img_x + block_width, img_y + block_width],
                    fill=("white" if (x^y) % modulus == v else "black")
                )

        img.save(f"alien_art_{modulus}_{v}.png")
        print(modulus, v)
