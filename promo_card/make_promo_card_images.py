from PIL import Image, ImageFont, ImageDraw
import qrcode


def main():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    with open("beta_codes.txt") as f:
        strings = [code.strip() for code in f.readlines()]

    for string in strings:
        qr.add_data(f"skoleapp.com/register?code={string}")
        qr.make(fit=True)
        fnt = ImageFont.truetype(
            '/Users/werneriaa/Library/Fonts/Roboto Mono for Powerline.ttf', 80)

        img = qr.make_image(fill_color="#FAF2DE", back_color="#AD3636")
        # img.save(f"{Path.home()}/Downloads/{string}.png")
        background = Image.open("promocard.png")
        img = img.resize((700, 700))
        d = ImageDraw.Draw(background)
        d.text((105, 275), f"{string}", font=fnt, fill=(250, 242, 222))
        # img.show()
        background.paste(img, (30, 360))
        # background.show()

        background.save(
            f"/Users/werneriaa/Documents/Skole/promocards/{string}.png")
        qr.clear()


if __name__ == "__main__":
    main()
