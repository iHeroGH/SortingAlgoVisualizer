from tkinter import *
from tkinter.ttk import *

import random

from Sorter import Sorter
from Event import Event

import time

class Render:
    def __init__(self, algo = "bubble", title = "SortVis", width = 0, height = 0, n = 100):

        self.window = self.create_window(width, height, title)
        self.canvas = self.create_canvas()

        self.list_to_sort = [n for n in range(0, n)]
        random.shuffle(self.list_to_sort)

        #self.list_to_sort = Sorter.generate_random_list(1000, 0, 10)

        #self.list_to_sort = [math.sin(math.radians(i)) for i in range(0, 50)]
        self.sorter = Sorter(self.list_to_sort)
        self.rectangles = self.get_rects()

        self.bind_keys()

        self.main_loop(algo)

    def main_loop(self, algorithm="bubble", sleep: int = 0):

        algorithm_generator = {
            "bubble": self.sorter.bubble_sort, # 1:24
            "insertion": self.sorter.insertion_sort, # :30
            "selection": self.sorter.selection_sort, # ?
            "quick": self.sorter.quick_sort, # :19
            "bogo": self.sorter.bogo_sort,
            "bozo": self.sorter.bozo_sort,
            "shuffle": self.sorter.shuffle_list
        }[algorithm]

        #print(self.list_to_sort, self.events, self.rectangles, sorted)

        for event in algorithm_generator():
            print(event)
            if not isinstance(event, Event):
                continue

            first_index, second_index = event.first, event.second
            first_rect, second_rect = self.rectangles[first_index], self.rectangles[second_index]
            color = event.color

            self.change_colors(first_rect, second_rect, color)

            if event.type == "swap":
                self.swap_rect_positions(first_rect, second_rect)
                self.rectangles = Sorter.swap(self.rectangles, first_index, second_index)

            time.sleep(sleep or event.time)

            if not event.keep:
                self.change_colors(first_rect, second_rect)

    def swap_rect_positions(self, first_rect, second_rect):
        first_x = self.canvas.coords(first_rect)[0]
        second_x = self.canvas.coords(second_rect)[0]

        self.canvas.move(first_rect, second_x-first_x, 0)
        self.canvas.move(second_rect, first_x-second_x, 0)

    def change_colors(self, first_rect, second_rect = None, color = 'white'):
        self.canvas.itemconfig(first_rect, fill=color)

        if second_rect:
            self.canvas.itemconfig(second_rect, fill=color)

        self.update_window()

    def update_window(self):
        self.window.update_idletasks()
        self.window.update()

    def create_window(self, width, height, title = "GUI"):
        window = Tk(className=title)

        self.screen_width, self.screen_height = self.get_screen_size(window)
        self.width, self.height = self.fix_dimensions(width, height)

        if self.width == 0 and self.height == 0:
            self.enter_fullscreen(window)
            self.width, self.height = self.screen_width, self.screen_height
        else:
            window.geometry(f"{int(self.width)}x{int(self.height)}+0+0")

        return window

    def fix_dimensions(self, width, height):

        width, height = max(0, width), max(0, height)
        width, height = min(width, self.screen_width), min(height, self.screen_height)

        if height and not width:
            width = self.screen_width
        if width and not height:
            height = self.screen_height

        return width, height

    def get_screen_size(self, window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    def create_canvas(self):
        canvas = Canvas(
            self.window, width = self.width, height = self.height, highlightthickness=0
            )
        canvas.grid()
        canvas.configure(bg='black')

        return canvas

    def get_rects(self):

        if not (self.list_to_sort and self.sorter):
            self.list_to_sort = Sorter.generate_random_list(self.width, 0, self.height)
            self.sorter = Sorter(self.list_to_sort)

        self.canvas.delete("all")
        self.rect_width = self.width / len(self.list_to_sort)
        max_height = max(self.list_to_sort)

        rectangles = []
        for n, height in enumerate(self.list_to_sort):

            curr_ratio = height / max_height
            curr_height = curr_ratio * (self.height-10)

            rect_id = self.canvas.create_rectangle(
                n * self.rect_width, self.height - curr_height, (n+1) * self.rect_width, self.height + 1, fill="white", width=0
            )

            rectangles.append(rect_id)

        return rectangles

    def enter_fullscreen(self, window = None):
        window = window or self.window
        window.attributes("-fullscreen", True)

    def escape_fullscreen(self, window = None):
        window = window or self.window
        window.attributes("-fullscreen", False)
        window.state("zoomed")

    def bind_keys(self):
        self.window.bind('<F11>', lambda event: self.enter_fullscreen())
        self.window.bind('<Escape>', lambda event: self.escape_fullscreen())

if __name__ == "__main__":
    render = Render("Sorter")
