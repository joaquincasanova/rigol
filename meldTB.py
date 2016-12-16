#!/usr/bin/env python2

import usbtmc
import time
import rigolScope
import rigolFG
import matplotlib.pyplot as plot
import sys
import numpy as np
from time import strftime
import csv

nameQ = '*IDN?'
def discoverFG():
    #what's connected? query.
    lod = usbtmc.getDeviceList()
    print lod
    if len(lod)==3:
        d = [usbtmc.UsbTmcDriver(lod[0]), usbtmc.UsbTmcDriver(lod[1]), usbtmc.UsbTmcDriver(lod[2])]
        d[0].write(nameQ)
        d[1].write(nameQ)
        d[2].write(nameQ)
        time.sleep(0.2)
        if d[0].read()=='':
            scID = lod[0]
            scDr = d[0]
            fgID1 = lod[1]
            fgDr1 = d[1]
            fgID2 = lod[2]
            fgDr2 = d[2]
        elif d[1].read()=='':
            scID = lod[1]
            scDr = d[1]
            fgID1 = lod[0]
            fgDr1 = d[0]
            fgID2 = lod[2]
            fgDr2 = d[2]
        else:
            scID = lod[2]
            scDr = d[2]
            fgID1 = lod[0]
            fgDr1 = d[0]
            fgID2 = lod[1]
            fgDr2 = d[1]
    elif len(lod)==2:
        d = [usbtmc.UsbTmcDriver(lod[0]), usbtmc.UsbTmcDriver(lod[1])]
        d[0].write(nameQ)
        d[1].write(nameQ)
        time.sleep(0.2)
        if d[0].read()=='':
            scID = lod[0]
            scDr = d[0]
            fgID1 = lod[1]
            fgDr1 = d[1]
            fgID2 = None
            fgDr2 = None
        elif d[1].read()=='':
            scID = lod[1]
            scDr = d[1]
            fgID1 = lod[0]
            fgDr1 = d[0]
            fgID2 = None
            fgDr2 = None
        else:
            scID = None
            scDr = None
            fgID2 = lod[1]
            fgID2 = d[1]
            fgID1 = lod[0]
            fgDr1 = d[0]
    elif len(lod)==1:
        d = usbtmc.UsbTmcDriver(lod)
        d.write(nameQ)
        time.sleep(0.2)
        if d.read()=='':
            scID = lod
            scDr = d
            fgID1 = None
            fgDr1 = None
            fgID2 = None
            fgDr2 = None
        else:
            fgID1 = lod
            fgDr1 = d
            fgID2 = None
            fgDr2 = None
            scID = None
            scDr = None
    else:
        fgID1 = None
        fgDr1 = None
        fgID2 = None
        fgDr2 = None
        scID = None
        scDr = None

    return fgID1, fgDr1, fgID2, fgDr2,scID, scDr

fgID1, fgDr1,fgID2, fgDr2, scID, scDr = discoverFG()

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

tscale = 10e-6
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


fieldnames=['bias','amp','field','field_f','phase','tscale','fft']
csvfile = open('./data.csv','w')
writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
writer.writeheader()

for dc in np.arange(0.2,.6,.1):
    for amp_drive in np.arange(0.05,0.3,.05):
        for f_field in [10., 100., 1000.]:
            scope.run()
            tscale = 20e-3
            scope.setTimeScale(tscale)    

            f_bias = 1e-6
            amp_bias = dc*2.
            d_bias=50

            amp_field =1.

            f_lo = 1e5
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
            fg1.on(2)

            fg2.on(1)
            fg2.on(2)

            for ph in ph_lo:
                #sweep until error stops decreasing
                fg2.phase(1,ph)
                time.sleep(waitfactor*tscale)
                ave[idx] = scope.getAve(2)
                print ph, ave[idx]
                if idx>=1 and abs(ave[idx])>abs(ave[idx-1]) and abs(ave[idx])<10.:
                    break
                else:
                    idx += 1

            idx = np.argmin(abs(ave))
            ph = ph_lo[idx]
            print "Min phase: ",ph, ave[idx]
            fg2.phase(1,ph)

            tscale = 1./f_field*20.#timescale for fft
            scope.setTimeScale(tscale)    

            time.sleep(waitfactor*tscale)
            scope.setScale(2,5.)
            scope.setOffset(2,0)
            #scope.setFFT(2, 1)
            time.sleep(tscale*waitfactor)
            scope.stop()
            wav=scope.getWave(2)#'math')
            writer.writerow({'bias':dc,'amp':amp_drive,'field':amp_field,'field_f':f_field,'phase':ph,'tscale':tscale,'fft':wav})

csvfile.close()

fg1.off(1)
fg1.off(2)

fg2.off(1)
fg2.off(2)

fg2.local()
fg1.local()

scope.reactivateControlButtons()
scope.reset()
    
    
