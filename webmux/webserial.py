from twisted.internet.protocol import Protocol, Factory
from twisted.internet.serialport import SerialPort

import serial
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD
from serial import STOPBITS_ONE, STOPBITS_TWO
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS

from twisted.python import log

class Serial(SerialPort):
    session = {}
    def __init__(self, deviceNameOrPortNumber, reactor,
    baudrate = 115200, bytesize = EIGHTBITS, parity = PARITY_NONE,
    stopbits = STOPBITS_ONE, timeout = 0, xonxoff = 0, rtscts = 0):
        self.protocol = SerialProtocol()
        super(Serial, self).__init__(self.protocol, deviceNameOrPortNumber,
        reactor, baudrate, bytesize, parity, stopbits, timeout, xonxoff,
        rtscts)

    def connect(self, terminal, on_error=None):
        Serial.session[terminal._id] = SerialSession(self, terminal)
        self.protocol.openSession(Serial.session[terminal._id])

class SerialFactory(object):
    serial = None

    def __init__(self):
        pass

    @classmethod
    def getserial(cls):
        from twisted.internet import reactor
        from argparse import ArgumentParser

        parser = ArgumentParser()
        parser.add_argument("-p", "--port", default=8080, type=int, help="Prot to listen on/")
        parser.add_argument("-d", "--device", default="/dev/ttyACM2", help="Consle device")
        parser.add_argument("-b", "--baudrate", default=115200, type=int, help="Baudrate for console device")
        args = parser.parse_args()

        if(cls.serial == None):
            cls.serial = Serial(args.device, reactor, args.baudrate)

        return cls.serial


class SerialProtocol(Protocol):
    def __init__ (self):
        self.opened = False

    def connecitonMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def openSession(self, session):
        session.openSession()
        self.opened = True

    def closeSession(self):
        self.opened = False

    def dataReceived(self, data):
        '''Data received from serial, send them to web session'''
        if (self.opened == True):
            for id in Serial.session:
                Serial.session[id].dataReceived(data)

class SerialSession(object):
    def __init__(self, serial, webterminal):
        self.serial = serial
        self.terminal = webterminal

    def openSession(self):
        client = SerialSessionClient(self)
        self.terminal.set_active_session(client)
        self.allocatePty()

    def allocatePty(self):
        term = self.terminal.get_name()
        log.msg("terminal name:", term)
        self.window_size = self.terminal.get_window_size()
        log.msg("terminal window size:", self.window_size)

        self.terminal.register_resize_callback(self._windowResized)
    
    def _windowResized(self, *args):
        self.window_size = self.terminal.get_window_size()
        self.updateWindowSize()

    def updateWindowSize(self):
        time_diff = float(time.time() - self.last_update)
        if time_diff < 1 and not self.queue_call:
            reactor.callLater(time_diff, self.updateWindowSize)
            self.queue_call = True
            return

        self.queue_call = False
        self.last_update = time.time()
        
    def dataReceived(self, data):
        '''Data received from serial protocol, send to web terminal'''
        self.terminal.io.parent.write_to_terminal(self.terminal._id, data)

class SerialSessionClient(object):
    def __init__(self, session):
        self.session = session

    def dataReceived(self, data):
        '''The data received from web. Send them to serial'''
        self.session.serial.writeSomeData(data)

