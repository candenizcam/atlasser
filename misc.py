import numpy as np
import matplotlib.pyplot as plt
import os


class ImageFile:
    def __init__(self, text):
        ts0 = text.split("/")
        ts1 = ts0[-1].split(".")
        self.type = ts1[1]
        if self.type != "png":
            print("WARNING input files are not .png")
        ts2 = ts1[0].split("-")
        self.index = ts2[1]
        self.name = ts2[0]
        self.image = plt.imread(text)


class AtlasMaker:
    def __init__(self, input_dir="inputs"):
        self.filename = input("enter filename: ")
        self.header = "%s.png\n" \
                      "size: %d, %d\n" \
                      "format: RGBA8888\n" \
                      "filter: Linear,Linear\n" \
                      "repeat: none\n"
        self.images = self.get_images(input_dir)
        self.h, self.w = self.h_w_finder(self.images)
        self.header = self.header % (self.filename, self.w, self.h)
        self.canvas, self.full_string = self.canvas_merger()
        self.outputter()

    def outputter(self):
        f = open("output/%s.atlas" % self.filename, "w")
        f.write(self.full_string)
        f.close()
        plt.imsave("output/%s.png" % self.filename, self.canvas)

    @staticmethod
    def get_images(input_dir):
        files = os.listdir(input_dir)
        return [ImageFile("%s/%s" % (input_dir, i)) for i in files]

    @staticmethod
    def h_w_finder(f):
        h = 0
        w = 0
        for i in f:
            h += i.image.shape[0]
            w = max(w, i.image.shape[1])
        return h, w

    def canvas_merger(self):
        canvas = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        y = 0
        strings = []
        for x, i in enumerate(self.images):
            h = i.image.shape[0]
            w = i.image.shape[1]
            canvas[y:y + h, 0:w, :] += i.image
            s = "%s\n" \
                "   rotate: false\n" \
                "   xy: %d, %d\n" \
                "   size: %d, %d\n" \
                "   orig: %d, %d\n" \
                "   offset: 0, 0\n" \
                "   index: %d"
            s2 = s % (i.name, 0, y, w, h, w, h, x)
            strings.append(s2)
            y += h
        full_string = self.header + "\n".join(strings)
        return canvas, full_string


if __name__ == "__main__":
    a = AtlasMaker()

