# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Julián Sibaja García,
         Karolay Ardila Salazar,
         Dayán Mendez Vasquez,
         Jorge Silva Correa,

Tipos de prueba:
  r - relajación
  mrh - mover la mano derecha
  mlh - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo

"""
from scipy import signal
import numpy as np
import scipy.io as sio
import matplotlib.pylab as plt

def getDataFromDB(id_s):
    mat_contents = sio.loadmat(id_s)
    conc = mat_contents['conc']
    rel = mat_contents['rel']
    conc = np.transpose(conc, (2, 1, 0))
    rel = np.transpose(rel, (2, 1, 0))
    return conc, rel


def butter_filter(data, lowcut=3, highcut=25, fs=500, order=6): # Filter
    nyq = 0.5*fs
    high = highcut/nyq
    [b, a] = signal.butter(order, high, btype='low')
    y = signal.lfilter(b, a, data)
    return y

def removeDC(data):
    ndata = np.zeros(np.shape(data))
    mean_v = np.mean(data, axis=2)
    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            # Señal original -  señal DC
            v_trial = (data[trial][electrode] - mean_v[trial][electrode])
            ndata[trial][electrode] = v_trial # guardamos señal sin DC
    return ndata

def downSampling(data, sc, fs):
    if int(fs % 2):
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc+1))
    else:
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc))

    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            sub_signals[trial][electrode] = data[trial][electrode][::sc]
    return sub_signals

def artifactRegression(data,reference):
    reference = np.transpose(np.matrix(reference))
    data = np.transpose(np.matrix(data))
    op1 = (np.transpose(reference)*reference)/int(reference.shape[0]-1)
    op2 = (np.transpose(reference)*data)/int(data.shape[0]-1)
    coeff,_,_,_=np.linalg.lstsq(op1,op2)
    data = data - reference*coeff
    data = np.transpose(data)
    return data

id_s = raw_input("[!] Digite el identificador del sujeto: ")

[datac, datar] = getDataFromDB(id_s)
data = removeDC(datac)
Y=butter_filter(data)
scale= 10
Fs = 500/scale # esto es porque fue submuestreado a 2
sub_signals = downSampling(Y,int(scale),Fs)

#"""
#sub_signals = downSampling(data,int(scale),Fs)
#
#ts = 1.0/Fs
#time = np.arange(0,len(data[0][0]) * ts,ts)
#f, t, S = signal.spectrogram(sub_signals[0][0], fs=Fs, nperseg=32,nfft=32,noverlap=10)
#ff = sub_signals.shape # Tamaño del array
#Sxx = np.zeros((ff[0]*ff[1],len(f)+3))
#i=0
#for electrode in range(0,len(sub_signals)):
#    for trial in range(0,len(sub_signals[electrode])):
#        x = sub_signals[electrode][trial]
#        _, _, S = signal.spectrogram(x, fs=Fs, nperseg=32,nfft=32,noverlap=10)
#        Sxx[i,0:3] =[electrode+1,test_type,trial]
#        Sxx[i,3::] = np.mean(S,axis=1)
#        i+=1
#
#saveDataDB(Sxx.tolist())