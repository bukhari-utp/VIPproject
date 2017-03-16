# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author:Julián Sibaja García, 
        Karolay Ardila Salazar,
        Dayán Mendez Vasquez,
        Jorge Silva Correa,
"""
from scipy import signal
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import json
import sqlite3

n = raw_input("Digite el numero de la prueba: ")
conn = sqlite3.connect('database.db') #connection object
c = conn.cursor()
c.execute('''select * from '''+"s"+n)
data = c.fetchall()
dic = {'AF3':[],'AF4':[],'F3':[],'F4':[],'F7':[],'F8':[],'FC5':[],'FC6':[],'T7':[],'T8':[],'P7':[],'P8':[],'O1':[],'O2':[]}

for row in data:
    dic['AF3'].append(row[2])
    dic['AF4'].append(row[3])
    dic['F3'].append(row[4])
    dic['F4'].append(row[5])
    dic['F7'].append(row[6])
    dic['F8'].append(row[7])
    dic['FC5'].append(row[8])
    dic['FC6'].append(row[9])
    dic['T7'].append(row[10])
    dic['T8'].append(row[11])
    dic['P7'].append(row[12])
    dic['P8'].append(row[13])
    dic['O1'].append(row[14])
    dic['O2'].append(row[15])
data = dic
fs = 128.0
ts = 1/fs
time = np.arange(0,len(data['AF3']) * ts,ts)
lst = ['AF3','AF4','F3','F4','F7','F8','FC5','FC6','T7','T8','P7','P8','O1','O2',]
index = list(xrange(len(data)))

k = 1
while k == 1:
  for key in lst:

    #Data vs time 
    plt.figure()
    plt.subplot(211)
    plt.plot(time,data[key])
    plt.ylabel('Sensor value')
    plt.xlabel('Time [sec]')
    plt.title(key)
    plt.grid()

    #Spectrogram 
    plt.subplot(212)
    f, t, Sxx, im = plt.specgram(data[key], NFFT=128, Fs=128,noverlap=100)
    plt.show()
    savefig(key + '.png', dpi = 300)
  k = 0
conn.close()
print "done"

"""
#Example of a signal
pi = np.pi
ph = 0
amp = 10
freq = 200
time = 1
fs = 1000
ts = 1.0/fs
time = np.arange(0,time,ts)
y = np.sin(2*pi*freq*time+ph)
"""
