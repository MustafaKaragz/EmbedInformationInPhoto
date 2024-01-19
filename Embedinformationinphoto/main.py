import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import secrets
import string
from stegano import lsb

                                        # MUSTAFA KARAGÖZ #

def generate_random_key(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for i in range(length))

def save_key_to_file(key, file_name="secret_key.txt"):
    with open(file_name, 'w') as file:
        file.write(key)

def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_index = 0
    for char in plain_text:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            key_index += 1

            shift = ord(key_char.upper()) - ord('A')
            if char.isupper():
                encrypted_text += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))
            elif char.islower():
                encrypted_text += chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
        else:
            encrypted_text += char

    return encrypted_text

def polybius_encrypt(text):
    polybius_square = [['A', 'B', 'C', 'D', 'E'],
                       ['F', 'G', 'H', 'I', 'K'],
                       ['L', 'M', 'N', 'O', 'P'],
                       ['Q', 'R', 'S', 'T', 'U'],
                       ['V', 'W', 'X', 'Y', 'Z']]

    encrypted_text = ""
    for char in text.upper():
        if char.isalpha():
            if char == 'J':
                char = 'I'
            for i in range(5):
                for j in range(5):
                    if polybius_square[i][j] == char:
                        encrypted_text += str(i + 1) + str(j + 1)
        else:
            encrypted_text += char

    return encrypted_text

def convert_tc_to_letters(tc_num):
    tc_letter_map = {
        '0': 'A', '1': 'B', '2': 'C', '3': 'D',
        '4': 'E', '5': 'F', '6': 'G', '7': 'H',
        '8': 'K', '9': 'L'
    }
    return ''.join(tc_letter_map[digit] for digit in tc_num)


def add_text_to_image(image, texts, key):
    draw = ImageDraw.Draw(image)
    width, height = image.size
    margin = 10


    positions = [(margin, margin), (margin, height - margin), (width - margin, margin)]

    text_color = (255, 255, 255, 255)

    for i, text in enumerate(texts):
        if i == 2:
            text = convert_tc_to_letters(text)
        encrypted_text = polybius_encrypt(vigenere_encrypt(text, key))
        text_width, text_height = draw.textbbox((0, 0), encrypted_text)[2:]

        position = positions[i]
        if i == 1:
            position = (position[0], position[1] - text_height)
        elif i == 2:
            position = (position[0] - text_width, position[1])

        draw.text(position, encrypted_text, fill=text_color)

def hide_message(image_path, texts, key, output_path):
    img = Image.open(image_path)
    add_text_to_image(img, texts, key)


    for text in texts:
        encrypted_text = polybius_encrypt(vigenere_encrypt(text, key))
        img = lsb.hide(img, encrypted_text)

    img.save(output_path)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.surname_label = tk.Label(self, text="Surname:")
        self.surname_label.pack()
        self.surname_entry = tk.Entry(self)
        self.surname_entry.pack()

        self.tc_label = tk.Label(self, text="SSNNo:")
        self.tc_label.pack()
        self.tc_entry = tk.Entry(self)
        self.tc_entry.pack()


        self.upload_button = tk.Button(self, text="UploadImage", command=self.upload_image)
        self.upload_button.pack()

        self.start_button = tk.Button(self, text="Encryption", command=self.start_hiding)
        self.start_button.pack()

    def upload_image(self):
        self.image_path = filedialog.askopenfilename()
        self.show_image(self.image_path)

    def show_image(self, path):
        img = Image.open(path)
        img.thumbnail((100, 100))
        self.img = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self, image=self.img)
        self.img_label.pack()

    def start_hiding(self):
        key = generate_random_key()
        save_key_to_file(key)

        messages = [
            self.name_entry.get(),
            self.surname_entry.get(),
            self.tc_entry.get()
        ]

        output_path = "image_with_secret_message.png"
        hide_message(self.image_path, messages, key, output_path)
        messagebox.showinfo("Success", "Messages are hidden and saved.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()