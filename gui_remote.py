#!/usr/bin/env python3.3

import tkinter as tk
from tkinter import messagebox
from remote import Remote, RemoteConnectionError

class RemoteGUI:
    
    def __init__(self, master, port, debug=False):
        self._get_port(master, port)
    
    def _get_port(self, master, port):
        
        def update_port():
            try:
                self.rem = Remote(entry.get())
            except RemoteConnectionError:
                error_frame.destroy()
                self._get_port(master, port)
            else:
                error_frame.destroy()
                self._draw_interface(master)
            
        error_frame = tk.Frame(master)
        error_frame.pack()
        
        message = tk.Message(error_frame, width=100, text='Enter port',
                                            takefocus=True)
        message.pack()
        
        entry = tk.Entry(error_frame)
        entry.pack()
        
        entry.insert(0, port)
        
        update_button = tk.Button(error_frame, text='update port', command=update_port)
        update_button.pack()
    
    def _draw_interface(self, master):
        frame = tk.Frame(master)
        frame.pack()

        forward_button = tk.Button(frame, text="forward", command=self.go_forward)
        forward_button.pack(side='top')

        back_button = tk.Button(frame, text="back", command=self.go_back)
        back_button.pack(side='bottom')
    
        left_button = tk.Button(frame, text='left', command=self.go_left)
        left_button.pack(side='left')
    
        right_button = tk.Button(frame, text='right', command=self.go_right)
        right_button.pack(side='right')
    
        # bind keyboard keys to events
    
        master.bind('Up', self.go_forward)
        master.bind('Down', self.go_back)
        master.bind('Left', self.go_left)
        master.bind('Right', self.go_right)
    
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
    root.title('Remote')
    
    port = '/dev/tty.RN42-59F6-SPP'
    app = RemoteGUI(root, port, True)
    
    root.mainloop()

if __name__ == '__main__':
    main()