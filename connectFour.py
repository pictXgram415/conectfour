import tkinter as tk
from PIL import Image, ImageTk as itk
from gridClass import GridClass


class Application(tk.Frame):

    def __init__(self, myName, role, master=None):
        super().__init__(master)
        master.title("game")
        master.geometry("650x500")

        self.master = master
        self.role = role
        self.myName = myName
        self.textCol = 0

        self.CANVAS_WIDTH = 400
        self.CANVAS_HEIGHT = 400

        self.gameFrame = tk.Frame(self)
        self.sideFrame = tk.Frame(self)

        self.pack()
        self.gameFrame.pack(side='left')
        self.show_opponent_name()
        self.game_scene()
        self.show_buttons()
        # self.sideFrame.pack(side='left', padx=10)
        # self.show_log_name()
        # self.show_log_text()

    ###
    # gameFrame
    ###

    def game_scene(self):
        self.c0 = tk.Canvas(self.gameFrame, width=self.CANVAS_WIDTH+1,
                            height=self.CANVAS_HEIGHT+1, bg='yellow')
        self.c0.pack(pady=5)
        self.gc = GridClass(self.c0, self.master, self.role, self.myName)
        self.label['text'] = u'相手：'+self.gc.opponentName+u'さん'

    def show_opponent_name(self):
        self.label = tk.Label(self.gameFrame)
        #self.label['text'] = u'相手：'+self.gc.opponentName+u'さん'
        self.label.pack(pady=5)

    def show_buttons(self):
        self.bottomButtons = tk.Frame(self.gameFrame)
        leftArrow = tk.Button(self.bottomButtons)
        leftArrow['text'] = u'←左へ'
        leftArrow['command'] = self.gc.move_left
        enter = tk.Button(self.bottomButtons)
        enter['text'] = u'決定'

        enter['command'] = lambda: [
            self.gc.choice_cell()]
        rightArrow = tk.Button(self.bottomButtons)
        rightArrow['text'] = u'→右へ'
        rightArrow['command'] = self.gc.move_right
        self.bottomButtons.pack(pady=10)
        leftArrow.pack(side='left', padx=10)
        enter.pack(side='left', padx=10)
        rightArrow.pack(side='left', padx=10)
    ###
    # sideFrame
    ###

    def show_log_name(self):
        self.logName = tk.Label(self.sideFrame)
        self.logName['text'] = u'ログ'
        self.logName.pack(pady=5)

    def show_log_text(self):
        self.c1 = tk.Canvas(self.sideFrame, width=self.CANVAS_WIDTH/2,
                            height=self.CANVAS_HEIGHT*2)
        self.c1.pack(pady=5)
        self.c1.create_rectangle(2, 2, self.CANVAS_WIDTH/2,
                                 self.CANVAS_HEIGHT, fill='white', tag='baseSheet')
        for i in range(5):
            self.logs('test')

    def logs(self, log):
        self.c1.create_text(5, self.textCol * 20 + 2, text=log, anchor=tk.NW)
        self.textCol += 1


###
# mainWindow
###


def start():
    root = tk.Tk()
    app = Application("yyyy", 0, master=root)
    app.mainloop()


if __name__ == "__main__":
    start()
