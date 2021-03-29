import psutil

from flask import Flask, render_template, Response
#from gpiozero import CPUTemperature

from subprocess import check_output
import os
import cv2
import socket 
import io 

vc = cv2.VideoCapture(0) 
app = Flask(__name__)
#app.debug = True # Uncomment to debug

@app.route('/')
def home():
    #temp=temp()
    return render_template("index.html", cpu=cpu(), memory=memory(), disk=disk(), temp=50, ip=ipaddr(), video = gen())


@app.route('/video')
def video():
    #temp=temp()
    return render_template("index.html", cpu=cpu(), memory=memory(), disk=disk(), temp=50, ip=ipaddr(), video = gen())


@app.route('/video_feed') 
def video_feed(): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 

def gen(): 
   """Video streaming generator function.""" 
   while True: 
       rval, frame = vc.read() 
       cv2.imwrite('pic.jpg', frame) 
       yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n') 


def cpu():
    return str(psutil.cpu_percent()) + '%'

def ipaddr():
    #ipadd = check_output(['hostname', '-I'])
    ipadd="1211515"
    return ipadd

def memory():
    memory = psutil.virtual_memory()
    # Divide from Bytes -> KB -> MB
    available = round(memory.available/1024.0/1024.0,1)
    total = round(memory.total/1024.0/1024.0,1)
    return str(available) + 'MB free / ' + str(total) + 'MB total ( ' + str(memory.percent) + '% )'

#def temp():
    #return str(CPUTemperature().temperature) + "C"

def disk():
    disk = psutil.disk_usage('/')
    # Divide from Bytes -> KB -> MB -> GB
    free = round(disk.free/1024.0/1024.0/1024.0,1)
    total = round(disk.total/1024.0/1024.0/1024.0,1)
    return str(free) + 'GB free / ' + str(total) + 'GB total ( ' + str(disk.percent) + '% )'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)