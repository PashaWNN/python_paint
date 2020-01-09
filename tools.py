from algorhitms import ellipse, bresenham_line, flood_fill


class Tool:
    auto_clear = True

    @classmethod
    def handle_press(cls, x, y, img):
        pass

    @classmethod
    def handle_motion(cls, x, y, img):
        pass

    @classmethod
    def handle_release(cls, x, y, img):
        pass


class Pencil(Tool):
    auto_clear = False

    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['last_x'] = x
        img.ctx['last_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        bresenham_line(img.ctx['last_x'], img.ctx['last_y'], x, y, img.put_pixel)

        img.ctx['last_x'] = x
        img.ctx['last_y'] = y


class Line(Tool):
    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['start_x'] = x
        img.ctx['start_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        x2, y2 = x, y
        x1, y1 = img.ctx['start_x'], img.ctx['start_y']
        bresenham_line(x1, y1, x2, y2, img.put_pixel)


class Oval(Tool):
    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['start_x'] = x
        img.ctx['start_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        xc, yc = img.ctx['start_x'], img.ctx['start_y']
        rx = abs(xc - x)
        ry = abs(yc - y)
        ellipse(rx, ry, xc, yc, img.put_pixel)


class Bucket(Tool):
    auto_clear = False
    @classmethod
    def handle_press(cls, x, y, img):
        current_color = img.get_pixel(x, y)
        flood_fill(x, y, img.put_pixel,
                   compare_pixel=lambda i, j: img.get_pixel(i, j) == current_color,
                   width=img.width(),
                   height=img.height())


tools_list = [Pencil, Line, Oval, Bucket]
