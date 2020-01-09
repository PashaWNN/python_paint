from tkinter import Tk, Label, PhotoImage, TclError
import pygubu
from tools import tools_list


class Application:
    def __init__(self, master):
        self.img_width = 400
        self.img_height = 400
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('ui.ui')
        self.main_window = builder.get_object('container', master)
        self.tools = self.builder.get_object('tools')
        self.widths = self.builder.get_object('widths')
        self.canvas = self.builder.get_object('canvas')
        self._pressed = False
        self.init_ui()
        self.color = 'red'
        self.current_tool = None
        self.current_width = None
        self._current_preview = None
        self.image = PhotoImage(width=self.img_width, height=self.img_height)
        self.init_canvas()

    def init_canvas(self):
        self.canvas.create_image(self.img_width // 2, self.img_height // 2,
                                 image=self.image, state='normal', tag='result')
        self.image.put('#555555', (1,2))
        self.image.put('#555555', (1, 3))
        self.image.put('#555555', (1, 4))
        self.image.put('#555555', (1, 5))
        self.image.put('#555555', (1, 6))

        self.canvas.bind('<Button-1>', self.handle_canvas)
        self.canvas.bind('<B1-Motion>', self.handle_canvas)
        self.canvas.bind('<ButtonRelease-1>', self.handle_canvas)

    def _blank_preview(self):
        if self._current_preview is not None:
            self._current_preview.blank()
            self._current_preview.pixels = []

    def _prepare_preview_object(self):
        img = PhotoImage(width=self.img_width, height=self.img_height)
        img.ctx = {}
        img.pixels = []

        def put_pixel(x, y):
            if x < 0 or y < 0:
                return
            img.put(self.color, (x, y))
            img.pixels.append((self.color, (x, y)))

        def clear():
            img.blank()
            img.pixels = []

        def get_pixel(x, y):
            local = img.get(x, y)
            return local if not local == (0, 0, 0) else self.image.get(x, y)

        img.put_pixel = put_pixel
        img.clear = clear
        img.get_pixel = get_pixel
        self.canvas.create_image(self.img_width // 2, self.img_height // 2, image=img, state='normal', tag='preview')
        self._current_preview = img

    def commit_to_canvas(self):
        for pixel in self._current_preview.pixels:
            self.image.put(*pixel)
        previews = self.canvas.find_withtag('preview')
        self._blank_preview()
        for p in previews:
            self.canvas.delete(p)

    def handle_canvas(self, event):
        if not self.current_tool:
            return
        x, y = event.x, event.y
        if str(event.type) == 'ButtonPress':
            self._prepare_preview_object()
            self.current_tool.tool.handle_press(x, y, self._current_preview)
            self._pressed = True
        elif str(event.type) == 'ButtonRelease':
            self.current_tool.tool.handle_release(x, y, self._current_preview)
            self.commit_to_canvas()
            self._current_preview = None
            self._pressed = False
        elif str(event.type) == 'Motion' and self._pressed:
            if self.current_tool.tool.auto_clear:
                self._blank_preview()
            self.current_tool.tool.handle_motion(x, y, self._current_preview)

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
