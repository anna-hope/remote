#!/usr/bin/env python3.3

# (c) Anton Osten 

import tkinter as tk
from tkinter import messagebox
from remote import Remote, RemoteConnectionError

class RemoteGUI:
    
    def __init__(self, master, debug=False):
        
        # get the screen size so we can calculate the offset
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        
        # centre it
        xoffset = round(screenwidth / 2)
        yoffset = round(screenheight / 3)
        
        
        # set the root window size
        master.geometry('{width}x{height}+{xoffset}+{yoffset}'.format(width=200,
         height=100, xoffset=xoffset,
                     yoffset=yoffset))
        
        self._get_port(master)
    
    def _connect(self, port):
        try:
            self.rem = Remote(port)
            return True
        except RemoteConnectionError:
            return False
    
    def _get_port(self, master):
        
        def set_port():
            port = entry.get()
            if self._connect(port):
                connect_frame.destroy()
                self._draw_interface(master)
            else:
                messagebox.showerror('Connection error', 
                                    "Could not connect on '{}'".format(port))
                
        connect_frame = tk.Frame(master)
        connect_frame.pack()
        
        message = tk.Message(connect_frame, width=100, text='Enter port',
                                            takefocus=True)
        message.pack()
        
        entry = tk.Entry(connect_frame)
        entry.pack()
        
        entry.insert(0, 'port')
        
        connect_button = tk.Button(connect_frame, text='connect', command=set_port)
        connect_button.pack()
    
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
    
        master.bind('<Up>', self.go_forward)
        master.bind('w', self.go_forward)
        
        master.bind('<Down>', self.go_back)
        master.bind('s', self.go_back)
        
        master.bind('<Left>', self.go_left)
        master.bind('a', self.go_left)
        
        master.bind('<Right>', self.go_right)
        master.bind('d', self.go_right)
    
    def terminate_command(f):
        def wrapper(*args):
            # when we use a keyboard key binding
            # it also passes an Event object along
            # so we want to ignore it without breaking things
            
            self = args[0]
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
    
    app = RemoteGUI(root, True)
    
    root.mainloop()

if __name__ == '__main__':
    main()