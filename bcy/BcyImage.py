# encoding: utf-8

class BcyImage(object):

    def __init__(self, title="", bigImage="", image="", author=""):
        self.title = title
        self.bigImage = bigImage
        self.image = image
        self.author = author

    def __str__(self):
        return "[title:" + self.title + ",bigImage:" + self.bigImage + ",author:" + self.author + "]"
