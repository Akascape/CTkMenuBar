"""
Menu Bar in Title Bar of customtkinter window
Author: Akash Bora
"""

import customtkinter
import sys

class CTkTitleMenu(customtkinter.CTkToplevel):
        
    def __init__(
        self,
        master,
        title_bar_color = "default",
        padx: int = 10,
        width: int = 10,
        x_offset: int = None,
        y_offset: int = None):
        
        super().__init__()

        if not sys.platform.startswith("win"):
            raise OSError("This title menu works only in windows platform, not supported on your system! \nTry the CTkMenuBar instead...")
        
        self.after(10)
        self.master = master
        master_type = self.master.winfo_name()
        
        if master_type=="tk":
            pass
        elif master_type.startswith("!ctktoplevel"):
            pass
        elif master_type.startswith("!toplevel"):
            pass        
        else:
            raise TypeError("Only root windows/toplevels can be passed as the master!")
        
        self.master.minsize(200,100)
        self.after(100, lambda: self.overrideredirect(True))
        
        if title_bar_color=="default":
            if customtkinter.get_appearance_mode()=="Light":
                title_bar_color = 0xFFFFFF # RGB order: 0xrrggbb             
            else:
                title_bar_color = 0x303030 # RGB order: 0xrrggbb
                
        self.transparent_color = self._apply_appearance_mode(self._fg_color)
        self.attributes("-transparentcolor", self.transparent_color)
        self.resizable(True, True)
        self.transient(self.master)
        self.menu = []

        self.config(background=self.transparent_color)
        self.caption_color = title_bar_color
        self.change_header_color(self.caption_color)
        self.x_offset = 40 if x_offset is None else x_offset
        self.y_offset = 6 if y_offset is None else y_offset
        self.width = width
        if x_offset is None:
            title = self.master.title()
            if len(title)>=1:
                for i in title:
                    if i.islower():
                        self.x_offset += 9
                    else:
                        self.x_offset += 7
            
        self.padding = padx
        
        self.master.bind("<Configure>", lambda _: self.change_dimension())
        self.master.bind("<Destroy>", lambda _: self.destroy())
        self.num = 0
        
        self.master.bind("<Map>", lambda e: self.withdraw)

    def add_cascade(self, text=None, **kwargs):
    
        if not "fg_color" in kwargs:
            fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
        else:
            fg_color = kwargs.pop("fg_color")
        if not "text_color" in kwargs:
            text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
        else:
            text_color = kwargs.pop("text_color")
            
        if text is None:
            text = f"Tab {self.num+1}"
    
        self.menu_button = customtkinter.CTkButton(self, text=text, fg_color=fg_color,
                                                   text_color=text_color, width=self.width, height=10, **kwargs)
        self.menu_button.grid(row=0, column=self.num, padx=(0, self.padding))
        self.num += 1

        return self.menu_button
    
    def change_dimension(self):
        width = self.master.winfo_width()-130-self.x_offset
        if width<0:
            self.withdraw()
            return
        if self.master.state()=="iconic":
            self.withdraw()
            return
        height = self.master.winfo_height()
        x = self.master.winfo_x()+self.x_offset
        y = self.master.winfo_y()+self.y_offset
        if self.master.state()=="zoomed":
            y += 4
            x -= 7
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
 
    def change_header_color(self, caption_color):
        try:
            from ctypes import windll, byref, sizeof, c_int
            # optional feature to change the header in windows 11
            HWND = windll.user32.GetParent(self.master.winfo_id())
            DWMWA_CAPTION_COLOR = 35
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_CAPTION_COLOR, byref(c_int(caption_color)), sizeof(c_int))
        except: None
