import tkinter as tk
import random

class GridApp:
    """Grid Base"""
    show_text = False
    def __init__(self, root):
        self.root = root
        self.root.title("NeuronGrowthSim")

        self.canvas = tk.Canvas(root, width=800, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(expand=True, anchor="center")

        self.canvas.pack()

        self.rows = 500
        self.columns = 800
        self.cell_width = 1
        self.cell_height = 1

        self.loop_interval = 1
        self.start_loop()

    def draw_gridbox(self, x, y):
        x1 = x * self.cell_width
        y1 = y * self.cell_height
        x2 = x1 + self.cell_width
        y2 = y1 + self.cell_height
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")

        if not GridApp.show_text:
            text_x = 400
            text_y = 400
            self.canvas.create_text(text_x, text_y, text="Text unterhalb", anchor="center")
            GridApp.show_text = True

    def start_loop(self):
        self.root.after(self.loop_interval, self.loop)

    def loop(self):
        self.draw_gridbox(random.randint(0, 800), random.randint(0, 500))
        self.start_loop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GridApp(root)
    root.mainloop()
