import numpy as np
from numpy import matlib
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import rigolUtils

fieldnames=['f_lo','phase','tscale','fft']
csvfile = open('data_no_fb_10khz_freq.csv','r')
data=np.zeros([1,804])
nfft=801
try:
    reader=csv.reader(csvfile)
    rownum=0
    for row in reader:
        if rownum==0:
            header=row
            col_f_lo=header.index("f_lo")
            col_phase=header.index("phase")        
            col_tscale=header.index("tscale")         
            col_fft=header.index("fft")     
        else:
            try:
                x=[float(i) for i in row]
            except ValueError:
                break
            this=np.array(x)
            this=this.reshape([1,-1])
            print this.shape
            this=this[0,0:807].reshape([1,-1])
            print this.shape

            try:
                data=np.append(data,this,axis=0)
            except:
                break
            
        rownum+=1
        #print rownum
finally:
    csvfile.close()

f_vals = [9.6e3,9.7e3, 9.8e3, 9.9e3, 10.0e3, 10.1e3,10.2e3,10.3e3,10.4e3]
field_f=10.    
data=np.delete(data,(0),axis=0)
colors=('b', 'g', 'r')
lines=(':','-','--')

idx1 = 0
for f in f_vals:
    idx1+=1
    plt.subplot(3, 3, idx1)
                
    col=colors[0]
    lin=lines[1]
    picks = np.where(abs(data[:,col_f_lo]-f)<.001)
    picks = np.intersect1d(picks, np.where(data[:,col_phase]<0.))
    
    data_slice_x=np.squeeze(np.reshape(np.array(range(0,nfft))*field_f/nfft*2,[1,nfft]))
    data_slice_y=np.squeeze(data[picks,3:])
    snr=rigolUtils.SNR(data_slice_y.reshape([1,-1]))
    print str(f), ', SNR: ',str(snr)
    plt.plot(data_slice_x.T, data_slice_y.T,linestyle=lin,color=col)
    plt.title('f_lo='+str(f)+' Hz')
    xmax = np.amax(data_slice_x)
    plt.xlim(0,xmax)
    plt.ylim(-80,0)

    if idx1==7:
        plt.ylabel('Vout (dbV)')
        plt.xlabel('Frequency (Hz)')
plt.show()

idx1 = 0
for f in f_vals:
    idx1+=1
    plt.subplot(3, 3, idx1)
                
    col=colors[0]
    lin=lines[1]
    picks = np.where(abs(data[:,col_f_lo]-f)<.001)
    picks = np.intersect1d(picks, np.where(data[:,col_phase]>0.))
    
    data_slice_x=np.squeeze(np.reshape(np.array(range(0,nfft))*field_f/nfft*2,[1,nfft]))
    data_slice_y=np.squeeze(data[picks,3:])
    snr=rigolUtils.SNR(data_slice_y.reshape([1,-1]))
    print str(f), ', SNR: ',str(snr)
    plt.plot(data_slice_x.T, data_slice_y.T,linestyle=lin,color=col)
    plt.title('f_lo='+str(f)+' Hz')
    xmax = np.amax(data_slice_x)
    plt.xlim(0,xmax)
    plt.ylim(-100,20)

    if idx1==7:
        plt.ylabel('Vout (dbV)')
        plt.xlabel('Frequency (Hz)')
plt.show()
