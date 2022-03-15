import os
from tkinter import *
from tkinter import filedialog, messagebox, Toplevel
from reader import open_xlsx
from reader import Generator
import threading
from pathlib import Path


class UnisatIDInterface:
    def __init__(self):
        self.path = Path.cwd()
        self.window = Tk()
        self.window.title("Unisat Auto-Badge")
        self.window.geometry('800x600')
        self.window.resizable(False, False)
        self.file = None
        self.dir = None

        bg = PhotoImage(file=self.path.joinpath(*"static/images/small_interface.png".split('/')))
        label1 = Label(self.window, image=bg)
        label1.place(x=0, y=0)
        self.set_buttons()
        self.window.mainloop()

    def set_buttons(self):
        file_btn = Button(self.window, text="Выберите Excel файл", command=self.load_file, height=2, width=50,)
        file_btn.place(x=190, y=300)

        path_btn = Button(self.window, text="Выберете пустую папку", command=self.set_dir, height=2, width=50, )
        path_btn.place(x=190, y=373)

        start_btn = Button(self.window, text="Начать", command=self.start, height=2, width=50, )
        start_btn.place(x=190, y=443)

        read_me_btn = Button(self.window, text="Инструкции", command=self.open_instructions, height=2, width=10, )
        read_me_btn.place(x=640, y=70)

    def open_instructions(self):
        window = Toplevel()
        window.title("Инструкция")
        window.geometry('800x300')
        window.configure(bg='white')
        window.resizable(False, False)
        lbl = Label(window, text="1. Укажите xlsx файл по стандарту указанному в картинке ниже", bg='white')
        lbl.place(x=30, y=0)

        bg = PhotoImage(file=self.path.joinpath(*"/static/images/example.png".split("/")))
        lbl2 = Label(window, image=bg, height=183, width=711)
        lbl2.place(x=30, y=30)

        lbl3 = Label(window, text="2. Укажите папку, где будут находиться сгенерированные изображения", bg='white')
        lbl3.place(x=30, y=230)

        lbl4 = Label(window, text="3. Дождитесь окончания времени генерации(время является примерным, "
                                  "нужно дождаться кнопки выхода).", bg='white')
        lbl4.place(x=30, y=260)

        window.mainloop()

    def load_file(self):
        self.file = filedialog.askopenfilename(initialdir=self.path,
                                               filetypes=(("Excel files", "*.xlsx"),))

    def set_dir(self):
        self.dir = filedialog.askdirectory(initialdir=self.path)
        try:
            if self.dir:
                os.mkdir(f"{self.dir}/cards")
                os.mkdir(f"{self.dir}/back")
                os.mkdir(f"{self.dir}/temp_cards")
                os.mkdir(f"{self.dir}/bar")
        except FileExistsError:
            messagebox.showerror('Ошибка', "В данной папке уже существуют директории cards и back. "
                                           "Выберите пустую директорию")

    def start(self):
        if self.dir and self.file:
            try:
                open_xlsx(dir_path=self.dir, file_path=self.file, timer=ClockInterface, window=self.window)

            except ValueError as error:
                messagebox.showerror('Ошибка', str(error))

                os.rmdir(f"{self.dir}/cards")
                os.rmdir(f"{self.dir}/back")
        else:
            if not self.dir and not self.file:
                messagebox.showerror('Ошибка', "Выберите excel файл и папку, для генерации картинок")
            elif not self.dir:
                messagebox.showerror('Ошибка', "Выберите папку, для генерации картинок")
            elif not self.file:
                messagebox.showerror('Ошибка', "Выберите excel файл")


class ClockInterface:
    def __init__(self, data, dir_path):
        self.path = Path.cwd()
        self.window = Tk()
        self.window.title("Unisat Auto-Badge")
        self.window.geometry('800x600')
        self.window.resizable(False, False)
        self.file = None
        self.dir = None
        self.is_done = False
        self.object_count = None

        my_thread = threading.Thread(target=self.run_generator, args=(data, dir_path))
        my_thread.start()

        bg = PhotoImage(file=self.path.joinpath(*"/static/images/small_interface.png".split("/")))
        label = Label(self.window, image=bg)
        label.place(x=0, y=0)
        self.objects_remain = Label(text="", font=('Helvetica', 38), bg='white')
        self.objects_remain.place(x=160, y=300)
        self.update_count()
        self.window.mainloop()

    def close(self):
        self.window.destroy()

    def run_generator(self, data, dir_path):
        self.object_count = len(data)
        for row in data:
            generator = Generator(name=row[0], pk=row[1], category=row[2], country=row[3], country_code=row[4],
                                  result_path=dir_path)
            generator.generate_images()

            self.object_count -= 1

        self.is_done = True

        if self.is_done:
            file_btn = Button(self.window, text="Close", command=self.close, height=2, width=50, )
            file_btn.place(x=190, y=430)

    def update_count(self):
        count = str(self.object_count)
        self.objects_remain.configure(text=f"Осталось {count} объектов")
        self.window.after(1000, self.update_count)

interface = UnisatIDInterface()
