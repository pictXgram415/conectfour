import tkinter as tk
from PIL import Image, ImageTk as itk
from connectFour import Application


class Start(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.title("start")
        master.geometry("300x200")
        self.pack()
        self.show_message()
        self.input_name()
        self.show_connect_button()

    def show_message(self):
        self.message = tk.Label(self)
        self.message['text'] = u'相手に表示する名前を入力してください'
        self.message.pack()

    def input_name(self):
        self.inputName = tk.Entry(self)
        self.inputName.insert(tk.END, "ななしの18FI")
        self.inputName.pack(padx=10, pady=10)

    def show_connect_button(self):
        self.connectButton = tk.Button(self)
        self.connectButton['text'] = u'接続する'
        self.connectButton['command'] = self.correct_button
        self.connectButton.pack()

    def correct_button(self):
        myName = self.inputName.get()
        self.master.destroy()
        root = tk.Tk()
        game = Application(myName, 1, master=root)
        game.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = Start(master=root)
    app.mainloop()
