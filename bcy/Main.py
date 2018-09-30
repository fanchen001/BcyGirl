# coding=utf-8
from bcy.PythonNode import *
from bcy.FacePP import *
from bcy.BcyImage import *

url = "https://bcy.net/coser/toppost100?type=lastday"
string = Stream.url2String(url, header=Stream.httpHeader("https://bcy.net/"))
node = PythonNode(string)
nodes = node.list("ul.l-clearfix.gridList.smallCards.js-workTopList > li > a")
imgs = []
for n in nodes:
    href = "https://bcy.net" + n.href()
    bcyString = Stream.url2String(href, header=Stream.httpHeader("https://bcy.net/", True))
    print("proc -> " + href + " success")
    bcyNode = PythonNode(bcyString)
    bcyNodes = bcyNode.list("article > img")
    for nn in bcyNodes:
        bcy = BcyImage()
        bcy.title = bcyNode.text("title")
        bcy.image = nn.src()
        bcy.bigImage = nn.src().replace("/w650", "")
        bcy.author = bcyNode.text("div > a > span")
        imgs.append(bcy)

for img in imgs:
    image = img.image
    face = FacePP(image)
    face.detect()
    if face.isGirl() and face.isBeauty():
        dir = "D:\\Bcy\\漂亮妹子\\" + img.author
    elif face.isGirl() and not face.isBeauty():
        dir = "D:\\Bcy\\普通妹子\\" + img.author
    elif not face.isGirl() and face.isBeauty():
        dir = "D:\\Bcy\\帅气汉子\\" + img.author
    else:
        dir = "D:\\Bcy\\普通汉子\\" + img.author
    Stream.mkDir(dir)
    split = img.bigImage.split("/")
    file = dir + "\\" + split[len(split) - 1]
    byte = Stream.url2Byte(img.bigImage)
    Stream.byte2File(byte, file)
    print("download -> " + img.bigImage + " success")
