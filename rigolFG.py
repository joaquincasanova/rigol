import usbtmc
import time

nameQ = '*IDN?'
channel1 = "CH1"
channel2 = "CH2"
app = "APPL"
sine = "SIN"
square = "SQU"
function = "FUNC"
freq = "FREQ"
volt = "VOLT"
phase = "PHAS"
unit = "UNIT"
vpp = " VPP"
duty = "DCYC"
loc = "SYST:LOC"
rem = "SYST:REM"
class RigolFunctionGenerator:
    """Class to control a Rigol DS1000 series oscilloscope"""
    def __init__(self, device = None):
        if(device == None):
            raise ValueError("There is no device to access")
        else:
            self.device = device
            self.initFG()
    def initFG(self):
        self.meas = usbtmc.UsbTmcDriver(self.device)
        self.meas.write(nameQ)
        time.sleep(0.2)
        self.name=self.meas.read()
        print 'FG: ',self.device,self.name
    def w(self,command):
        if len(command) < 30: print "FG: ", self.name, command
        self.meas.write(command)
        time.sleep(0.2)
 
    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()

    def off(self,chan):
        time.sleep(0.8)
        if chan==1:
            self.w("OUTP OFF")
        else:
            self.w("OUTP:"+channel2+" OFF")
        
    def on(self,chan):
        time.sleep(0.8)
        if chan==1:
            self.w("OUTP ON")
        else:
            self.w("OUTP:"+channel2+" ON")

    def sine(self, chan, f, amp, off, ph):

        if chan==1:
            self.w(nameQ)
            self.meas.read()
            self.w(volt+':'+unit+ vpp)
            self.w(app+':'+sine+' '+str(f)+','+str(amp)+','+str(off))
            self.w(phase+' '+str(ph))
        else:
            self.w(nameQ)
            self.meas.read()
            self.w(volt+':'+unit+':'+channel2+vpp)
            self.w(app+':'+sine+':'+channel2+' '+str(f)+','+str(amp)+','+str(off))
            self.w(phase+' '+str(ph))

    def phase(self, chan, ph):

        if chan==1:
            self.w(nameQ)
            self.meas.read()
            self.w(phase+' '+str(ph))
        else:
            self.w(nameQ)
            self.meas.read()
            self.w(phase+' '+str(ph))
        
    def square(self, chan, f, amp, off, d):

        if chan==1:
            self.w(nameQ)
            self.meas.read()
            self.w(volt+':'+unit+ vpp)
            self.w(app+':'+square+' '+str(f)+','+str(amp)+','+str(off))
            self.w(function+':'+square+':'+duty+' '+str(d))
        else:
            self.w(nameQ)
            self.meas.read()
            self.w(volt+':'+unit+':'+channel2+vpp)
            self.w(app+':'+square+':'+channel2+' '+str(f)+','+str(amp)+','+str(off))
            self.w(function+':'+square+':'+duty+':'+channel2+' '+str(d))
    def local(self):
        self.w(nameQ)
        self.meas.read()
        self.w(loc)

    def sync(self,stat):
        
        self.w(nameQ)
        self.meas.read()
        self.w('OUTP:SYNC '+ stat)
        
