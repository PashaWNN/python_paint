from tkinter import PhotoImage


def _safe_put(img, x, y):
    if x < 0 or y < 0:
        return
    img.put('#000000', (x, y))


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
        pass

    @classmethod
    def handle_motion(cls, x, y, img):
        print(x, y)
        _safe_put(img, x, y)

    @classmethod
    def handle_release(cls, x, y, img):
        pass


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

        dx = x2 - x1
        dy = y2 - y1

        for x in range(min(x1, x2), max(x1, x2)):
            y = int(y1 + dy * (x - x1) / dx)
            _safe_put(img, x, y)

    @classmethod
    def handle_release(cls, x, y, img):
        pass


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

        x = 0
        y = ry

        # Initial decision parameter of region 1  
        d1 = ((ry * ry) - (rx * rx * ry) +
              (0.25 * rx * rx))
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y

        # For region 1  
        while (dx < dy):

            # Print points based on 4-way symmetry  
            _safe_put(img, x + xc, y + yc)
            _safe_put(img, -x + xc, y + yc)
            _safe_put(img, x + xc, -y + yc)
            _safe_put(img, -x + xc, -y + yc)

            # Checking and updating value of  
            # decision parameter based on algorithm  
            if (d1 < 0):
                x += 1
                dx = dx + (2 * ry * ry)
                d1 = d1 + dx + (ry * ry)
            else:
                x += 1
                y -= 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d1 = d1 + dx - dy + (ry * ry)

                # Decision parameter of region 2  
        d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) +
              ((rx * rx) * ((y - 1) * (y - 1))) -
              (rx * rx * ry * ry))

        # Plotting points of region 2  
        while (y >= 0):

            # printing points based on 4-way symmetry  
            _safe_put(img, x + xc, y + yc)
            _safe_put(img, -x + xc, y + yc)
            _safe_put(img, x + xc, -y + yc)
            _safe_put(img, -x + xc, -y + yc)

            # Checking and updating parameter  
            # value based on algorithm  
            if (d2 > 0):
                y -= 1
                dy = dy - (2 * rx * rx)
                d2 = d2 + (rx * rx) - dy
            else:
                y -= 1
                x += 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d2 = d2 + dx - dy + (rx * rx)

    @classmethod
    def handle_release(cls, x, y, img):
        pass


tools_list = [Pencil, Line, Oval]