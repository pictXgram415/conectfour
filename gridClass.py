import tkinter as tk
from PIL import Image, ImageTk as itk
import time
import threading

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400


class GridClass():
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    IMG_RED_STR = "./netopro/conectFour/images/RED_COIN.png"
    IMG_YEL_STR = "./netopro/conectFour/images/YELLOW_COIN.png"
    IMG_BLANK_STR = "./netopro/conectFour/images/BLANK.png"
    STATUS_STR = ["red", "yellow", "blank"]
    deeps = {}
    stage = True

    def __init__(self, c0, pMaster, status):
        super().__init__()
        self.IMG_RED = self.read_image(self.IMG_RED_STR)
        self.IMG_YEL = self.read_image(self.IMG_YEL_STR)
        self.IMG_BLANK = self.read_image(self.IMG_BLANK_STR)
        self.c0 = c0
        self.currentTag = 3
        self.status = -1  # 0:red,1:yel,2:fin
        self.pMaster = pMaster  # parent master
        self.threadGame = None
        for i in range(7):
            self.deeps[i] = 6
        for y in range(7):
            for x in range(7):
                self.make_cell(x, y)
        self.game()

    def game(self):
        self.stage = False
        if self.status == 0:
            print("y")
            self.status = 1
            self.start_game_y()
        elif self.status == 1 or self.status == -1:
            print("r")
            self.status = 0
            self.start_game_r()

    def test(self):
        print("test")

    def game_thread(self):
        if not self.threadGame:
            self.threadGame = threading.Thread(target=self.game)
            self.threadGame.start()
            print("start")
        else:
            self.threadGame.join()
            self.threadGame = None
            print("end")

    def make_cell(self, x, y):
        x1 = x * self.CANVAS_HEIGHT / 7 + 2
        y1 = y * self.CANVAS_HEIGHT / 7 + 2
        num = x + y * 7
        self.c0.create_rectangle(x1, y1, x1 + self.CANVAS_HEIGHT/7, y1 +
                                 self.CANVAS_HEIGHT / 7, fill='white', tags='cell')

        self.c0.create_image(x1, y1, image=self.IMG_BLANK,
                             tags=str(num) + 'th', anchor=tk.NW)

    def read_image(self, img):
        imageOpen = Image.open(img)
        imageOpen = imageOpen.resize(
            (int(self.CANVAS_HEIGHT/7), int(self.CANVAS_HEIGHT/7)))
        image = itk.PhotoImage(imageOpen)
        return image

    def show_buttons(self, root):
        bottomButtons = tk.Frame(root)
        leftArrow = tk.Button(bottomButtons)
        leftArrow['text'] = u'←左へ'
        leftArrow['command'] = self.move_left
        enter = tk.Button(bottomButtons)
        enter['text'] = u'決定'
        enter['command'] = self.choice_cell
        rightArrow = tk.Button(bottomButtons)
        rightArrow['text'] = u'→右へ'
        rightArrow['command'] = self.move_right
        bottomButtons.pack(pady=10)
        leftArrow.pack(side='left', padx=10)
        enter.pack(side='left', padx=10)
        rightArrow.pack(side='left', padx=10)

    def start_game_r(self):
        self.change_red(self.currentTag)

    def start_game_y(self):  # currentTagの値だけもらえばできる
        time.sleep(1)
        self.currentTag = 1
        self.choice_cell()

    def get_status(self):
        return self.status

    def change_red(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_RED)

    def change_yel(self, tag):
        self.c0.itemconfig(str(tag)+"th", image=self.IMG_YEL)

    def clear(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_BLANK)

    def move_left(self):
        if 0 < self.currentTag and self.status < 2:
            self.clear(self.currentTag)
            self.currentTag -= 1
            self.change_red(self.currentTag)

    def move_right(self):
        if self.currentTag < 6and self.status < 2:
            self.clear(self.currentTag)
            self.currentTag += 1
            self.change_red(self.currentTag)

    def choice_cell(self):
        if self.deeps[self.currentTag] > 0:
            self.stage = True
            p = self.currentTag + self.deeps[self.currentTag] * 7
            if self.status == 0:
                self.change_red(p)
            elif self.status == 1:
                self.change_yel(p)
            self.clear(self.currentTag)
            self.deeps[self.currentTag] -= 1
            self.c0.itemconfigure(
                str(p) + 'th', tags=str(p) + self.STATUS_STR[self.status])
            if self.isCheck_win():

                winWindow = tk.Toplevel()
                winWindow.geometry("200x100")
                winWindow.title(self.STATUS_STR[self.status]+"win")
                tk.Label(
                    winWindow, text=self.STATUS_STR[self.status]+u'が勝利しました').pack()
                b = tk.Button(winWindow, text="閉じる", command=lambda: [
                              winWindow.destroy(), self.pMaster.destroy()])
                b.pack()

                self.status = 2
            self.currentTag = 3
            # self.game_thread()

    def isCheck_win(self):
        if self.isCheck_row() or self.isCheck_col() or self.isCheck_slash(1) or self.isCheck_slash(-1):
            return True
        else:
            return False

    def isCheck_row(self):
        row = self.deeps[self.currentTag]+1
        check = 0
        for i in range(7):
            p = i + row * 7
            if self.c0.find_withtag(str(p)+self.STATUS_STR[self.status]):
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
            if self.c0.find_withtag(str(p)+self.STATUS_STR[self.status]):
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
            if self.c0.find_withtag(str(p)+self.STATUS_STR[self.status]):
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
    gl = GridClass(c0, root, 0)
    # gl.set_images('./netopro/conectFour/images/RED_COIN.png')
    # gl.set_images("./netopro/conectFour/images/YELLOW_COIN.png")

    gl.show_buttons(root)
    root.mainloop()
