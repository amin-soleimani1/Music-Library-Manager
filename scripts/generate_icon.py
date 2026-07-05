from PIL import Image, ImageDraw

img = Image.open("assets/images/icon.jpg").convert("RGBA")

size = img.size

radius = 150

mask = Image.new("L", size, 0)

draw = ImageDraw.Draw(mask)
draw.rounded_rectangle(
    (0, 0, size[0], size[1]),
    radius=radius,
    fill=255
)

img.putalpha(mask)

img.save(
    "assets/images/icon.ico",
    format="ICO",
    sizes=[
        (16,16),
        (32,32),
        (48,48),
        (64,64),
        (128,128),
        (256,256)
    ]
)