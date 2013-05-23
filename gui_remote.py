#!/usr/bin/env python3.3

import tkinter as tk
from remote import Remote, RemoteConnectionError

class RemoteGUI:
    
    def __init__(self, master, port):
        
        frame = tk.Frame(master)
        frame.pack()
        
        connected = False
        
        while not connected:
            try:
                self.rem = Remote(port)
            except RemoteConnectionError:
                error_frame = tk.Frame(master)
                error_frame.pack()
                
                message = tk.Message(error_frame, width=100, text='Connection error',
                                                    takefocus=True)
                message.pack()
                
                # TODO: replace with a GUI prompt
                port = input('New port: ')
            else:
                connected = True
    
        forward_button = tk.Button(frame, text="forward", command=self.go_forward)
        forward_button.pack(side='top')
    
        back_button = tk.Button(frame, text="back", command=self.go_back)
        back_button.pack(side='bottom')
        
        left_button = tk.Button(frame, text='left', command=self.go_left)
        left_button.pack(side='left')
        
        right_button = tk.Button(frame, text='right', command=self.go_right)
        right_button.pack(side='right')
    
    def terminate_command(f):
        def wrapper(self):
            f(self)
            self.rem.send('0')
        return wrapper
    
    @terminate_command
    def go_forward(self):
        self.rem.send('f')
    
    @terminate_command
    def go_back(self):
        self.rem.send('b')
    
    @terminate_command
    def go_left(self):
        self.rem.send('l')
    
    @terminate_command
    def go_right(self):
        self.rem.send('r')

def main():
    
    root = tk.Tk()
    
    port = '/dev/tty.RN42-59F6-SPP'
    app = RemoteGUI(root, port)
    
    root.mainloop()

if __name__ == '__main__':
    main()