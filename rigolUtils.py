import numpy as np
import usbtmc
import time
def SNR(y):
    if len(y)==0:
        return []
    else:
        if y.shape[0]>1: y=y.reshape([1,-1])
        return np.amax(y[0,390:411]-np.mean(np.hstack((y[0,10:390], y[0,411:]))))


def discoverFG():

    nameQ = '*IDN?'
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
