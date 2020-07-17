import tkinter as tk
from PIL import Image, ImageTk as itk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("game")
        master.geometry("600x400")
        self.grid()
        self.show_label()
        # self.create_widgets()
        # self.show_image()

    def create_widgets(self):
        self.test = tk.Button(self)
        self.test['text'] = u"test"
        self.test['width'] = 50
        #self.test['command'] = self.show_image
        self.test.pack()

    def text_box(self):
        self.editBox = tk.Entry(self)
        self.editBox['width'] = 60
        self.editBox.insert(tk.END, "defoult")
        self.editBox.pack()

    def show_image(self):
        imageOpen = Image.open(
            'Y:/kuso/netproPy/netopro/conectFour/images/RED_COIN.png')
        imageOpen = imageOpen.resize((25, 25))
        self.image = itk.PhotoImage(
            imageOpen)
        self.frame = tk
        for x in range(7):
            for y in range(6):
                self.canvas = tk.Canvas(
                    self,
                    width=30,
                    height=30,
                )
                self.canvas.grid(column=x, row=y)
                self.canvas.create_image(
                    5,
                    5,
                    image=self.image,
                    tag="illust",
                    anchor=tk.NW
                )
                self.canvas.grid()

    def show_label(self):
        self.label = tk.Label(self)
        self.label['text'] = u'test'
        self.label.grid()


root = tk.Tk()

app = Application(master=root)
app.mainloop()
