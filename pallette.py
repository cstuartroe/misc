from PIL import Image, ImageDraw

def pallette(increments,square_width):
    out = Image.new("RGB",(square_width*(increments**2),square_width*increments))
    d = ImageDraw.Draw(out)
    
    for i in range(increments):
        r = round(i*255/(increments-1))
        for j in range(increments):
            g = round(j*255/(increments-1))
            for k in range(increments):
                b = round(k*255/(increments-1))

                d.rectangle([(square_width*increments*i)+(square_width*j),square_width*k,
                             (square_width*increments*i)+(square_width*(j+1)),square_width*(k+1)],
                            fill = (r,g,b))
    return out

p = pallette(5,20)
p.save('pallette.png')
