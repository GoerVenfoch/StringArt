import os
from PIL import Image, ImageDraw
import math

# from kivy.clock import Clock
# from kivy.uix.popup import Popup


class GSA:
    def __init__(self, image_path, num_pins, num_lines, num_thread):
        self.image = Image.open(image_path)
        self._filename = os.path.splitext(os.path.basename(image_path))[0]
        self.num_points = num_pins
        self.num_lines_end = num_lines
        self._point_list = []
        self._lines_list = []
        # self._weight_image = self.image.size[0] * self.image.size[1] * 255
        self._weight_thread = num_thread

    def convert_gray(self):
        self.image = self.image.convert("L")

    def get_min_side(self):
        width, height = self.image.size
        return min(width, height)

    def put_mask(self):
        mask = Image.new("L", self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        diameter = self.get_min_side()
        draw.pieslice((0, 0, diameter, diameter), start=0, end=360, fill=255)
        result = Image.new('L', self.image.size)
        result.paste(self.image, mask=mask)
        self.image = result

    def init_points_list(self):
        angle = 2 * math.pi / self.num_points
        radius = self.get_min_side()/2 - 1

        for i in range(self.num_points):
            x = int(radius + radius * math.cos(i * angle))
            y = int(radius + radius * math.sin(i * angle))
            self._point_list.append((x, y))

    # def search_weigth_image(self):
    #     width, height = self.image.size
    #
    #     for y in range(height):
    #         for x in range(width):
    #             pixel = self.image.getpixel((x, y))
    #             self._weight_image -= pixel

    def build_lines_list(self, progress_bar):
        start_point = self._point_list[0]
        # end = self._weight_image * (0.60 - 1 / self._weight_thread)
        # dt = 100 / self.num_lines_end
        for i in range(self.num_lines_end):
            print(i)
            progress_bar.update_progress(1)
            end_point = self.search_line(start_point)
            self._lines_list.append((start_point, end_point))
            start_point = end_point

    def search_line(self, start):
        max_score = 0
        point = None

        for i in self._point_list:
            if i is start:
                continue
            line_pixels = alg_brezenhem(start, i)
            weight = sum((255 - self.image.getpixel(pixel)) for pixel in line_pixels)
            score = weight / len(line_pixels)
            if score > max_score:
                max_score = score
                point = i
        self.event_edit_line_pixsel(start, point)
        return point

    def event_edit_line_pixsel(self, start, end):
        line_pixels = alg_brezenhem(start, end)
        for y in line_pixels:
            pixel = self.image.getpixel(y)
            new_pixel = max(pixel + self._weight_thread, 0)
            self.image.putpixel(y, new_pixel)
            # self._weight_image -= self.image.getpixel(y) - pixel

    def write_file(self):
        with open(self._filename, 'w') as file:
            file.write(str(self.num_points) + ".0")
            for i in self._lines_list:
                file.write("," + str(self._point_list.index(i[1])))


def alg_brezenhem(start_point, end_point):
    x0, y0 = start_point
    x1, y1 = end_point

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    line_pixels = []

    while True:
        line_pixels.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    return line_pixels


def generate_sa(image_path, num_pins, num_lines, num_thread, progress_bar):
    print("Task started")
    my_object = GSA(image_path, num_pins, num_lines, num_thread)
    my_object.put_mask()
    my_object.init_points_list()
    # my_object.search_weigth_image()
    my_object.build_lines_list(progress_bar)
    my_object.write_file()
    progress_bar.update_progress(10)
