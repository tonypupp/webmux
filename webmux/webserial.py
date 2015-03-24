from twisted.internet.protocol import Protocol, Factory
from twisted.internet.serialport import SerialPort

import serial
#import pdb
#pdb.set_trace()
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD
from serial import STOPBITS_ONE, STOPBITS_TWO
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS

class Serial(SerialPort):
    def __init__(self, protocol, deviceNameOrPortNumber, reactor,
        baudrate = 115200, bytesize = EIGHTBITS, parity = PARITY_NONE,
        stopbits = STOPBITS_ONE, timeout = 0, xonxff = 0, rtscts = 0):
        SerialPort.__init__(protocol, deviceNameOrPortNumber, reactor,
            baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts)
        self.protocol = protocol

    def connect(self, terminal, on_error=None):
        self.session = SerialSession(self, terminal)
        self.protocol.openSession(self.session)

class SerialProtocol(Protocol):
    def __init__ (self, session):
        self.session = session
        self.opened = False

    def connecitonMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def openSession(self, session):
        self.session = session
        self.session.openSession()
        self.opened = True

    def closeSession(self):
        self.session = False
        self.opened = False

    def dataReceived(self, data):
        '''Data received from serial, send them to web session'''
        if (self.opened == Ture)
            self.session.dataReceived(data)

    def trigger(self, type, *args):
        pass

    def trigger_all(self, type, *args):
        pass

class SerialProtocolFactory(Factory):
    protocol = SerialProtocol
    transports = set()

    def trigger_all(self, type, *args):
        raw_data = json.dump({
            "type": type,
            "args": list(args),
        })

        for transport in self.transports:
            transport.write(raw_data)

class SerialSession(object):
    def __init__(self, serial, web_terminal):
        self.serial = serial
        self.terminal = web_terminal

    def openSession():
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
        
    def dataReceived(data):
        '''Data received from serial protocol, send to web terminal'''
        self.terminal.write_to_terminal(data)

class SerialSessionClient(object)
    def __init__(self, session):
        self.session = session

    def dataReceived(data):
        '''The data received from web. Send them to serial'''
        self.session.serial.writeSomeData(data)

