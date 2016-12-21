import numpy as np
from numpy import matlib
import csv
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt

fieldnames=['f_lo','phase','tscale','fft']
csvfile = open('./data2.csv','r')
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
            try:
                data=np.append(data,this,axis=0)
            except:
                break
            
        rownum+=1
        #print rownum
finally:
    csvfile.close()

f_vals = [9.6e4,9.7e4, 9.8e4, 9.9e4, 10.0e4, 10.1e4,10.2e4,10.3e4,10.4e4]
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
    
    data_slice_x=np.squeeze(np.reshape(np.array(range(0,nfft))*field_f/nfft*2,[1,nfft]))
    data_slice_y=np.squeeze(data[picks,3:])

    plt.plot(data_slice_x.T, data_slice_y.T,linestyle=lin,color=col)
    plt.title('f_lo='+str(f)+' Hz')
    xmax = np.amax(data_slice_x)
    plt.xlim(0,xmax)
    plt.ylim(-100,20)

    if idx1==7:
        plt.ylabel('Vout (dbV)')
        plt.xlabel('Frequency (Hz)')
plt.show()
