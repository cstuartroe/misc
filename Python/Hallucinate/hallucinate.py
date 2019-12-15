from PIL import Image
import numpy as np
import imageio
from tqdm import tqdm
from statistics import stdev

#np.random.seed(2020)

def scaled_sigmoid(arr, scale=1):
    s = 1/(1 + np.exp(-arr))
    return (s*scale)


def middlecluster(x):
    # x is in [0, 1)
    return ((2*x-1)**3 + 1)/2


def hsl2rgb(h, s, l):
##    assert(0 <= h and h < 360)
##    assert(0 <= s and s < 360)
##    assert(0 <= l and l < 360)
    s = middlecluster(s/360)
    l = middlecluster(l/360)
    # h = (3*h + 9*np.sin(h/3)) % 360
    
    chroma = (1 - abs(2*l - 1))*s
    x = chroma * (1 - abs((h/60)%2 - 1))
    m = l - chroma/2
    
    if h < 60:
        r, g, b = chroma+m, x+m, m
    elif h < 120:
        r, g, b = x+m, chroma+m, m
    elif h < 180:
        r, g, b = m, chroma+m, x+m
    elif h < 240:
        r, g, b = m, x+m, chroma+m
    elif h < 300:
        r, g, b = x+m, m, chroma+m
    else:
        r, g, b = chroma+m, m, x+m

    return (int(r*255), int(g*255), int(b*255))

def rgb2hex(r, g, b):
##    assert(0 <= r and r < 256)
##    assert(0 <= g and g < 256)
##    assert(0 <= b and b < 256)
    return "#" + hex(r*65536 + g*256 + b)[2:].rjust(6, "0")


def hallucinate_image(sidelength, M1, M2, filename):
    pixels = np.zeros((sidelength, sidelength, 3), dtype=np.uint8)

    for x in range(sidelength):
        for y in range(sidelength):
            features = np.array([
                2*x/sidelength - 1,
                2*y/sidelength - 1,
                (sidelength-x)/sidelength - .5,
                (sidelength-y)/sidelength - .5,
                np.cos((x-sidelength/2)/(sidelength/3)),
                np.cos((y-sidelength/2)/(sidelength/3)),
                x/(y+sidelength/3) - 1.5,
                y/(x+sidelength/3) - 1.5
            ])
            
            #scaled = scaled_sigmoid(features, 255).astype(int)
            hidden = scaled_sigmoid(np.matmul(features, M1))
            h, s, l = scaled_sigmoid(np.matmul(hidden, M2), 359).astype(int)
            r, g, b = hsl2rgb(h, s, l)
            
            pixels[x][y][0] = r
            pixels[x][y][1] = g
            pixels[x][y][2] = b

    img = Image.fromarray(pixels, 'RGB')
    img.save(filename)


HIDDEN_NEURONS = 100
WIDTH1 = 4
WIDTH2 = .3
MUTATE_RATE = .1


def hallucinate_gif(sidelength, frames, filename):    
    M1 = WIDTH1 * np.random.randn(8, HIDDEN_NEURONS)
    M2 = WIDTH2 * np.random.randn(HIDDEN_NEURONS, 3)

    dM1 = WIDTH1 * MUTATE_RATE * np.random.randn(8, HIDDEN_NEURONS)
    dM2 = WIDTH2 * MUTATE_RATE * np.random.randn(HIDDEN_NEURONS, 3)

##    vals = []

    with imageio.get_writer(filename, mode='I') as writer:
        for i in tqdm(range(frames)):
            hallucinate_image(sidelength, M1, M2, "hallucinate.png")
            writer.append_data(imageio.imread("hallucinate.png"))

##            m1 = list(M1.flatten())
##            m2 = list(M2.flatten())
##            vals.append((
##                sum(m1)/len(m1),
##                stdev(m1),
##                sum(m2)/len(m2),
##                stdev(m2)
##                ))

            M1 = M1*(1 - MUTATE_RATE) + dM1
            M2 = M2*(1 - MUTATE_RATE) + dM2

            mutate1 = WIDTH1 * MUTATE_RATE * .5 * np.random.randn(8, HIDDEN_NEURONS)
            dM1 = dM1*.9 + mutate1

            mutate2 = WIDTH2 * MUTATE_RATE * .5 * np.random.randn(HIDDEN_NEURONS, 3)
            dM2 = dM2*.9 + mutate2

##    for mu1, s1, mu2, s2 in vals:
##        print(round(mu1,3), round(s1,3), round(mu2,3), round(s2,3))
    

if __name__ == "__main__":
    hallucinate_gif(256, 48, "hallucinate.gif")
