import os
import barcode
import transliterate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from barcode.writer import ImageWriter
from pathlib import Path


class Generator:
    def __init__(self, name, pk, category, country, country_code, result_path):
        self.pk = pk
        self.draw = None
        self.path = Path.cwd()
        self.template_size = 3400

        self.result_path = result_path

        self.file_name = f'cards/{self.pk}.png'

        self.category = category
        self.country = country
        self.country_code = country_code

        self.name_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 50 * 4)
        self.name = name
        self.name_size = self.name_font.getsize(self.name)

        self.description_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 30 * 4)

        self.validity_period_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 24 * 4)

        self.code_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 24 * 4)

        self.label_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 36 * 4)
        self.label_description_font = ImageFont.truetype(f"{self.path}/static/fonts/arial_regular.ttf", 30 * 4)

    @staticmethod
    def has_cyr(s):
        lower = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return lower.intersection(s.lower()) != set()
    #
    # def transliterate(self, s):
    #     if self.has_cyr(s):
    #         s = transliterate.translit(s, reversed=True)
    #     return s

    def draw_name(self):
        self.draw.text(((self.template_size - self.name_size[0]) / 2, 478 * 4), self.name, (0, 29, 60),
                       font=self.name_font)

    def draw_front_description(self):
        category_size = self.description_font.getsize(f"{self.category} of the")[0]
        category_size = (self.template_size - category_size)/2

        self.draw.text((category_size, 572 * 4), self.category, (255, 97, 60),
                       font=self.description_font,)

        self.draw.text((category_size + self.description_font.getsize(self.category)[0] +
                        self.description_font.getsize(" ")[0], 572 * 4), "of the", (0, 0, 0),
                       font=self.description_font, )

        self.draw.text((251 * 4, 614 * 4), "UNEPG 2022", (0, 0, 0),
                       font=self.description_font, )
        self.draw.text((443 * 4, 614 * 4), self.country, (0, 174, 239),
                       font=self.description_font, )

    def draw_description(self):
        self.draw.text((210 * 4, 530 * 4), "KazNU Coordinator", (0, 29, 60), font=self.label_font)
        self.draw.text((210 * 4, (530 + 50) * 4), "Amirkhan: 8 (702) 820 0400", (0, 29, 60),
                       font=self.label_description_font)
        self.draw.text((210 * 4, (530 + 120) * 4), "UNICEF Kazakhstan", (0, 29, 60), font=self.label_font)
        self.draw.text((210 * 4, (530 + 170) * 4), "Raushan: 8 (705) 174 0212", (0, 29, 60),
                       font=self.label_description_font)

    def place_bar_code(self, filename):
        bar_code = Image.open(filename)
        width, height = bar_code.size
        bar_code = bar_code.resize((width * 4, height * 4), Image.ANTIALIAS)
        card_name = f'cards/{self.pk}.png'
        card = Image.open(card_name)
        bar_code = bar_code.convert("RGBA")
        card = card.convert("RGBA")

        card.paste(bar_code, (int((self.template_size - width * 4)/2), 705 * 4))
        bar_code.close()
        # os.remove(filename)
        return card

    def draw_bar_code(self):
        options = {"module_height": 6.5, "text_distance": 0.5}
        code128 = barcode.get('code128', f'{self.country_code}-{self.pk}-{self.category.upper()}', writer=ImageWriter())
        filename = code128.save(f"{self.path}/media/bar/1", options=options)
        return self.place_bar_code(filename)

    def draw_codes(self):
        self.draw.text((210 * 4, 770 * 4), "101 - Fire", (0, 0, 0), font=self.code_font)
        self.draw.text((210 * 4, (765 + 40) * 4), "102 - Police", (0, 0, 0), font=self.code_font)
        self.draw.text((210 * 4, (765 + 75) * 4), "103 - Ambulance", (0, 0, 0), font=self.code_font)

    def draw_footer(self):
        text_1 = "UNEPG is a joint project of UNICEF Kazakhstan"
        text_2 = "and Al-Farabi Kazakh National University"
        center_1 = (self.template_size - self.code_font.getsize(text_1)[0])/2
        center_2 = (self.template_size - self.code_font.getsize(text_2)[0])/2

        self.draw.text((center_1, 1034 * 4), text_1, (0, 0, 0), font=self.code_font)
        self.draw.text((center_2, (1034 + 40) * 4), text_2, (0, 0, 0), font=self.code_font)

    def draw_validity(self):
        self.draw.text(((self.template_size -
                         self.validity_period_font.getsize("Validity period: 21/03/2022 - 01/05/2022")[0])/2, 839 * 4),
                       "Validity period: 21/03/2022 - 01/05/2022", (0, 0, 0), font=self.validity_period_font)

    def draw_front(self):
        path = Path.cwd()
        card_template = Image.open(path.joinpath(*"/static/images/front.png".split("/")))
        self.draw = ImageDraw.Draw(card_template)

        self.draw_name()
        self.draw_front_description()
        self.draw_validity()
        card_template.save(self.file_name)
        self.draw_bar_code()
        card = self.draw_bar_code()
        card.save(f'{self.result_path}/cards/{self.pk}.png')
        # os.remove(f'cards/{self.transliterate(self.name)}.png')
        card.close()
        card_template.close()

    def draw_back(self):
        path = Path.cwd()
        card_template = Image.open(path.joinpath(*"/static/images/back.png".split("/")))
        self.draw = ImageDraw.Draw(card_template)
        self.draw_description()
        self.draw_codes()
        self.draw_footer()
        card_template.save(f"{self.result_path}/back/back.png")

    def generate_images(self):
        self.draw_front()
        self.draw_back()
