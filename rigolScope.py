
import usbtmc
import timeAxis
import time

channel1 = "CHAN1"
channel2 = "CHAN2"
math = "MATH"
source = "SOUR"
meas = "MEAS"
fft = "FFT"
waveform = "WAV"
mode = "MODE"
norm = "NORM"
form = "FORM"
asc = "ASC"
data = "DATA?"
item = "ITEM?"
scale = "SCAL"
ave = "VAVG"
timescale = "TIM"
tscal = "SCAL?"
toffs = "OFFS?"
disp = "DISP"
probe = "PROB"
voffs = "OFFS"
operator = "OPER"
byte = "BYTE"
center = "HCEN"

class RigolScope:
    """Class to control a Rigol DS1000 series oscilloscope"""
    def __init__(self, device = None):
        if(device == None):
            raise ValueError("There is no device to access")
        else:
            self.device = device
            self.initScope()

    def initScope(self):

        self.meas = usbtmc.UsbTmcDriver(self.device)

        print "SCOPE: ", self.device, self.meas.getName()

        #self.channel1 = rigolScopeChannel.RigolScopeChannel(self, self.CHANNEL1);
        #self.channel2 = rigolScopeChannel.RigolScopeChannel(self, self.CHANNEL2);        
        
    def write(self, command):
        """Send an arbitrary command directly to the scope"""
        self.meas.write(command)
        
    def read(self, command):
        """Read an arbitrary amount of data directly from the scope"""
        out=self.meas.read(command)
        time.sleep(.02)
        return out
    
    def reset(self):
        """Reset the instrument"""
        self.meas.sendReset()

    def getName(self):
        return self.meas.getName()

    def getDevice(self):
        return self.device
        
    def run(self):
        self.write(":RUN")
        
    def stop(self):
        self.write(":STOP")
        
    def reactivateControlButtons(self):
        self.write(":KEY:FORC")
    
    def getScopeInformation(self, channel, command, readBytes):
        self.write(":" + channel + ":" + command)
        return self.read(readBytes)
        
    def getScopeInformationFloat(self, channel, command):
        rawScopeInformation = self.getScopeInformation(channel, command, 20)
        floatScopeInformation = float(rawScopeInformation)
        return floatScopeInformation
    
    def getScopeInformationInteger(self, channel, command):
        rawScopeInformation = self.getScopeInformation(channel, command, 20)
        floatScopeInformation = int(rawScopeInformation)
        return floatScopeInformation
    
    def getScopeInformationString(self, channel, command, readBytes):
        return self.getScopeInformation(channel, command, readBytes)
        
    def getTimeScale(self):
        return self.getScopeInformationFloat(timescale, tscal)
        
    def getTimescaleOffset(self):
        return self.getScopeInformationFloat(timescale, toffs)
        
    def getTimeAxis(self):
        return timeAxis.TimeAxis(self.getTimeScale())

    def chanNum(self,c):
        if c==1:
           chan=channel1
        elif c==2:
           chan=channel2
        else:
           chan=math
        return chan

    def setScale(self, c, s):
        chan=self.chanNum(c)
            
        command = ':'+chan+':'+scale + ' ' + str(s)
        print command
        self.write(command)

    def mathScale(self, s):
        
        command = ':MATH:SCAL' + ' ' + str(s)
        print command
        self.write(command)

    def getAve(self, c):
        chan=self.chanNum(c)
           
        command = ':'+meas+':'+source + ' ' + chan
        print command
        self.write(command)
           
        command = ':'+meas+':'+item + ' ' + ave + ','+chan
        print command
        self.write(command)

        out = self.read(32)

        return out
    
    def setFFT(self,c,stat,f_field):
        chan=self.chanNum(c)
        
        command = ':' + math + ':' + source + str(1)+ ' ' + chan
        print command
        self.write(command)

        command = ':' + math + ':' + operator + ' ' + fft
        print command
        self.write(command)

        command = ':' + math + ':' + fft + ':' + center + ' ' + str(f_field)
        print command
        self.write(command)

        command = ':' + math + ':' + disp + ' ' + str(stat)
        print command
        self.write(command)

    def getWave(self, c):
        chan=self.chanNum(c)

        command = ':' + waveform + ':' + source + ' ' + chan
        print command
        self.write(command)

        command = ':' + waveform + ':' + mode + ' ' + norm
        print command
        self.write(command)

        command = ':' + waveform + ':' + form + ' ' + asc
        print command
        self.write(command)
     
        command = ':' + waveform + ':' + data + ' ' + chan
        print command
        self.write(command)

        out = self.read(1)
        print 'Reading ...'
        while True:
            try:
                out = out + self.read(1)
            except OSError:
                print 'Done'
                break
        return out[11:]
    def setDisp(self, c, stat):
        chan=self.chanNum(c)
           
        command = ':'+chan+':'+disp + ' ' + str(stat)
        print command
        self.write(command)

    def setProbe(self, c, atten):
        chan=self.chanNum(c)
           
        command = ':'+chan+':'+probe + ' ' + str(atten)
        print command
        self.write(command)

    def setOffset(self, c, offset):
        chan=self.chanNum(c)
           
        command = ':'+chan+':'+voffs+ ' ' + str(offset)
        print command
        self.write(command)

    def setTimeScale(self,scal):
           
        command = ':TIM:MAIN:' + tscal[0:-1]+' ' + str(scal)
        print command
        self.write(command)
