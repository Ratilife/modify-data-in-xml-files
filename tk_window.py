from tkinter import *  # Импортируем все из библиотеки Tkinter для создания графического интерфейса
from tkinter import filedialog, messagebox, ttk
import pickle  # pickle - модуль Python для сериализации и десериализации объектов.
from datetime import date

from Functions import Functions


# Задаем имя отчета по умолчанию метод не работает
def report_name():
    """Загружает значения из entry_b, entry_c и устанавливает их в entry_heading."""
    today = date.today()
    entry_heading.delete(0, END)
    entry_heading.insert(0, f"Отчет замены {entry_b.get()} на {entry_c.get()} создан {today}")
    # Генерация события <<EntryChange>> после установки текста в entry_c
    entry_c.event_generate("<<EntryChange>>")


# save_entries() - функция, которая сериализует значения entry_a и entry_d в файл data.pickle.
def save_entries():  # неработает
    """Сохраняет значения из entry_a и entry_d в файл."""
    data = {
        "entry_a": entry_a.get(),
        "entry_d": entry_d.get(),
    }
    with open("data.pickle", "wb") as f:
        pickle.dump(data, f)


# load_entries() - функция, которая десериализует значения из data.pickle и устанавливает их в entry_a и entry_d.
def load_entries():
    """Загружает значения из файла data.pickle и устанавливает их в entry_a и entry_d."""
    try:
        with open("data.pickle", "rb") as f:
            data = pickle.load(f)
        entry_a.delete(0, END)
        entry_a.insert(0, data["entry_a"])
        entry_d.delete(0, END)
        entry_d.insert(0, data["entry_d"])
    except FileNotFoundError:
        print("Файл data.pickle не найден.")

def path_to_file_check(entry):
    """Открывает диалоговое окно для выбора файла и возвращает его путь."""
    # Определяем тип диалогового окна (файл)
    file_path = filedialog.askopenfilename(title="Выберите файл")
    # Обрабатываем выбранный путь
    if file_path:
        # Выводим выбранный путь в поле entry
        entry.delete(0, 'end')
        entry.insert(0, file_path)
        print(f"Выбранный файл: {file_path}")
    else:
        print("Файл не выбран.")
def path_to_files(entry):
    """Открывает диалоговое окно для выбора папки и возвращает ее путь."""
    # Определяем тип диалогового окна (папка)
    dir_path = filedialog.askdirectory(title="Выберите папку с файлами")
    # Обрабатываем выбранный путь
    if dir_path:
        # Выводим выбранный путь в поле entry_a
        entry.delete(0, END)
        entry.insert(0, dir_path)
        print(f"Выбранный путь: {dir_path}")
    else:
        print("Путь не выбран.")


def to_begin():
    """ Начало процесса замены данных. Нажатие кнопки 'Начать'"""
    if entry_e.get().strip() == "":
        messagebox.showinfo("Информация", "Значение указанное в xml-файле не указано.\nУкажите значение!")
    else:
        # Создание словаря для данных на замену
        data_for_the_substitution = {entry_b.get(): entry_c.get()}

        bg = Functions()
        # Начало процесса заменны данных
        bg.start(entry_a.get(), data_for_the_substitution, entry_d.get()+ "\\" + entry_heading.get()+".txt", entry_e.get())
        messagebox.showinfo("Информация", "Всё: процесс завершен!")

def check():
    if entry_a_check.get().strip() == "":
        messagebox.showinfo("Информация", "Значение указанное в xml-файле не указано.\nУкажите значение!")
    else:
        bg = Functions()
        output_file_name = "differences.txt"
        bg.compare_xml_files(entry_a_check.get(), entry_b_check.get(), entry_d_check.get()+"\\"+output_file_name)
        messagebox.showinfo("Информация", "Всё: сравнение завершено!")
# Создание главного окна:
window = Tk()
window.title("Изменить версию 1C в xml-файле")  # Заголовок окна
window.geometry('600x230+500+150')  # Ширина 600, высота 230, смещение на 500 пикселей вправо и 150 пикселей вниз
# Размер окна и его начальное положение на экране
# Создание элементов интерфейса:

# создаем набор вкладок
nb = ttk.Notebook()
nb.pack(expand=True, fill=BOTH)

frame_change = ttk.Frame(nb)
frame_check  = ttk.Frame(nb)

frame_change.pack(fill=BOTH, expand=True)
frame_check.pack(fill=BOTH, expand=True)

nb.add(frame_change, text="Изменить")
nb.add(frame_check, text="Проверка")
# Метки (labels):
label_a = Label(frame_change, text="Путь к файлам:")
label_a.grid(column=0, row=0, padx=0, pady=10, sticky=W)

# Поля ввода (entries):
entry_a = Entry(frame_change, width=60)
entry_a.grid(columnspan=5, column=1, row=0, padx=0, pady=10, sticky=W)

# Кнопки (buttons):
button_a = Button(frame_change, text="...", command=lambda: path_to_files(entry_a))
button_a.grid(column=6, row=0, padx=0, pady=10, sticky=W)

# Метки (labels):
label_b = Label(frame_change, text="Поменять элемент:")
label_b.grid(column=0, row=1, padx=0, pady=10, sticky=W)

# Поля ввода (entries):
entry_b = Entry(frame_change, width=25)
entry_b.grid(column=1, row=1, padx=0, pady=10, sticky=W)
entry_b.insert(0, 'version')
# Метки (labels):
label_e = Label(frame_change, text="c:")
label_e.grid(column=2, row=1, padx=0, pady=10, sticky=W)

entry_e = Entry(frame_change, width=10)
entry_e.grid(column=3, row=1, padx=0, pady=10, sticky=W)

# Метки (labels):
label_с = Label(frame_change, text="на:")
label_с.grid(column=4, row=1, padx=0, pady=10, sticky=W)

# Поля ввода (entries):
entry_c = Entry(frame_change, width=10)
entry_c.grid(column=5, row=1, padx=0, pady=10, sticky=W)

# Метки (labels):
label_d = Label(frame_change, text="Путь к сохранению отчета:")
label_d.grid(column=0, row=2, padx=0, pady=10, sticky=W)

# Поля ввода (entries):
entry_d = Entry(frame_change, width=60)
entry_d.grid(columnspan=5, column=1, row=2, padx=0, pady=10, sticky=W)

# Кнопки (buttons):
button_b = Button(frame_change, text="...", command=lambda: path_to_files(entry_d))
button_b.grid(column=6, row=2, padx=0, pady=0, sticky=W)

# Метки (labels):
label_heading = Label(frame_change, text="Имя отчета:")
label_heading.grid(column=0, row=3, padx=0, pady=0, sticky=W)

# Поля ввода (entries):
entry_heading = Entry(frame_change, width=40)
entry_heading.grid(columnspan=5, column=1, row=3, padx=0, pady=0, sticky=W)

# bind связывает entry_c с событием FocusOut и вызывает lambda-функцию, когда фокус уходит с поля
entry_c.bind("<FocusOut>", lambda event: report_name())

# Метки (labels):
label_txt = Label(frame_change, text=".txt")
label_txt.grid(column=4, row=3, padx=0, pady=0, sticky=W)

# Кнопки (buttons):
button = Button(frame_change, text="Начать", bg="black", fg="red", command=to_begin)
button.grid(column=1, row=4, padx=0, pady=10, sticky=W)

# Интерфейс для сравнения
label_a_check = Label(frame_check, text="Путь к файлу источник:")
label_a_check.grid(column=0, row=0, padx=0, pady=10, sticky=W)


entry_a_check = Entry(frame_check, width=50)
entry_a_check.grid(columnspan=1, column=1, row=0, padx=0, pady=10, sticky=W)

button_a_check = Button(frame_check, text="...", command=lambda: path_to_file_check(entry_a_check))
button_a_check.grid(column=2, row=0, padx=0, pady=10, sticky=W)

label_b_check = Label(frame_check, text="Путь к файлу с измененными данными:")
label_b_check.grid(column=0, row=1, padx=0, pady=10, sticky=W)

entry_b_check = Entry(frame_check, width=50)
entry_b_check.grid(columnspan=1, column=1, row=1, padx=0, pady=10, sticky=W)

button_b_check = Button(frame_check, text="...", command=lambda: path_to_file_check(entry_b_check))
button_b_check.grid(column=2, row=1, padx=0, pady=10, sticky=W)

label_с_check = Label(frame_check, text="Путь к сохранению отчета:")
label_с_check.grid(column=0, row=2, padx=0, pady=10, sticky=W)

entry_d_check = Entry(frame_check, width=50)
entry_d_check.grid(columnspan=5, column=1, row=2, padx=0, pady=10, sticky=W)

button_с_check = Button(frame_check, text="...", command=lambda: path_to_files(entry_d_check))
button_с_check.grid(column=2, row=2, padx=0, pady=0, sticky=W)

button_check = Button(frame_check, text="Проверить", bg="black", fg="blue", command=check)
button_check.grid(column=1, row=4, padx=0, pady=10, sticky=W)


# Запуск главного цикла Tkinter для отображения и обработки интерфейса:
window.mainloop()
