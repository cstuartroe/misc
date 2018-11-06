from PIL import Image

def steg_impose(overt,hidden):
    assert(overt.size == hidden.size)
    x, y = overt.size
    overt_pix = overt.load()
    hidden_pix = hidden.load()
    for i in range(x):
        for j in range(y):
            overt_pixel = overt_pix[i,j]
            hidden_pixel = hidden_pix[i,j]
            overt_pix[i,j] = tuple([((overt_pixel[k]//4)*4) + (hidden_pixel[k]//64) for k in range(3)])
    return overt

def steg_reveal(img):
    pix = img.load()
    x, y = img.size
    for i in range(x):
        for j in range(y):
            pixel = pix[i,j]
            pix[i,j] = tuple([((pixel[k]%4)*64) for k in range(3)])
    return img

def leftshift(img):
    pix = img.load()
    x, y = img.size
    for i in range(x):
        for j in range(y):
            pixel = pix[i,j]
            pix[i,j] = tuple([((pixel[k]//32)*32) for k in range(3)])
    return img

overt = Image.open('tree.png')
hidden = Image.open('secret.png')
img = steg_impose(overt,hidden)
img.save('cat.png')
img = Image.open('tree.png')
img = steg_reveal(img)
img.save('2secret.png')
