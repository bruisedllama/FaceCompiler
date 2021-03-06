from ImageEyes import *
from shiftImagesBySquare import *
import numpy as np
import cv2 as cv2
import math
#first the driver calls shiftImageByEyes and passes in the already processed base , in the case that it recognizes zero eyes, there are a bunch of return zeroes which you can trace
#it will then call shiftImageBySquare and to not compute the baseImage detection all the time, we get the 
def shiftImageByEyes(frompath, basepath, topath):
    image = ImageEyes(frompath)
    crash = adjustAngle(image)
    if(crash==0):
        basepath = basepath.fileName
        basepath = Image(basepath)
        shiftImageBySquare(frompath,basepath,topath)
    adjustImage(image)
    createImage(topath, baseimage, image)

def adjustAngle(image):
    midpoints = image.midpoints
    if(midpoints ==0):
        return 0
    xDiff = midpoints[0][0] - midpoints[1][0]
    yDiff = midpoints[0][1] - midpoints[1][1]
    angle = np.arctan(yDiff/xDiff)
    h= image.image.shape[0]
    w = image.image.shape[1]
    R = cv2.getRotationMatrix2D((h/2,w/2),(angle * 180 / math.pi),1)
    rotated = cv2.warpAffine(image.image,R,(h,w)) #change to (w,h) for no change landscape to portrait
    image.setImage(rotated)

def getDistanceRatio(image1, image2):
    return image1.distance / image2.distance


def adjustImage(toAdjust):
    ratio = getDistanceRatio(baseimage, toAdjust)
    img = toAdjust.image

    width = int(img.shape[1] * ratio)
    height = int(img.shape[0] * ratio)
    img = cv2.resize(img, (width, height))
    toAdjust.setImage(img)
    toAdjust.update()
    cv2.imwrite("newImage.jpg", toAdjust.image)

def createImage(topath, baseImage, image1):
    wh = baseImage.imgParameters()
    width = wh[0]
    height = wh[1]
    blankImage = np.zeros((height, width, 3), np.uint8)
    midpointBase = baseImage.getMidpointOfLine()
    midpointImage = image1.getMidpointOfLine()

    xDifference = midpointBase[0] - midpointImage[0]
    yDifference = midpointBase[1] - midpointImage[1]
    wh1 = image1.imgParameters()
    width1 = wh1[0]
    height1 = wh1[1]
    print(blankImage.shape)
    print(image1.image.shape)
    print(width1, height1)
    for xcoord in range(0, width):
        for ycoord in range(0, height):
            oldx = int(xcoord - xDifference)
            oldy = int(ycoord - yDifference)
            if oldy >= 0 and oldx >= 0 and oldy<height1 and oldx<width1:
                blankImage[ycoord][xcoord] = image1.image[oldy][oldx]
    cv2.imwrite(topath, blankImage)
