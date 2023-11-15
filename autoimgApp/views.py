from django.shortcuts import render
import cv2
import numpy as np
import base64
from rembg import remove
import random as rdnnnn
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import autoimgApp.password as password
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from autoimgApp.models import ContactMessage, WorkingDB
import os
import threading
import time

seg = SelfiSegmentation()
randdomList = [1,2,3,4,5,6]

caceDD = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

deletExtraImagesRUNNINGstatus = True

def deletExtraImages():
    global deletExtraImagesRUNNINGstatus
    time.sleep(15)
    if deletExtraImagesRUNNINGstatus:
        deletExtraImagesRUNNINGstatus = False
        mainDir = "./media/FileDBFolder"
        allfiles = os.listdir(mainDir)
        for file in allfiles:
            created = os.path.getctime(f"{mainDir}/{file}")
            if((datetime.fromtimestamp(created)+timedelta(minutes=5)) < datetime.now()):
                os.remove(f"{mainDir}/{file}")
        WorkingData = WorkingDB.objects.all()
        WorkingData[len(WorkingData)-2].delete()
        deletExtraImagesRUNNINGstatus = True



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
        try:
            file = request.FILES['picture']
            WorkingData = WorkingDB(selectFile=file)
            WorkingData.save()
            main_URL = WorkingData.selectFile.url
            img = cv2.imread(f"./media{main_URL}")
            h, w, c = img.shape
            needSize = int(request.POST.get('q-select'))

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
            if(request.POST.get('removequality')=="normal" or request.POST.get('removequality')=="advence"):
                # print("Working..................")
                cropedImg = seg.removeBG(cropedImg, (blueC,greenC,redC), cutThreshold=0.6)
                cv2.imwrite(f"./media{main_URL.replace('.', 'cropped')}.jpg", cropedImg)
            elif(request.POST.get('removequality')=="advence"):
                # print("Working..................")
                fileLocationCode = int(rdnnnn.choice(randdomList))
                op = remove(cropedImg)
                cv2.imwrite(f"xxxxxxxx{fileLocationCode}.png", op)
                cropedImg = cv2.imread(f"xxxxxxxx{fileLocationCode}.png")
                cropedImg = seg.removeBG(cropedImg, (blueC,greenC,redC), cutThreshold=0.6)
                cv2.imwrite(f"./media{main_URL.replace('.', 'cropped')}.png", cropedImg)
            else:
                cv2.imwrite(f"./media{main_URL.replace('.', 'cropped')}.jpg", cropedImg)


            cv2.imwrite(f"./media{main_URL.replace('.', 'facedetection')}.jpg", imgCopy)
            sendData = {
                "img": main_URL,
                "facedetected": f"{main_URL.replace('.', 'facedetection')}.jpg",
                "cropeImage": f"{main_URL.replace('.', 'cropped')}.jpg",
                "needSize": needSize
            }
            t1 = threading.Thread(target=deletExtraImages)
            t1.start()

            return render(request, 'index.html', sendData)
        except:
            return render(request, 'index.html', {"errorMsg":"Please give a valid image!"})
    return render(request, 'index.html')
         






def about(request):
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')





def contact(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email3 = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        dateee = datetime.today()
        cmsgdb = ContactMessage(fullname=fullname, email=email3, phone=phone, subject=subject, message=message, dateee=dateee)
        cmsgdb.save()
        senderEmail = password.senderEmailId()
        ePassword = password.emailPassword()
        receiverEmail = password.recverEmailId()
        # receiverEmail = "systemready2014@gmail.com"
        messagee = MIMEMultipart("alternative")
        messagee["Subject"] = f"GooBusinesses Contact Message form {fullname}"
        messagee["From"] = senderEmail
        messagee["To"] = receiverEmail

        htmlHead = """<html>
        <head>
            <style>
                *{
                    margin: 0;
                    padding: 0;
                }
                .header{
                    background-color: #417690;;
                    width: 100vw;
                    height: 54px;
                }
                h1{
                    color: green;
                    margin: 10px;
                }
                .data{
                    color: blueviolet;
                }
                
                .subjectcl{
                    text-align:center;
                    margin: 5px 0px;
                    color:green;
                }
                .msg{
                    margin:3px 0px;
                }
            </style>
        </head>"""
        htmlBody = f"""
                    <body>
                <div class="header"></div>
                <h1>Hi Welcome to Goo Businesses</h1>
                    <h3><span>Date: </span><span class="data">{dateee}</span></h3>
                    <h3><span>Name: </span><span class="data">{fullname}</span></h3>
                    <h3><span>Phone: </span><span class="data">{phone}</span></h3>
                    <h3><span>Email: </span><span class="data">{email3}</span></h3>
                    <h2 class="data subjectcl">{subject}</h2>
                    <pre class="msg">{message}</pre>
            </body>
        </html>
                """
        html = htmlHead + htmlBody
        part2 = MIMEText(html, "html")
        messagee.attach(part2)
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(senderEmail, ePassword)
                server.sendmail(senderEmail, receiverEmail, messagee.as_string())
                # emailStatus = 'Email also successfully received.....'
                # print('Success......')
        except:
            pass
        return render(request, 'contact.html', {'backmsg': 'Message sent successfully'})
        
    return render(request, 'contact.html')