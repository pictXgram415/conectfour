import tkinter as tk
from PIL import Image, ImageTk as itk

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400


class GridClass():
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    IMG_RED_STR = "./netopro/conectFour/images/RED_COIN.png"
    IMG_YEL_STR = "./netopro/conectFour/images/YELLOW_COIN.png"
    IMG_BLANK_STR = "./netopro/conectFour/images/BLANK.png"
    deeps = {}
    mycoins = {}

    def __init__(self, c0):
        super().__init__()
        self.IMG_RED = self.read_image(self.IMG_RED_STR)
        self.IMG_YEL = self.read_image(self.IMG_YEL_STR)
        self.IMG_BLANK = self.read_image(self.IMG_BLANK_STR)
        self.c0 = c0
        self.currentTag = 3
        for i in range(7):
            self.deeps[i] = 6
        for y in range(7):
            for x in range(7):
                self.make_cell(x, y)
        self.start_game_r()

    def make_cell(self, x, y):
        x1 = x * self.CANVAS_HEIGHT / 7 + 2
        y1 = y * self.CANVAS_HEIGHT / 7 + 2
        num = x + y * 7
        self.c0.create_rectangle(x1, y1, x1 + self.CANVAS_HEIGHT/7, y1 +
                                 self.CANVAS_HEIGHT / 7, fill='white', tags='cell')

        self.c0.create_image(x1, y1, image=self.IMG_BLANK,
                             tags=str(num) + 'th', anchor=tk.NW)
        self.mycoins[num] = 0

    def read_image(self, img):
        imageOpen = Image.open(img)
        imageOpen = imageOpen.resize(
            (int(self.CANVAS_HEIGHT/7), int(self.CANVAS_HEIGHT/7)))
        image = itk.PhotoImage(imageOpen)
        return image

    def show_buttons(self, root):
        self.bottomButtons = tk.Frame(root)
        leftArrow = tk.Button(self.bottomButtons)
        leftArrow['text'] = u'←左へ'
        leftArrow['command'] = self.move_left
        enter = tk.Button(self.bottomButtons)
        enter['text'] = u'決定'
        enter['command'] = lambda: self.choice_cell()
        rightArrow = tk.Button(self.bottomButtons)
        rightArrow['text'] = u'→右へ'
        rightArrow['command'] = self.move_right
        self.bottomButtons.pack(pady=10)
        leftArrow.pack(side='left', padx=10)
        enter.pack(side='left', padx=10)
        rightArrow.pack(side='left', padx=10)

    def change_red(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_RED)

    def change_yel(self, tag):
        self.c0.itemconfig(str(tag)+"th", image=self.IMG_YEL)

    def clear(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_BLANK)

    def start_game_r(self):
        self.change_red(self.currentTag)

    def move_left(self):
        if 0 < self.currentTag:
            self.clear(self.currentTag)
            self.currentTag -= 1
            self.change_red(self.currentTag)

    def move_right(self):
        if self.currentTag < 6:
            self.clear(self.currentTag)
            self.currentTag += 1
            self.change_red(self.currentTag)

    def choice_cell(self):
        if self.deeps[self.currentTag] > 0:
            p = self.currentTag+self.deeps[self.currentTag]*7
            self.change_red(p)
            self.clear(self.currentTag)
            self.deeps[self.currentTag] -= 1
            self.c0.itemconfigure(str(p) + 'th', tags=str(p) + 'red')
            if self.isCheck_win():
                print("win")
            self.currentTag = 3
            self.start_game_r()

    def isCheck_win(self):
        if self.isCheck_row() or self.isCheck_col() or self.isCheck_slash(1) or self.isCheck_slash(-1):
            return True
        else:
            return False

    def isCheck_row(self):
        row = self.deeps[self.currentTag]+1
        check = 0
        for i in range(7):
            p = i + row*7
            if self.c0.find_withtag(str(p)+"red"):
                check = check * 1 + 1
            else:
                check = check * 0 + 0
            if check == 4:
                return True
        return False

    def isCheck_col(self):
        col = self.currentTag
        check = 0
        for i in reversed(range(7)):
            p = i * 7 + col
            if self.c0.find_withtag(str(p)+"red"):
                check = check * 1 + 1
            else:
                check = check * 0 + 0
            if check == 4:
                return True
        return False

    def isCheck_slash(self, axis):  # axis=1:右下がりaxis=-1:右上がり
        count = 0
        col = self.currentTag
        row = self.deeps[self.currentTag]+1
        check = 0
        for i in reversed(range(7)):
            p = i * 7 + col-(6-row) - count
            count += axis
            if self.c0.find_withtag(str(p)+"red"):
                check = check * 1 + 1
            else:
                check = check * 0 + 0
            if check == 4:
                return True
        return False


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry("800x450")
    c0 = tk.Canvas(root, width=CANVAS_WIDTH+1,
                   height=CANVAS_HEIGHT+1, bg='yellow')
    c0.pack()
    gl = GridClass(c0)
    # gl.set_images('./netopro/conectFour/images/RED_COIN.png')
    # gl.set_images("./netopro/conectFour/images/YELLOW_COIN.png")

    gl.show_buttons(root)
    root.mainloop()
