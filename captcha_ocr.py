from PIL import Image

from pytesseract import image_to_string
img = Image.open('0afd91cb8211d26bf8c7063662ca84af.jpg') # Your image here!
img = img.convert("RGBA")

# Make the letters bolder for easier recognition
'''
for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][0] < 90:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][1] < 136:
            pixdata[x, y] = (0, 0, 0, 255)

for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
        if pixdata[x, y][2] > 0:
            pixdata[x, y] = (255, 255, 255, 255)

img.save("input-black.gif", "GIF")
'''
#   Make the image bigger (needed for OCR)
big = img.resize((1000, 500), Image.NEAREST)

ext = ".tif"
big.save("input-NEAREST" + ext)

#   Perform OCR using tesseract-ocr library

image = Image.open('0afd91cb8211d26bf8c7063662ca84af.jpg')
print (image_to_string(image))
