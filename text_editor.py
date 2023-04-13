from tkinter import *
import tkinter as tk
from tkinter import ttk, INSERT
import tkinter
import os
import tkinter.filedialog
from difflib import SequenceMatcher
from tkinter import filedialog
from tkinter import colorchooser
import speech_recognition as sr
import random
from PIL import Image, ImageTk
import pyttsx3
from tkinter import font
import cv2 as cv
import tkinter.messagebox
from tkinter import messagebox



root = Tk()
root.iconbitmap('icon.ico')

root.title("Текстовый Редактор \"LOgka\"")
file_name = None
_width = 1200
_height = 800

root_width = root.winfo_screenwidth()
root_height = root.winfo_screenheight()

x = (root_width / 2) - (_width / 2)
y = (root_height / 2) - (_height / 2)

root.geometry(f'{_width}x{_height}+{int(x)}+{int(y)}')

############################################ МЕНЮ #####################################################
def new_file(event=None):
    global url
    url = ""
    content_text.delete(1.0, tk.END)
# Открыть файл
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Выберите файл",
                                     filetypes=(("Текстовый файл", "*.txt"), ("Все файлы", "*.*")))
    try:
        with open(url, "r") as fr:
            content_text.delete(1.0, tk.END)
            content_text.insert(1.0, fr.read())
    except FileNotFoundError:
        return
    except:
        return
    content_text.title(os.path.basename(url))

def write_to_file(file_name):
        try:
            content = content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
        except IOError:
            pass

# Сохранить как
def save_as(event=None):
    global url
    try:
        content = content_text.get(1.0, tk.END)
        url = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                       filetypes=(("Текстовый файл", "*.txt"), ("Все файлы", "*.*")))
        url.write(content)
        url.close()
    except:
        return

# Сохранить
def save(event=None):
    global url
    try:
        if url:
            content = str(content_text.get(1.0, tk.END))
            with open(url, "w", encoding="utf-8") as fw:
                fw.write(content)
        else:
            url = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                           filetypes=(("Текстовый файл", "*.txt"), ("Все файлы", "*.*")))
            content2 = content_text.get(1.0, tk.END)
            url.write(content2)
            url.close()
    except:
        return


###############################################################################################
############################### Значки для составного меню ####################################
global new_file_icon
global open_file_icon
global save_file_icon
global cut_icon
global copy_icon
global paste_icon
global clear_all_icon
global find_icon
global text_color_icon
global bold_icon
global italic_icon
global strikeout_icon
global select_icon
global text_to_speech_icon
global speech_to_text_icon
global exit_icon
global align_left_icon
global align_right_icon
global align_center_icon
global compare_icon

new_file_icon = PhotoImage(file='icons/new_file.png')
open_file_icon = PhotoImage(file='icons/open_file.png')
save_file_icon = PhotoImage(file='icons/save.png')
cut_icon = PhotoImage(file='icons/cut.png')
copy_icon = PhotoImage(file='icons/copy.png')
paste_icon = PhotoImage(file='icons/paste.png')
clear_all_icon = PhotoImage(file= 'icons/clear_all.png')
find_icon = PhotoImage(file='icons/find_text.png')
text_color_icon = PhotoImage(file='icons/font_color.png')
bold_icon = PhotoImage(file='icons/font-style-bold.png')
italic_icon = PhotoImage(file='icons/italic.png')
strikeout_icon = PhotoImage(file='icons/strike.png')
underline_icon = PhotoImage(file='icons/underline.png')
select_icon = PhotoImage(file='icons/cursor.png')
text_to_speech_icon = PhotoImage(file='icons/text to speech.png')
speech_to_text_icon = PhotoImage(file='icons/speech.png')
exit_icon = PhotoImage(file='icons/exit.png')
align_left_icon = PhotoImage(file= 'icons/align_left.png')
align_right_icon = PhotoImage(file= 'icons/align_right.png')
align_center_icon = PhotoImage(file= 'icons/align_center.png')
tool_bar_icon = tk.PhotoImage(file="icons/tool_bar.png")
status_bar_icon = tk.PhotoImage(file="icons/status_bar.png")
compare_icon = PhotoImage(file='icons/compare.png')
############################################################################
########################## МЕНЮ РЕДАКТИРОВАНИЯ #############################
def cut():
        content_text.event_generate("<<Cut>>")
        on_content_changed()
        return "break"
def copy():
        content_text.event_generate("<<Copy>>")
        on_content_changed()
        return "break"
def paste():
        content_text.event_generate("<<Paste>>")
        on_content_changed()
        return "break"
def clearall():
    content_text.delete(1.0, tk.END)
    on_content_changed()
    return "break"
def selectall(event=None):
        content_text.tag_add('sel','1.0','end')
        return "break"
# Сравнение файлов
def compare_files():
        file1 = filedialog.askopenfilename(initialdir="C:/gui/", title="Choose File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

        text_file1 = open(file1, 'r')

        file1_data = text_file1.read()
        file2_data = content_text.get(1.0,END)
        similarity = SequenceMatcher(None, file1_data, file2_data).ratio()
        messagebox.showinfo("Плагиат", f"Содержание составляет {similarity * 100:.3f}% общего.")
##################################################################
#################### Найти или Заменить ##########################
def find_text(event=None):
    def find():
        word = find_input.get()
        content_text.tag_remove('match', "1.0", tk.END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos = content_text.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+ {len(word)}c"
                content_text.tag_add("match", start_pos, end_pos)
                matches += 1
                start_pos = end_pos
                content_text.tag_config("match", foreground="yellow", background="green")
    def replace():
        word = find_input.get()
        replace_text = replace_input.get()
        content = content_text.get(1.0, tk.END)

        new_content = content.replace(word, replace_text)
        content_text.delete(1.0, tk.END)
        content_text.insert(1.0, new_content)
    search_toplevel = Toplevel(root)
    search_toplevel.geometry("375x250+500+200")
    search_toplevel.iconphoto(False, PhotoImage(file="icons/find_text.png"))
    search_toplevel.title('Поиск')
    search_toplevel.resizable(0, 0)

    # окно
    find_frame = ttk.LabelFrame(search_toplevel, text="Найти или заменить")
    find_frame.pack(pady=20)

    text_find_label = ttk.Label(find_frame, text="Найти : ")
    text_replace_label = ttk.Label(find_frame, text="Заменить на :")

    find_input = ttk.Entry(find_frame, width=30)
    replace_input = ttk.Entry(find_frame, width=30)

    find_button = ttk.Button(find_frame, text="Найти", command=find)
    replace_button = ttk.Button(find_frame, text="Заменить", command=replace)

    text_find_label.grid(row=0, column=0, padx=4, pady=4)
    text_replace_label.grid(row=1, column=0, padx=4, pady=4)

    find_input.grid(row=0, column=1, padx=4, pady=4)
    replace_input.grid(row=1, column=1, padx=4, pady=4)

    find_button.grid(row=2, column=0, padx=8, pady=4)
    replace_button.grid(row=2, column=2, padx=8, pady=4)

    search_toplevel.mainloop()
##################################################################################
########################### Работа со звуком #####################################
#Читка текста
def text_to_speech(**kwargs):
        if 'text' in kwargs:
            text = kwargs['text']
        else:
            text = content_text.get(1.0,END)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()

### Форматиирование текста
def text_formatter(phrase):
    interrogatives = ('как', 'почему', 'что', 'когда', 'кто', 'где', 'вы', "кому", "чья")
    capitalized = phrase.capitalize()
    if phrase.startswith(interrogatives):
        return (f'{capitalized}?')
    else:
        return (f'{capitalized}.')

def speech_to_text():
        errors = [
            "Я не понимаю, что ты имеешь в виду!",
            "Прошу прощения?",
            "Не могли бы повторить",
            "Повторите это еще раз, пожалуйста!",
            "Извините, я этого не понял"
        ]
        r = sr.Recognizer()
        def SpeakText(command):
            engine = pyttsx3.init()
            engine.say(command)
            engine.runAndWait()
        while (1):
            try:
                # используем микрофон для входа
                with sr.Microphone() as source2:
                    text_to_speech(text='Скажи текст, через две секунды после этого сообщения говорите четко')
                    r.pause_threshold = 2  # задержка в две секунды с момента запуска кнопки перед прослушиванием
                    # Прослушиваем входные данные от пользователя
                    print("Listening ...")
                    audio2 = r.listen(source2)
                    query = r.recognize_google(audio2, language='ru-RU')
                    query = text_formatter(query)
                    # using google to recognize audio
                    Text = r.recognize_google(audio2)
                    Text = Text.lower()
            except Exception:
                error = random.choice(errors)
                text_to_speech(text=error)
                query = speech_to_text()
            content_text.insert(tk.INSERT, query, tk.END)
            return query
#############################################################################################
# Жирный шрифт
def bold_it():
        # Create our font
        try:
            bold_font = font.Font(content_text, content_text.cget("font"))
            bold_font.configure(weight="bold")

            # Configure a tag
            content_text.tag_configure("bold", font=bold_font)

            # Define Current tags
            current_tags = content_text.tag_names("sel.first")

            # If statment to see if tag has been set
            if "bold" in current_tags:
                content_text.tag_remove("bold", "sel.first", "sel.last")
            else:
                content_text.tag_add("bold", "sel.first", "sel.last")

        except Exception:
            pass

# Курсив
def italics_it():
        # Create our font
        try:
            italics_font = font.Font(content_text, content_text.cget("font"))
            italics_font.configure(slant="italic")

            # Configure a tag
            content_text.tag_configure("italic", font=italics_font)

            # Define Current tags
            current_tags = content_text.tag_names("sel.first")

            # If statment to see if tag has been set
            if "italic" in current_tags:
                content_text.tag_remove("italic", "sel.first", "sel.last")
            else:
                content_text.tag_add("italic", "sel.first", "sel.last")
        except Exception:
            pass

# Подчеркивание
def change_underline():
        # Create our font
        try:
            underline_font = font.Font(content_text, content_text.cget("font"))
            underline_font.configure(underline=1)
            # Configure a tag
            content_text.tag_configure("underline", font=underline_font)
            # Define Current tags
            current_tags = content_text.tag_names("sel.first")
            # If statment to see if tag has been set
            if "underline" in current_tags:
                content_text.tag_remove("underline", "sel.first", "sel.last")
            else:
                content_text.tag_add("underline", "sel.first", "sel.last")
        except Exception:
            pass

# Зачеркнутый
def change_strikeout():
        try:
            strikeout_font = font.Font(content_text, content_text.cget("font"))
            strikeout_font.configure(overstrike=1)
            content_text.tag_configure("overstrike", font=strikeout_font)
            current_tags = content_text.tag_names("sel.first")
            if "overstrike" in current_tags:
                content_text.tag_remove("overstrike", "sel.first", "sel.last")
            else:
                content_text.tag_add("overstrike", "sel.first", "sel.last")
        except Exception:
            pass

######## Выравнивание ########
### По левый край
def align_left():
    text_content = content_text.get(1.0, "end")
    content_text.tag_config("left", justify=tk.LEFT)
    content_text.delete(1.0, tk.END)
    content_text.insert(tk.INSERT, text_content, "left")


    align_left_btn.configure(command=align_left)

### По центру
def align_center():
    text_content = content_text.get(1.0, "end")
    content_text.tag_config("center", justify=tk.CENTER)
    content_text.delete(1.0, tk.END)
    content_text.insert(tk.INSERT, text_content, "center")

    align_center_btn.configure(command=align_center)

### По правому краю
def align_right():
    text_content = content_text.get(1.0, "end")
    content_text.tag_config("right", justify=tk.RIGHT)
    content_text.delete(1.0, tk.END)
    content_text.insert(tk.INSERT, text_content, "right")
    align_right_btn.configure(command=align_right)
###################################

def SetFontSize():
    Font[1] = size_var.get()
    content_text.config(font=Font)

def SetFontFace():
    Font[0] = face_var.get()
    content_text.config(font=Font)

#Цвет текста
def text_color():
        # Pick a color
        my_color = colorchooser.askcolor()[1]
        if my_color:
            try:
                # Create our font
                color_font = font.Font(content_text, content_text.cget("font"))

                # Configure a tag
                content_text.tag_configure("colored", font=color_font, foreground=my_color)

                # Define Current tags
                current_tags = content_text.tag_names("sel.first")

                # If statment to see if tag has been set
                if "colored" in current_tags:
                    content_text.tag_remove("colored", "sel.first", "sel.last")
                else:
                    content_text.tag_add("colored", "sel.first", "sel.last")
            except Exception:
                content_text.config(fg=my_color)
    #ABOUT MENU



#Выход
def exit_editor(event=None):
        if tkinter.messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?))))))))))))))"):
            root.destroy()

#Изменить тему
def change_theme(event=None):
        selected_theme = theme_choice.get()
        fg_bg_colors = color_schemes.get(selected_theme)
        foreground_color, background_color = fg_bg_colors.split('.')
        content_text.config(
            background=background_color, fg=foreground_color)

# Всплывающее меню
def show_popup_menu(event):
        popup_menu.tk_popup(event.x_root, event.y_root)

################################################# МЕНЮ #################################################################
menu_bar = Menu(root) #menu begins

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Новый файл', accelerator='Ctrl+N', compound='left', image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Открыть', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label="Сохранить", accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0, command=save)
file_menu.add_command(label="Сохранить как", accelerator='Ctrl+Shift+S',image=save_file_icon, compound='left', underline=0, command = save_as)
file_menu.add_separator()
file_menu.add_command(label="Сравнить файл",image=compare_icon,compound='left', command=compare_files)
file_menu.add_separator()
file_menu.add_command(label="Выход", accelerator='Alt+F4',image=exit_icon, compound='left', underline=0, command=exit_editor)
menu_bar.add_cascade(label='Файл', menu=file_menu)

######################################### Редактировать ###########################################################
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_separator()
edit_menu.add_command(label='Вырезать', accelerator='Ctrl+X', compound='left',  image=cut_icon, underline=0, command=cut)
edit_menu.add_command(label='Копировать', accelerator='Ctrl+C', compound='left', image=copy_icon, underline=0, command=copy)
edit_menu.add_command(label='Вставить', accelerator='Ctrl+V', compound='left',  image=paste_icon, underline=0, command=paste)
edit_menu.add_command(label='Очистить все', compound='left',  image=clear_all_icon, underline=0, command=clearall)
edit_menu.add_separator()
edit_menu.add_command(label='Поиск', accelerator='Ctrl+F', compound='left',  image=find_icon, underline=0, command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Выбрать все',image=select_icon, accelerator='Ctrl+A', compound='left', underline=0, command=selectall)
menu_bar.add_cascade(label='Редактировать', menu=edit_menu)


############ тулбар  и статусбар ##############
show_statusbar = tk.BooleanVar()
show_statusbar.set(True)
show_toolbar = tk.BooleanVar()
show_toolbar.set(True)

# Скрыть тулбар
def hide_toolbar():
    global show_toolbar
    if show_toolbar:
        shortcut_bar.pack_forget()
        show_toolbar = False
    else:
        content_text.pack_forget()
        status_bar.pack_forget()
        shortcut_bar.pack(side=tk.TOP, fill=tk.X)
        content_text.pack(fill=tk.BOTH, expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar = True

# Скрыть состояние
def hide_statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar = False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar = True
#################################################
####### Просмотр #######
view_menu = Menu(menu_bar, tearoff=0)
show_line_number=IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Панель инструментов", onvalue=True, offvalue=False, variable=show_toolbar,
                     image=tool_bar_icon, compound=tk.LEFT, command=hide_toolbar)
view_menu.add_checkbutton(label="Строка состояния", onvalue=True, offvalue=False, variable=show_statusbar,
                     image=status_bar_icon, compound=tk.LEFT, command=hide_statusbar)
menu_bar.add_cascade(label='Просмотр', menu=view_menu)
##############################
###### Тема  ####
themes_menu=Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Темы", compound='left', menu=themes_menu)
''' Цветовая тема'''
color_schemes = {
    "Светлая": '#000000.#ffffff',
    "Серая": '#474747.#e0e0e0',
    "Темная": '#c4c4c4.#2d2d2d',
    "Красная": '#2d2d2d.#ffe8e8',
    "Кремовая": '#d3b774.#FFFDD0',
    "Синяя": '#ededed.#6b9dc2'
}
theme_choice=StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)

############################
########################## Шрифт ###############################

Font = ["Arial", 12]
font_sizes = [8,9,10,11,12,14,16,18,20,22,24,26,28,34,36,48,72]
font_faces = ["Arial", "Times New Roman", "Helvetica", "Courier", "Star Wars", "Comic Sans MS", "Bahnschrift"]
font_size = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Размер шрифта', menu=font_size)
font_face = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Тип шрифта', menu=font_face)
size_var = IntVar()
size_var.set(12)
face_var = StringVar()
face_var.set("Arial")
for k in sorted(font_sizes):
    font_size.add_radiobutton(label=k, compound='left', variable=size_var, command=SetFontSize)

for j in sorted(font_faces):
    font_face.add_radiobutton(label=j, compound='left', variable=face_var, command=SetFontFace)

##################################################
root.config(menu=menu_bar)
########### Верхняя панель быстрого доступа############
shortcut_bar=Frame(root, height=25)
shortcut_bar.pack(fill=X,side=TOP)

# Добавление значков быстрого доступа
text_color_btn= Button(shortcut_bar,image=text_color_icon,height=40,width=40,command=text_color, cursor="hand2")
text_color_btn.pack(side='left')
bold_it_btn= Button(shortcut_bar,image=bold_icon,height=40,width=40,command=bold_it, cursor="hand2")
bold_it_btn.pack(side='left')
italics_it_btn= Button(shortcut_bar,image=italic_icon,height=40,width=40,command=italics_it, cursor="hand2")
italics_it_btn.pack(side='left')
change_underline_btn= Button(shortcut_bar,image=underline_icon,height=40,width=40,command=change_underline, cursor="hand2")
change_underline_btn.pack(side='left')
change_strikeout_btn= Button(shortcut_bar,image=strikeout_icon,height=40,width=40,command=change_strikeout, cursor="hand2")
change_strikeout_btn.pack(side='left')
align_left_btn= Button(shortcut_bar,image=align_left_icon,height=40,width=40,command=align_left, cursor="hand2")
align_left_btn.pack(side='left')
align_center_btn= Button(shortcut_bar,image=align_center_icon,height=40,width=40,command=align_center, cursor="hand2")
align_center_btn.pack(side='left')
align_right_btn= Button(shortcut_bar,image=align_right_icon,height=40,width=40,command=align_right, cursor="hand2")
align_right_btn.pack(side='left')
text_to_speech_btn= Button(shortcut_bar,image=text_to_speech_icon,height=40,width=40,command=text_to_speech, cursor="hand2")
text_to_speech_btn.pack(side='left')
speech_to_text_btn= Button(shortcut_bar,image=speech_to_text_icon,height=40,width=40,command=speech_to_text, cursor="hand2")
speech_to_text_btn.pack(side='left')
################################################################################
# Добавление основного контекстного текстового виджета и виджета полосы прокрутки
content_text = Text(root, wrap='word',font=Font)
scroll_bar = Scrollbar(root)
scroll_bar.pack(side='right', fill='y')
content_text.pack(fill='both', expand=True)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)


# Настройка всплывающего меню
popup_menu = Menu(content_text,tearoff=0)
popup_menu.add_command(label='Вырезать', underline=7, command=cut)
popup_menu.add_command(label='Копировать', underline=7, command=copy)
popup_menu.add_command(label='Вставить', underline=7, command=paste)
popup_menu.add_separator()
popup_menu.add_command(label='Очистить все', underline=7, command=clearall)
popup_menu.add_command(label='Выбрать все', underline=7, command=selectall)
content_text.bind('<Button-3>', show_popup_menu)

######################   Строка состояния  ############### ############################

status_bar = ttk.Label(root, text="Строки")
status_bar.pack(side=tk.BOTTOM)

text_changed = False

def changed(event=None):
    global text_changed
    if content_text.edit_modified():
        text_changed = True
        words = len(content_text.get(1.0, "end-1c").split())
        characters = len(content_text.get(1.0, "end-1c"))
        status_bar.config(text=f'Символов : {characters}  Слов : {words}')
    content_text.edit_modified(False)
content_text.bind("<<Modified>>", changed)
url = ""


# Обработка привязки
content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)
content_text.bind('<Control-A>',selectall)
content_text.bind('<Control-a>',selectall)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Control-f>',find_text)
content_text.bind("<Control-B>",bold_it)
content_text.bind("<Control-b>",bold_it)
content_text.bind("<Control-I>",italics_it)
content_text.bind("<Control-i>",italics_it)
content_text.bind("<Control-U>",change_underline)
content_text.bind("<Control-u>",change_underline)

content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()
#############################################################################################################

root.protocol('WM_DELETE_WINDOW', exit_editor)

mainloop()
