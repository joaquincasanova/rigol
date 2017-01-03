import numpy as np
from numpy import matlib
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import rigolUtils

fieldnames=['bias','amp','f_lo','field_f','phase','tscale','fft']
csvfile = open('./data4b.csv','r')
data=np.zeros([1,807])
nfft=801
try:
    reader=csv.reader(csvfile)
    rownum=0
    for row in reader:
        if rownum==0:
            header=row
            col_bias=header.index("bias")
            col_f_lo=header.index("f_lo")
            col_amp=header.index("amp")
            col_field_f=header.index("field_f")
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
            try:
                data=np.append(data,this,axis=0)
            except:
                break
            
        rownum+=1
        #print rownum
finally:
    csvfile.close()

amp_vals = [.1]
bias_vals = [.3,.31,.32,.33,.34,.35,.36,.37,.38]#[.3,.35,.4,.45,.5,.55,.6,.65,.7]
field_f_vals = [10.,100.,1000.]    
data=np.delete(data,(0),axis=0)
colors=('b', 'g', 'r')
lines=(':','-','--')

for f in field_f_vals:
    idx=0
    for b in bias_vals:
        idx+=1
        plt.subplot(3, 3, idx)
        
        col=colors[0]
        lin=lines[1]
        lab='Field f='+str(f)+' Hz'+' bias'+str(b)+' V'
        picks = np.where(abs(data[:,col_bias]-b)<.001)
        picks = np.intersect1d(picks, np.where(abs(data[:,col_field_f]-f)<.001))
        data_slice_x=np.reshape(np.array(range(0,nfft))*f/nfft*2,[1,nfft])
        data_slice_y=data[picks,6:]
        data_slice_y=data[picks,6:]
        snr=rigolUtils.SNR(data_slice_y)
        print lab+', SNR (dB):' + str(snr)
        try:
            plt.plot(data_slice_x.T, data_slice_y.T,linestyle=lin,color=col,label=lab)
        except:
            break
        plt.title(lab)
        xmax = np.amax(data_slice_x)
        plt.xlim(0,xmax)
        plt.ylim(-100,20)

        if idx==7:
            plt.ylabel('Vout (dbV)')
            plt.xlabel('Frequency (Hz)')
    plt.show()

        

plt.show()
