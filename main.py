import cv2
from math import *
import numpy as np
 
def getWrapImage(img, matRotation, width, height):
    print("img shape:",img.shape)
    m0 = matRotation[0,0]
    m1 = matRotation[0,1]
    m2 = matRotation[0,2]
    m3 = matRotation[1,0]
    m4 = matRotation[1,1]
    m5 = matRotation[1,2]
    img_ = np.zeros((width,height,3))
    for k in range(img.shape[2]):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                tmpx = int(m0 * i + m1 * j + m2);
                tmpy = int(m3 * i + m4 * j + m5);
                if(tmpx <width and tmpy <height):
                    img_[tmpx,tmpy,k] = img[i,j,k]
    return img_

def dumpRotateImage(img,degree):
 
    height, width = img.shape[:2]
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width//2, height//2), degree, 1)
    print(matRotation)
    matRotation[0,2] += (widthNew - width)//2
    matRotation[1,2] += (heightNew - height)//2
    print(matRotation)
    imgRotation = cv2.warpAffine(img, matRotation,(widthNew,heightNew),borderValue=(255,255,255))
 
    matRotation2 = cv2.getRotationMatrix2D((widthNew//2, heightNew//2), degree, 1)
    # imgRotation2 = cv2.warpAffine(img, matRotation2, (widthNew, heightNew), borderValue=(255, 255, 255))
    imgRotation2 = getWrapImage(img, matRotation2, widthNew, heightNew)
    return imgRotation,imgRotation2, matRotation
 
 
def draw_box(img,box):
    cv2.line(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 3)
    cv2.line(img, (box[0], box[1]), (box[4], box[5]), (0, 255, 0), 3)
    cv2.line(img, (box[2], box[3]), (box[6], box[7]), (0, 255, 0), 3)
    cv2.line(img, (box[4], box[5]), (box[6], box[7]), (0, 255, 0), 3)
    return img

image = cv2.imread('/Users/austinjing/Documents/Aye/RotateImage/test.jpg')
imgRotation, imgRotation2, matRotation = dumpRotateImage(image, 15)
box = [200,250,250,200,230,280,280,230]
 
reverseMatRotation = cv2.invertAffineTransform(matRotation)
pt1 = np.dot(reverseMatRotation,np.array([[box[0]],[box[1]],[1]]))
pt2 = np.dot(reverseMatRotation,np.array([[box[2]],[box[3]],[1]]))
pt3 = np.dot(reverseMatRotation,np.array([[box[4]],[box[5]],[1]]))
pt4 = np.dot(reverseMatRotation,np.array([[box[6]],[box[7]],[1]]))
 
#print(pt1, pt2, pt3, pt4)
box2 = [pt1[0],pt1[1],pt2[0],pt2[1],pt3[0],pt3[1],pt4[0],pt4[1]]
 
cv2.imwrite('/Users/austinjing/Documents/Aye/RotateImage/drawBox.jpg',draw_box(imgRotation,box))
cv2.imwrite('/Users/austinjing/Documents/Aye/RotateImage/raw.png',draw_box(image,box2))
