import qrcode as qrcode
import transliterate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os


class Generator:
    def __init__(self, name, pk):
        self.pk = pk
        self.draw = None
        self.path = os.getcwd()
        self.template_size = 2240

        self.name_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_bold.ttf", 38 * 4)
        self.name = name
        self.name_size = self.name_font.getsize(self.name)

        self.code_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 16 * 4)

        self.label_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 24 * 4)
        self.label_description_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 20 * 4)

    @staticmethod
    def has_cyr(s):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(s.lower()) != set()

    def transliterate(self, s):
        if self.has_cyr(s):
            s = transliterate.translit(s, reversed=True)
        return s

    def draw_name(self):
        self.draw.text(((self.template_size - self.name_size[0]) / 2, 341 * 4), self.name, (0, 29, 60),
                       font=self.name_font)

    def draw_description(self):
        self.draw.text((42 * 4, 416 * 4), "Кординатор / Coordinator", (0, 29, 60), font=self.label_font)
        self.draw.text((42 * 4, (416 + 30) * 4), "Темирбаев А.A: 8 (702) 820 0400", (0, 29, 60),
                       font=self.label_description_font)
        self.draw.text((42 * 4, (416 + 60) * 4), "UNICEF Kazakhstan", (0, 29, 60), font=self.label_font)
        self.draw.text((42 * 4, (416 + 90) * 4), "Ибрашева Р: 8 (705) 174 0212", (0, 29, 60),
                       font=self.label_description_font)

    def draw_codes(self):
        self.draw.text((42 * 4, 576 * 4), "101 - служба пожаротушения", (0, 0, 0), font=self.code_font)
        self.draw.text((42 * 4, (576 + 20) * 4), "102 - полиция", (0, 0, 0), font=self.code_font)
        self.draw.text((42 * 4, (576 + 40) * 4), "103 - скорая медицинская помощь", (0, 0, 0), font=self.code_font)

    def generate_qr(self):
        path = os.getcwd()
        file_name = f'{path}/media/qr/{self.transliterate(self.name)}.png'
        qrcode_image = qrcode.make(f"{self.transliterate(self.name)}-KZ2022")
        qrcode_image.save(f'{file_name}', 'PNG')
        return file_name

    def place_qr(self):
        file_name = self.generate_qr()
        qr_code = Image.open(file_name)
        qr_code = qr_code.resize((160*4, 160*4), Image.ANTIALIAS)
        card_name = f'cards/{self.transliterate(self.name)}.png'
        card = Image.open(card_name)
        qr_code = qr_code.convert("RGBA")
        card = card.convert("RGBA")
        card.paste(qr_code, (371 * 4, 539 * 4))
        qr_code.close()
        os.remove(file_name)
        return card

    def generate_images(self):
        path = os.getcwd()
        card_template = Image.open(f"{path}/static/images/big-template.png")
        self.draw = ImageDraw.Draw(card_template)

        self.draw_name()
        self.draw_description()
        self.draw_codes()
        card_template.save(f'cards/{self.transliterate(self.name)}.png')

        card = self.place_qr()
        card.save(f'cards/{self.pk}.png')
        os.remove(f'cards/{self.transliterate(self.name)}.png')
        card.close()
