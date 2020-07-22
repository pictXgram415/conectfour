import tkinter as tk
from PIL import Image, ImageTk as itk
import time
import threading
import socket

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400


class GridClass(tk.Frame):
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400
    IMG_RED_STR = "./netopro/conectFour/images/RED_COIN.png"
    IMG_YEL_STR = "./netopro/conectFour/images/YELLOW_COIN.png"
    IMG_BLANK_STR = "./netopro/conectFour/images/BLANK.png"
    STATUS_STR = ["red", "yellow", "th"]
    deeps = {}
    opponentName = ""
    stage = True
    role = 0  # 0:server ,1:client

    def __init__(self, c0, pMaster, role, myName):
        super().__init__()
        self.IMG_RED = self.read_image(self.IMG_RED_STR)
        self.IMG_YEL = self.read_image(self.IMG_YEL_STR)
        self.IMG_BLANK = self.read_image(self.IMG_BLANK_STR)
        self.c0 = c0
        self.currentTag = 3
        self.turnMaster = -1
        self.pMaster = pMaster  # parent master
        self.opponent = -1
        self.role = role

        for i in range(7):
            self.deeps[i] = 6
        for y in range(7):
            for x in range(7):
                self.make_cell(x, y)
        if role == 0:
            self.connect_client(myName)
            self.game_server()
        else:
            self.connect_server(myName)
            self.game_client()

    def game_server(self):
        if self.stage:
            if self.turnMaster == 0:
                self.stage = False
                # print("y")
                self.turnMaster = 1
                self.server_send()
                self.opponent = self.server_recv()
                self.opponent_y(self.opponent)
            elif self.turnMaster == 1 or self.turnMaster == -1:
                self.stage = False
                # print("r")
                self.turnMaster = 0
                self.start_game_r()
        try:
            self.after(500, self.game_server)
        except:
            pass

    def game_client(self):
        if self.stage:
            if self.turnMaster == 0:
                self.stage = False
                print("y")
                self.turnMaster = 1
                self.start_game_y()
            elif self.turnMaster == 1 or self.turnMaster == -1:
                self.stage = False
                print("r")
                if self.turnMaster != -1:
                    self.client_send()
                self.turnMaster = 0
                self.opponent = self.client_recv()
                self.opponent_r(self.opponent)

        try:
            self.after(500, self.game_client)
        except:
            pass

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
        enter['command'] = lambda: [self.choice_cell()]
        rightArrow = tk.Button(bottomButtons)
        rightArrow['text'] = u'→右へ'
        rightArrow['command'] = self.move_right
        bottomButtons.pack(pady=10)
        leftArrow.pack(side='left', padx=10)
        enter.pack(side='left', padx=10)
        rightArrow.pack(side='left', padx=10)
        extra = tk.Button(root)

    def start_game_r(self):
        self.currentTag = 3
        self.change_red(self.currentTag)

    def start_game_y(self):
        self.currentTag = 3
        self.change_yel(self.currentTag)

    def opponent_r(self, tag):
        self.currentTag = tag
        self.set_stage(False)
        self.choice_cell()

    def opponent_y(self, tag):  # currentTagの値だけもらえばできる
        # time.sleep(1)
        self.currentTag = tag
        self.set_stage(False)
        self.choice_cell()

    def set_status(self, num):
        self.turnMaster = num

    def set_stage(self, flg):
        self.stage = flg

    def change_red(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_RED)

    def change_yel(self, tag):
        self.c0.itemconfig(str(tag)+"th", image=self.IMG_YEL)

    def clear(self, tag):
        self.c0.itemconfig(str(tag)+'th', image=self.IMG_BLANK)

    def move_left(self):
        if 0 < self.currentTag and self.turnMaster in range(2):
            self.clear(self.currentTag)
            self.currentTag -= 1
            if self.role == 0:
                self.change_red(self.currentTag)
            else:
                self.change_yel(self.currentTag)

    def move_right(self):
        if self.currentTag < 6 and self.turnMaster in range(2):
            self.clear(self.currentTag)
            self.currentTag += 1
            if self.role == 0:
                self.change_red(self.currentTag)
            else:
                self.change_yel(self.currentTag)

    def choice_cell(self):
        if self.deeps[self.currentTag] > 0 and not self.stage:
            self.stage = True
            p = self.currentTag + self.deeps[self.currentTag] * 7
            if self.turnMaster == 0:
                # print("red")
                self.change_red(p)
            elif self.turnMaster == 1:
                # print("yel")
                self.change_yel(p)
            self.clear(self.currentTag)
            self.deeps[self.currentTag] -= 1
            self.c0.itemconfigure(
                str(p) + 'th', tags=str(p) + self.STATUS_STR[self.turnMaster])
            if self.isCheck_win():
                if self.role == 0:
                    self.server_send()
                else:
                    self.client_send()
                winWindow = tk.Toplevel()
                winWindow.geometry("200x100")
                winWindow.title(self.STATUS_STR[self.turnMaster]+"win")
                tk.Label(
                    winWindow, text=self.STATUS_STR[self.turnMaster]+u'が勝利しました').pack()
                b = tk.Button(winWindow, text="閉じる", command=lambda: [
                              winWindow.destroy(), self.pMaster.destroy(), self.set_status(None), self.del_sockets()])
                b.pack()

                self.turnMaster = 2
            if self.isCheck_full():
                if self.role == 0:
                    self.server_send()
                else:
                    self.client_send()
                winWindow = tk.Toplevel()
                winWindow.geometry("200x100")
                winWindow.title("draw")
                tk.Label(
                    winWindow, text=u'引き分けました').pack()
                b = tk.Button(winWindow, text="閉じる", command=lambda: [
                              winWindow.destroy(), self.pMaster.destroy(), self.set_status(None).self.del_sockets()])
                b.pack()

                self.turnMaster = 2

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
            if self.c0.find_withtag(str(p)+self.STATUS_STR[self.turnMaster]):
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
            if self.c0.find_withtag(str(p)+self.STATUS_STR[self.turnMaster]):
                check = check * 1 + 1
            else:
                check = check * 0 + 0
            if check == 4:
                return True
        return False

    def isCheck_slash(self, axis):  # axis=1:右下がりaxis=-1:右上がり
        col = self.currentTag
        row = self.deeps[self.currentTag]+1
        check = 0
        p = col+row*7
        bottom = (6-row)*(7+axis)+p
        mem = {}
        for i in range(7):
            mem[bottom % 7] = bottom
            bottom = bottom - 7 + axis * -1
        for i in range(7):
            p = mem[i]
            if self.c0.find_withtag(str(p) + self.STATUS_STR[self.turnMaster]):
                check = check * 1 + 1
            else:
                check = check * 0 + 0
            if check == 4:
                return True
        return False

    def isCheck_full(self):
        count = 0
        for i in range(7):
            for j in range(7):
                p = j + i * 7
                if self.c0.find_withtag(str(p) + self.STATUS_STR[2]):
                    count += 1
        print(count)
        if count <= 7:
            return True
        else:
            return False

    def connect_client(self, myName):
        print("start server")
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 9999
        self.serversocket.bind((host, port))
        self.serversocket.listen(1)
        print('waiting connection...')
        self.clientsocket, addr = self.serversocket.accept()
        print("Got a connection from %s" % str(addr))
        msg = 'Thank you for connecting' + "\r\n"
        self.clientsocket.send(msg.encode('utf-8'))
        self.opponentName = self.clientsocket.recv(1024)
        self.opponentName = self.opponentName.decode('utf-8')
        self.clientsocket.send(myName.encode("utf-8"))
        self.clientInput = -1

    def server_send(self):
        msg = str(self.currentTag)
        self.clientsocket.send(msg.encode("utf-8"))

    def server_recv(self):
        self.clientInput = self.clientsocket.recv(1024)
        self.clientInput = self.clientInput.decode('utf-8')
        self.clientInput = int(self.clientInput)
        return self.clientInput

    def del_serversocket(self):
        self.clientsocket.close()
        self.serversocket.close()

    def connect_server(self, myName):
        print("start client")
        host = "localhost"
        port = 9999
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.connect((host, port))
        print("connect")
        msg = self.serversocket.recv(1024)
        print(msg.decode("utf-8"))
        self.serversocket.send(myName.encode("utf-8"))
        msg = self.serversocket.recv(1024)
        print("opponentName>>", end="")
        msg = msg.decode("utf-8")
        print(msg)
        self.opponentName = msg
        self.clientInput = ""

    def client_send(self):
        msg = str(self.currentTag)
        self.serversocket.send(msg.encode("utf-8"))

    def client_recv(self):
        self.clientInput = self.serversocket.recv(1024)
        self.clientInput = self.clientInput.decode("utf-8")
        print(self.clientInput)
        self.clientInput = int(self.clientInput)
        return self.clientInput

    def del_clientsocket(self):
        self.serversocket.close()

    def del_sockets(self):
        if self.role == 0:
            self.del_serversocket()
        else:
            self.del_clientsocket()


def start():
    root = tk.Tk()
    root.title('test')
    root.geometry("600x450")
    c0 = tk.Canvas(root, width=CANVAS_WIDTH+1,
                   height=CANVAS_HEIGHT+1, bg='yellow')
    c0.pack()
    gl = GridClass(c0, root, 1, "yyyyy")

    gl.show_buttons(root)
    root.mainloop()


if __name__ == '__main__':

    start()
