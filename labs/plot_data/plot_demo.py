import os
import sys
import json
import time
import datetime
import serial
import threading
import matplotlib.pyplot as plt
import seaborn as sns

from queue import Queue


from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph.opengl as gl
import pyqtgraph as pg

# define plot curve
global curve1,curve2

### define a global queue
global data_queue
data_queue = Queue()


class SerialCollect(object):
    def __init__(self,port,baudrate = 115200):
        try:
            self._s = serial.Serial(port=port,baudrate=baudrate,timeout=1)
        except serial.SerialException:
            print("open serial error.")
            exit(0)
        self._left_flag = b'{'
        self._right_flag = b'}'
        self._packs = bytes()
    def recv(self):
        print('begin recving data...')
        while True:
            data = self._s.read(8192)
            if not data:
                # print('fails to read data.')
                self._packs = b''
                time.sleep(1)
                continue
            self._packs = self._packs + data
            while True:
                #find the pack head flag
                left_index = self._packs.find(self._left_flag)
                right_index = self._packs.find(self._right_flag)
                #parse data
                if left_index >= 0 and right_index >=0 and right_index > left_index:
                    pack_data = self._packs[left_index:right_index+1]
                    # print(len(pack_data))
                    # print(pack_data.decode())
                    # data_queue.put(eval(pack_data))
                    data_queue.put(json.loads(pack_data))

                    self._packs = self._packs[right_index+1:]
                else:
                    # if left_index < 0:
                    #     self._packs = b''
                    break

def plot():
    print("start plot")
    time.sleep(0.03)

    org_wave = []
    rpm_wave = []

    while True:
        if data_queue.empty():
            time.sleep(0.01)
            continue
        else:
            t = ''
            devid = ''
            fm = 0
            ver = ''
            dist = 0
            data = data_queue.get()
            t = datetime.datetime.fromtimestamp(int(data['t'])).strftime('%Y-%m-%d %H:%M:%S') if 't' in data.keys() else '--'
            devid = data['deviId'] if 'deviId' in data.keys() else '--'
            ver = data['version'] if 'version' in data.keys() else '--'
            dist = data['d'] if 'd' in data.keys() else '--'
            fm = data['fm'] if 'fm' in data.keys() else '--'
            rpm = data['r'] if 'r' in data.keys() else '--'
            e = data['e'] if 'e' in data.keys() else 0



            if 'rw' in data.keys() and 'rcw' in data.keys():
                org_wave = data['rw']
                rpm_wave = data['rcw']


            print('dev:{},time:{},exist:{},fast move:{},distance:{},rpm:{},versoion:{}'.format(devid,t,e,fm,dist,rpm,ver))

            curve1.setData(org_wave)
            curve2.setData(rpm_wave)

            #update plot immediate
            QtGui.QApplication.processEvents()


def main():
    recv = SerialCollect("/dev/tty.usbmodem14301")
    collect = threading.Thread(target=recv.recv)
    collect.setDaemon(True)
    collect.start()
    

    global curve1,curve2

    # Set graphical window, its title and size
    win = pg.GraphicsLayoutWidget(show=True)
    win.resize(1500,600)
    win.setWindowTitle('plot data')

    pg.setConfigOptions(antialias=True)

    p1 = win.addPlot(title="org wave")
    curve1 = p1.plot(pen='r')
    p1.setLabels(left='amplitude', bottom='frame')

    win.nextRow()
    p2 = win.addPlot(title="rpm wave")
    curve2 = p2.plot(pen='r')
    p2.setLabels(left='amplitude', bottom='frame')

    #timer = QtCore.QTimer()
    #a = timer.timeout.connect(plot)
    #timer.start(30)
    
    plot_thread = threading.Thread(target=plot)
    plot_thread.setDaemon(True)
    plot_thread.start()



    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    main()
