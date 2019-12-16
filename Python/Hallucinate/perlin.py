from PIL import Image
import numpy as np
import imageio
from tqdm import tqdm

np.random.seed(2020)


def sigmoid(arr):
    return 1/(1 + np.exp(-arr))


def sharpen(arr, degree=10):
    return sigmoid(degree*(2*arr-1))


def cutoff(arr):
    z = np.zeros(arr.shape)
    return np.where(arr < .5, z, z+1)


def smoothstep(arr):
    return 3*np.power(arr, 2) - 2*np.power(arr, 3)


def normal(arr):
    return (arr - np.amin(arr))/(np.amax(arr) - np.amin(arr))


def hsl2rgb(h, s, l):
    chroma = np.multiply((1 - np.abs(2*l - 1)), s)
    hprime = h*6
    x = np.multiply(chroma, (1 - np.abs((hprime)%2 - 1)))
    m = l - chroma/2

    z = np.zeros(h.shape)

    r = m + np.where(np.logical_or(hprime < 1, 5 <= hprime), chroma, z) + np.where(np.logical_or(np.logical_and(1 <= hprime, hprime < 2), np.logical_and(4 <= hprime, hprime < 5)), x, z)
    g = m + np.where(np.logical_and(1 <= hprime, hprime < 3), chroma, z) + np.where(np.logical_and(3 <= hprime, hprime < 5), x, z)
    b = m + np.where(np.logical_and(3 <= hprime, hprime < 5), chroma, z) + np.where(np.logical_or(np.logical_and(2 <= hprime, hprime < 3), (5 <= hprime)), x, z)

    return np.dstack(((r*255), (g*255), (b*255)))


class PerlinLayer:
    def __init__(self, lattice_width, mutate_rate, width, height):
        assert(height % lattice_width == 0)
        assert(width % lattice_width == 0)
        
        self.lattice_width = lattice_width
        self.mutate_rate = mutate_rate
        self.height = height
        self.width = width
        
        self.orientations = np.random.rand(self.height//self.lattice_width, self.width//self.lattice_width)
        self.mutator = np.random.rand(self.height//self.lattice_width, self.width//self.lattice_width)

    def generate(self):
        unitvecs = np.dstack((np.sin(2*np.pi*self.orientations), np.cos(2*np.pi*self.orientations)))
        x, y = np.meshgrid(np.arange(0, self.width), np.arange(0, self.height))

        upper_lefts = np.repeat(np.repeat(unitvecs, self.lattice_width, axis=0), self.lattice_width, axis=1)
        upper_rights = np.concatenate((upper_lefts[:,self.lattice_width:], upper_lefts[:,:self.lattice_width]), axis=1)
        lower_lefts = np.concatenate((upper_lefts[self.lattice_width:], upper_lefts[:self.lattice_width]))
        lower_rights = np.concatenate((lower_lefts[:,self.lattice_width:], lower_lefts[:,:self.lattice_width]), axis=1)

        x_mod = np.mod(x, self.lattice_width)/self.lattice_width
        y_mod = np.mod(y, self.lattice_width)/self.lattice_width

        upper_left_grads = (np.multiply(x_mod, upper_lefts[:,:,0]) + np.multiply(y_mod, upper_lefts[:,:,1]))
        upper_right_grads = (np.multiply((x_mod-1), upper_rights[:,:,0]) + np.multiply((y_mod), upper_rights[:,:,1]))
        lower_left_grads = (np.multiply(x_mod, lower_lefts[:,:,0]) + np.multiply((y_mod-1), lower_lefts[:,:,1]))
        lower_right_grads = (np.multiply((x_mod-1), lower_rights[:,:,0]) + np.multiply((y_mod-1), lower_rights[:,:,1]))

        x_interp = smoothstep(x_mod)
        y_interp = smoothstep(y_mod)

        pixels = (upper_left_grads*(1-x_interp)*(1-y_interp)) + \
                 (upper_right_grads*(x_interp)*(1-y_interp)) + \
                 (lower_left_grads*(1-x_interp)*(y_interp)) + \
                 (lower_right_grads*(x_interp)*(y_interp))

        return normal(pixels)

    def mutate(self):
        self.orientations = self.orientations + self.mutate_rate*(self.mutator)
        #self.mutator = self.mutator*.93 + np.random.rand(self.height//self.lattice_width, self.width//self.lattice_width)*.1


class PerlinGenerator:
    def __init__(self, width, height, frames, filename, hue_layers, lightness_layers):
        self.height = height
        self.width = width
        self.frames = frames
        self.filename = filename
        
##        self.hue_layers = [PerlinLayer(lattice_width, mutate_rate, width, height) for lattice_width, mutate_rate in hue_layers]
        self.lightness_layers = [PerlinLayer(lattice_width, mutate_rate, width, height) for lattice_width, mutate_rate in lightness_layers]


    def perlin_gif(self):
        with imageio.get_writer(self.filename, mode='I') as writer:
            for i in tqdm(range(self.frames)):
##                h = np.zeros((self.height, self.width))
##                for layer in self.hue_layers:
##                    h += layer.generate()
##                    layer.mutate()
##                h = normal(h)
                
                l = np.zeros((self.height, self.width))
                for layer in self.lightness_layers:
                    l += layer.generate()
                    layer.mutate()
                l = sharpen(normal(l), degree=30)

##                s = np.zeros((self.height, self.width)) + 1

##                pixels = hsl2rgb(h, s, l)
                pixels = np.dstack((l, l, l))*255

                img = Image.fromarray(np.uint8(pixels), 'RGB')
                
                img.save("hallucinate.png")
                writer.append_data(imageio.imread("hallucinate.png"))
    

if __name__ == "__main__":
    hue_layers = [
        (40, .05),
        (30, .05)
    ]    
    
    lightness_layers = [
        (80, .2),
        (60, .1),
    ]
    
    pg = PerlinGenerator(1200, 720, 30, "hallucinate2.gif", hue_layers, lightness_layers)
    pg.perlin_gif()
