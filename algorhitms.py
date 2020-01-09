def ellipse(rx, ry, xc, yc, callback):
    """Draw and ellipse"""
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
        callback(x + xc, y + yc)
        callback(-x + xc, y + yc)
        callback(x + xc, -y + yc)
        callback(-x + xc, -y + yc)

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
        callback(x + xc, y + yc)
        callback(-x + xc, y + yc)
        callback(x + xc, -y + yc)
        callback(-x + xc, -y + yc)

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


def naive_line(x1, y1, x2, y2, callback):
    """Draw a line with naive algorithm"""
    dx = x2 - x1
    dy = y2 - y1

    for x in range(min(x1, x2), max(x1, x2)):
        y = int(y1 + dy * (x - x1) / dx)
        callback(x, y)


def bresenham_line(x1, y1, x2, y2, callback):
    dx = x2 - x1
    dy = y2 - y1

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        callback(x1 + x * xx + y * yx, y1 + x * xy + y * yy)
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy


def flood_fill(x, y, set_pixel, compare_pixel, width, height):
    to_fill = set()

    def add(i, j):
        if compare_pixel(i, j):
            to_fill.add((i, j))

    add(x, y)

    while to_fill:
        (x, y) = to_fill.pop()
        if not compare_pixel(x, y):
            continue
        set_pixel(x, y)
        print(len(to_fill))
        if 0 < x:
            add(x - 1, y)
        if x < width:
            add(x + 1, y)
        if y > 0:
            to_fill.add((x, y - 1))
        if y < height:
            to_fill.add((x, y + 1))
