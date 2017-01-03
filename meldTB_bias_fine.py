#!/usr/bin/env python2

import usbtmc
import time
import rigolScope
import rigolFG
import rigolUtils
import matplotlib.pyplot as plot
import sys
import numpy as np
from time import strftime
import csv
import string
nameQ = '*IDN?'
fgID1, fgDr1,fgID2, fgDr2, scID, scDr = rigolUtils.discoverFG()

fgDr1.write(nameQ)
time.sleep(.2)
n1=fgDr1.read()

if 'DG1022U' in n1:
    #define FG2 as 1022U
    fgID=fgID1
    fgDr=fgDr1
    fgID1=fgID2
    fgDr1=fgDr2
    fgID2=fgID1
    fgDr2=fgDr1

scope = rigolScope.RigolScope(device=scID)
fg1 = rigolFG.RigolFunctionGenerator(device=fgID1)
fg2 = rigolFG.RigolFunctionGenerator(device=fgID2)

adjustfactor = 12.
waitfactor = 48.

tscale = 2e-3
scope.setTimeScale(tscale)    
scope.reactivateControlButtons()

fg1.off(2)
fg1.off(1)

fg2.off(2)
fg2.off(1)

#channel 1 is LO.
#channel 2 is DC bias.
scope.setDisp(1,0)
scope.setDisp(2,1)
scope.setProbe(2,1)
scope.setScale(2,10.)
scope.setOffset(2,0)
scope.run()
time.sleep(tscale*waitfactor)


fieldnames=['bias','amp','f_lo','field_f','phase','tscale','fft']
csvfile = open('./data_no_fb_bias_fine.csv','w')
writer=csv.writer(csvfile,delimiter=',')
writer.writerow(fieldnames)
try:
    for dc in [.3,.31,.32,.33,.34,.35,.36,.37,.38]:
        for amp_drive in [.1]:
            for f_field in [10.,100.,1000.]:
                for amp_field in [1.]:
                    for f_lo in [10.0e4]:
                        scope.run()
                        tscale = 2e-3
                        scope.setTimeScale(tscale)
                        scope.setScale(2,10.)
                        scope.setOffset(2,0)    

                        f_bias = 1e-6
                        amp_bias = dc*2.
                        d_bias=50

                        #f_lo = 1e5
                        amp_lo = 5.
                        ph_lo = np.arange(-180,180,1)
                        ave = 14.0*np.ones(ph_lo.shape)
                        #1022
                        fg1.square(2,f_bias,amp_bias,0.,50)#bias
                        fg1.sine(1,f_field,amp_field,0.,0)#field

                        idx=0
                        #1022u
                        fg2.sine(2,f_lo,amp_drive,0.,0)#drive
                        fg2.sine(1,f_lo,amp_lo,0.,0)#lo - need to adjust phase

                        fg1.on(1)
                        fg2.on(1)
                        
                        fg1.on(2)
                        fg2.on(2)

                        time.sleep(waitfactor*tscale)
                        time.sleep(waitfactor*tscale)

                        for ph in ph_lo:
                            #sweep until error stops decreasing
                            fg2.phase(1,ph)
                            time.sleep(waitfactor*tscale)
                            ave[idx] = scope.getAve(2)
                            print ph, ave[idx]
                            if idx>=1 and abs(ave[idx])>abs(ave[idx-1]) and abs(ave[idx-1])<1.:
                                break
                            else:
                                idx += 1

                        top = scope.getMax(2)
                        idx = np.argmin(abs(ave))
                        ph = ph_lo[idx]
                        print "Min voltage phase: ",ph, ave[idx]
                        fg2.phase(1,ph)

                        tscale = 1./f_field*20.#timescale for fft
                        scope.setTimeScale(tscale)
                        if top<=0.01:                                           
                            scope.setScale(2,.05)
                        elif top>0.01 and top<=0.5:                                           
                            scope.setScale(2,.1)
                        elif top>0.5 and top<=1:
                            scope.setScale(2,.2)
                        elif top>1 and top<=2.5:
                            scope.setScale(2,.5)
                        elif top>2.5 and top<=5:
                            scope.setScale(2,1.0)
                        else:
                            scope.setScale(2,2.0)
                                
                        scope.mathScale(20)
                        scope.setOffset(2,0)
                        scope.setFFT(2, 1, f_field)

                        time.sleep(max(200e-3,tscale)*waitfactor)

                        scope.stop()
                        wav=scope.getWave('math')
                        wav=string.split(wav,',')
                        wav=[string.atof(w) for w in wav]
                        row=[dc,amp_drive,f_lo,f_field,ph,tscale]
                        row=np.hstack((row,wav))
                        writer.writerow(row)

    csvfile.close()

    fg1.off(1)
    fg2.off(1)

    fg1.off(2)
    fg2.off(2)

    fg2.local()
    fg1.local()

    scope.reactivateControlButtons()
except KeyboardInterrupt:
    csvfile.close()

    print "Quitting on: ", f_lo
    fg1.off(1)
    fg2.off(1)

    fg1.off(2)
    fg2.off(2)

    fg2.local()
    fg1.local()

    scope.reactivateControlButtons()
    
    
