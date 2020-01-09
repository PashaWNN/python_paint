from algorhitms import ellipse, bresenham_line


def _safe_put(img, x, y, color='#000000'):
    if x < 0 or y < 0:
        return
    img.put(color, (x, y))


class Tool:
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
    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['last_x'] = x
        img.ctx['last_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        def callback(x, y):
            _safe_put(img, x, y)

        bresenham_line(img.ctx['last_x'], img.ctx['last_y'], x, y, callback)

        img.ctx['last_x'] = x
        img.ctx['last_y'] = y


class Line(Tool):
    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['start_x'] = x
        img.ctx['start_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        img.blank()
        x2, y2 = x, y
        x1, y1 = img.ctx['start_x'], img.ctx['start_y']

        def callback(x, y):
            _safe_put(img, x, y)

        bresenham_line(x1, y1, x2, y2, callback)


class Oval(Tool):
    @classmethod
    def handle_press(cls, x, y, img):
        img.ctx['start_x'] = x
        img.ctx['start_y'] = y

    @classmethod
    def handle_motion(cls, x, y, img):
        img.blank()
        xc, yc = img.ctx['start_x'], img.ctx['start_y']
        rx = abs(xc - x)
        ry = abs(yc - y)

        def callback(x, y):
            _safe_put(img, x, y)

        ellipse(rx, ry, xc, yc, callback)


tools_list = [Pencil, Line, Oval]
