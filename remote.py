import serial
import multiprocessing as mp

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message

class BadInputError(CustomError):
    pass

class RemoteConnectionError(CustomError):
    pass

class Remote(object):
    def __init__(self, port, baudrate=115200):
        try:
            self.ser = serial.Serial(port, baudrate)
        except (FileNotFoundError, OSError, serial.serialutil.SerialException) as e:
            raise RemoteConnectionError(e)
    
    def send(self, data):
        '''Accepts either bytes or str'''
        # check if its bytes or str
        if not isinstance(data, (bytes, str)):
            raise BadInputError('Expected bytes or str')
        # if it's str, convert it to bytes
        try:
            self.ser.write(data)
        except TypeError:
            data = bytes(data, 'utf-8')
            self.ser.write(data)
        return len(data)
    
    def receive(self, timeout=None):
        '''Reads information sent over.
        If a timeout is specified, the reading process is killed after the timeout.'''
        # start another process to kill in case it's taking too long
        with mp.Pool(processes=1) as p:
            r = p.apply_async(self.ser.read)
            try:
                received_data = r.get(timeout)
            except mp.TimeoutError:
                return 'timeout'
        try:
            output = received_data.decode('utf-8')
        except UnicodeDecodeError:
            output = received_data
        
        return output
        