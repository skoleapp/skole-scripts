from pathlib import Path
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import qrcode


def main():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    strings = [
        "4LZTCF",
        "4FGSR3",
        "65FGTG",
        "FXGG55"
    ]


    for string in strings:
        qr.add_data(f"skoleapp.com/register/?code={string}")
        qr.make(fit=True)
        fnt = ImageFont.truetype('/Users/werneriaa/Library/Fonts/Roboto Mono for Powerline.ttf', 80)

        img = qr.make_image(fill_color="#FAF2DE", back_color="#AD3636")
        #img.save(f"{Path.home()}/Downloads/{string}.png")
        background = Image.open("promocard.png")
        img = img.resize((700,700))
        d = ImageDraw.Draw(background)
        d.text((105,275), f"{string}",font=fnt, fill=(250,242,222))
        img.show()
        background.paste(img, (30, 360))
        background.show()
        
        background.save(f"{Path.home()}/Downloads/{string}.png")


if __name__ == "__main__":
    main()
