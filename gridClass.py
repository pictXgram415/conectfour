import tkinter as tk
from PIL import Image, ImageTk as itk
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400


def make_cell(x, y, img, c0):
    x1 = x * CANVAS_HEIGHT/7+2
    y1 = y * CANVAS_HEIGHT/7+2
    c0.create_rectangle(x1, y1, x1 + CANVAS_HEIGHT/7, y1 +
                        CANVAS_HEIGHT/7, fill='white', tags='cell')
    c0.create_image(x1, y1, image=img, tag="coin", anchor=tk.NW)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('test')
    root.geometry("800x450")
    c0 = tk.Canvas(root, width=CANVAS_WIDTH+1,
                   height=CANVAS_HEIGHT+1, bg='yellow')
    c0.pack()
    imageOpen = Image.open(
        './netopro/conectFour/images/RED_COIN.png')
    imageOpen = imageOpen.resize((int(CANVAS_HEIGHT/7), int(CANVAS_HEIGHT/7)))
    image = itk.PhotoImage(imageOpen)
    for x in range(7):
        for y in range(7):
            make_cell(x, y, image, c0)

    root.mainloop()
