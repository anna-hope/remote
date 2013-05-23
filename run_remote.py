#!/usr/bin/env python3.3

from remote import Remote, RemoteConnectionError

def main():
    print('Initialising...')
    
    port = '/dev/tty.RN42-B597-SPP'
    
    connected = False
    
    while not connected:
        try:
            rem = Remote(port)
        except RemoteConnectionError:
            print('\x1b[31;1mConnection on port {} unsuccessful\x1b[0m'.format(port))
            port = input('Please enter the right serial port: ')
            print('attempting another connection...')
        else:
            connected = True
    
    while True:
        data = input('Input: ')
        rem.send(data)
        rem.send('0')

if __name__ == '__main__':
    main()