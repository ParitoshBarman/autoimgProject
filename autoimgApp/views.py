from django.shortcuts import render
import cv2
import numpy as np
import base64
from rembg import remove
import random as rdnnnn
from cvzone.SelfiSegmentationModule import SelfiSegmentation
seg = SelfiSegmentation()
randdomList = [1,2,3,4,5,6]

caceDD = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def getBase64Image(img):
    image_np = np.array(img)
    base64_image = base64.b64encode(cv2.imencode('.png', image_np)[1]).decode()
    return f"data:image/png;base64,{base64_image}"

# Create views here.
def index(request):
    if request.method == 'POST':
        # img = data_uri_to_cv2_img(f"data:image/png;base64,{request.POST.get('pictureBase')}")
        img = data_uri_to_cv2_img(f"{request.POST.get('pictureBase')}")
        h, w, c = img.shape
        needSize = 800
        if(h>needSize or w>needSize):
            img = cv2.resize(img, (int(needSize), int((h*needSize)/w)))

        imgCopy = img.copy()
        gray = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2GRAY)
        faces = caceDD.detectMultiScale(gray, 1.1, 4)
        prviosH = 0
        prviosW = 0
        prviosx = 0
        prviosy = 0
        for (x, y, H, W) in faces:
            cv2.rectangle(imgCopy, (x, y), (x+W, y+H), (0, 0, 255), 3)
            if(prviosH<H and prviosW<W):
                prviosH = H
                prviosW = W
                prviosx = x
                prviosy = y
            # break
        H = prviosH
        W = prviosW
        x = prviosx
        y = prviosy
        start1 = y-int(H*(1/2))
        if start1<0:
            start1 = 0
        start2 = x-int(W*(1/3))
        if start2<0:
            start2 = 0
        end1 = y+H+int(H*(1/2))
        if end1>h:
            end1 = h
        end2 = x+W+int(W*(1/3))
        if end2>w:
            end2 = w
        cropedImg = img[start1:end1, start2:end2]

        redC, greenC, blueC = hex_to_rgb(request.POST.get('color'))
        # if(request.POST.get('bgchek')=="on"):
        if(request.POST.get('removequality')=="normal"):
            print("Working..................")
            cropedImg = seg.removeBG(cropedImg, (blueC,greenC,redC), cutThreshold=0.6)
        elif(request.POST.get('removequality')=="advence"):
            print("Working..................")
            fileLocationCode = int(rdnnnn.choice(randdomList))
            op = remove(cropedImg)
            cv2.imwrite(f"xxxxxxxx{fileLocationCode}.png", op)
            cropedImg = cv2.imread(f"xxxxxxxx{fileLocationCode}.png")
            cropedImg = seg.removeBG(cropedImg, (blueC,greenC,redC), cutThreshold=0.6)



        sendData = {
            "img": getBase64Image(img),
            "facedetected": getBase64Image(imgCopy),
            "cropeImage": getBase64Image(cropedImg)
        }

        return render(request, 'index.html', sendData)

    return render(request, 'index.html')
         