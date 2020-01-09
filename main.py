from tkinter import Tk, Canvas, Label, PhotoImage
import pygubu
from tools import tools_list


class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui.ui')
        self.main_window = builder.get_object('container', master)
        self.tools = self.builder.get_object('tools')
        self.widths = self.builder.get_object('widths')
        self.canvas = self.builder.get_object('canvas')
        self._pressed = False
        self.init_ui()
        self.current_tool = None
        self.current_width = None
        self.canvas.stack = []
        self.canvas.bind('<Button-1>', self.handle_canvas)
        self.canvas.bind('<B1-Motion>', self.handle_canvas)
        self.canvas.bind('<ButtonRelease-1>', self.handle_canvas)

    def handle_canvas(self, event):
        if not self.current_tool:
            return
        x, y = event.x, event.y
        if str(event.type) == 'ButtonPress':
            img = PhotoImage(width=400, height=400)
            img.ctx = {}
            self.canvas.create_image(200, 200, image=img, state='normal')
            self.canvas.stack.append(img)
            self.canvas.current_editing = img
            self.current_tool.tool.handle_press(x, y, img)
            self._pressed = True
        elif str(event.type) == 'ButtonRelease':
            self.current_tool.tool.handle_release(x, y, self.canvas.current_editing)
            self.canvas.current_editing = None
            self._pressed = False
        elif str(event.type) == 'Motion' and self._pressed:
            x, y = event.x, event.y
            self.current_tool.tool.handle_motion(x, y, self.canvas.current_editing)

    def select_tool(self, event):
        self._select_accessory('tool', event)

    def select_width(self, event):
        self._select_accessory('width', event)

    def _select_accessory(self, accessory, event):
        lbl = event.widget
        if getattr(self, f'current_{accessory}'):
            getattr(self, f'current_{accessory}')['relief'] = 'raised'
        lbl['relief'] = 'sunken'
        setattr(self, f'current_{accessory}', lbl)

    def init_ui(self):
        for tool in tools_list:
            img = PhotoImage(file=f'images/{tool.__name__.lower()}_tool.gif')
            lbl = Label(self.tools, relief='raised', image=img)
            lbl.img = img
            lbl.tool = tool
            lbl.bind('<Button-1>', self.select_tool)
            lbl.pack()

        for width in range(1, 7):
            img = PhotoImage(file=f'images/{width}.gif')
            lbl = Label(self.widths, relief='raised', image=img)
            lbl.img = img
            lbl.value = width
            lbl.bind('<Button-1>', self.select_width)
            lbl.pack(padx=6)


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()
