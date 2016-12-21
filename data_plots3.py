import numpy as np
from numpy import matlib
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

fieldnames=['bias','amp','f_lo','field_f','phase','tscale','fft']
csvfile = open('./data3.csv','r')
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

amp_vals = [.05,.1,.15]
bias_vals = [.3, .45, .5]
field_f_vals = [10.,100.,1000.]
field_vals = [.1]
flo_vals = [.98e5,1e5,1.04e5]    
data=np.delete(data,(0),axis=0)
colors=('b', 'g', 'r')
lines=(':','-','--')

idx1 = 0
for f in field_f_vals:
    for fa in flo_vals:
        idx1+=1
        idx2 = 0
        for b in bias_vals:
            idx3 = 0
            for a in amp_vals:
                plt.subplot(4, 3, idx1)
                
                col=colors[idx2]
                lin=lines[idx3]
                lab='bias='+str(b)+', amp='+str(a)
                picks = np.where(abs(data[:,col_bias]-b)<.001)
                picks = np.intersect1d(picks, np.where(abs(data[:,col_f_lo]-fa)<.001))
                picks = np.intersect1d(picks, np.where(abs(data[:,col_amp]-a)<.001))
                picks = np.intersect1d(picks, np.where(abs(data[:,col_field_f]-f)<.001))
                data_slice_x=np.reshape(np.array(range(0,nfft))*f/nfft*2,[1,nfft])
                data_slice_y=data[picks,6:]
                data_slice_y=data[picks,6:]
                snr=data_slice_y[0,398:403]-np.mean(np.hstack((data_slice_y[0,6:398], data_slice_y[0,403:])))
                print lab, 'Field freq='+str(f)+' LO freq'+str(fa)+' Hz, SNR (dB):' + str(np.amax(snr))
                try:
                    plt.plot(data_slice_x.T, data_slice_y.T,linestyle=lin,color=col,label=lab)
                except:
                    break
                plt.title('Field freq='+str(f)+' LO freq'+str(fa)+' Hz')
                xmax = np.amax(data_slice_x)
                plt.xlim(0,xmax)
                plt.ylim(-100,20)
                idx3+=1
            idx2+=1

        if idx1==8:
            legend = plt.legend(loc=(0,-1.5),labelspacing=0)

        if idx1==7:
            plt.ylabel('Vout (dbV)')
            plt.xlabel('Frequency (Hz)')
plt.show()

        

plt.show()
