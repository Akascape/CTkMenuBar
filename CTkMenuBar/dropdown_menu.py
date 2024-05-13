"""
Custom Dropdown Menu for CTkMenuBar
Original Author: LucianoSaldivia | https://github.com/LucianoSaldivia
Modified by: Akash Bora (Akascape)
"""

from __future__ import annotations
import customtkinter
from functools import partial
import tkinter as tk
from typing import Callable

class _CDMOptionButton(customtkinter.CTkButton):
    def setParentMenu(self, menu: "CustomDropdownMenu"):
        self.parent_menu = menu

    def cget(self, param):
        if param=="option":
            return self.cget("text")
        return super().cget(param)
    
    def configure(self, **kwargs):
        if "option" in kwargs:
            super().configure(text=kwargs.pop("option"))
        super().configure(**kwargs)
        
class _CDMSubmenuButton(_CDMOptionButton):
    def setSubmenu(self, submenu: "CustomDropdownMenu"):
        self.submenu = submenu
        
    def cget(self, param):
        if param=="submenu_name":
            return self.cget("text")
        return super().cget(param)
    
    def configure(self, **kwargs):
        if "submenu_name" in kwargs:
            super().configure(text=kwargs.pop("submenu_name"))
        super().configure(**kwargs)
        
class CustomDropdownMenu(customtkinter.CTkFrame):
    
    def __init__(self, 
                 widget: customtkinter.CTkBaseClass | _CDMSubmenuButton,
                 master: any = None,
                 border_width: int = 1,
                 width: int = 150,
                 height: int = 25,
                 bg_color: str | tuple[str, str] = None,
                 corner_radius: int = 10,
                 border_color: str | tuple[str, str] = "grey50",
                 separator_color: str | tuple[str, str] = ["grey80","grey20"],
                 text_color: str | tuple[str, str] = ["black","white"],
                 fg_color: str | tuple[str, str] = "transparent",
                 hover_color: str | tuple[str, str] = ["grey75","grey25"],
                 font: customtkinter.CTkFont = ("helvetica", 12),
                 padx: int = 3,
                 pady: int = 3,
                 cursor: str = "hand2",
                 **kwargs):
        
        if widget.master.winfo_name().startswith("!ctktitlemenu"):
            widget.master.master.bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
            widget.master.master.bind("<Button-1>", self._checkIfMouseLeft, add="+")
            master = widget.master if master is None else master
            widget.master.menu.append(self)
            
        elif widget.master.winfo_name().startswith("!ctkmenubar"):
            widget.winfo_toplevel().bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
            widget.winfo_toplevel().bind("<Button-1>", self._checkIfMouseLeft, add="+")
            master = widget.master.master if master is None else master
            widget.master.menu.append(self)
        else:
            widget.winfo_toplevel().bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
            widget.winfo_toplevel().bind("<Button-1>", self._checkIfMouseLeft, add="+")
            master = widget.master if master is None else master
            
        super().__init__(
            master=master,
            border_width=border_width,
            fg_color=bg_color,
            border_color=border_color,
            corner_radius=corner_radius,
            **kwargs)

        self.border_color = border_color
        self.border_width = border_width
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.menu_seed_object = widget
        self.master = master
        self.menu_seed_object.configure(command=self.toggleShow)
        self.fg_color = fg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.font = font
        self.height = height
        self.width = width
        self.padx = padx
        self.pady = pady
        self.cursor = cursor
        self.hovered = False
        self.is_submenu = False

        self.separator_color = separator_color
        self._options_list: list[_CDMOptionButton | _CDMSubmenuButton] = []
        
    def selectOption(self, command) -> None:
        self._hideAllMenus()
        if command:
            command()
        
    def dummy():
        pass
    
    def add_option(self, option: str, command: Callable=dummy, **kwargs) -> None:
        optionButton = _CDMOptionButton(
            self,
            width = self.width,
            height = self.height,
            text=option,
            anchor="w",
            text_color=self.text_color,
            command=partial(self.selectOption, command), **kwargs)
        optionButton.configure(cursor=self.cursor)
                          
        optionButton.setParentMenu(self)
        self._options_list.append(optionButton)
        self._configureButton(optionButton)

        optionButton.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
        
        if self.is_submenu:
            optionButton.bind("<Enter>", lambda e, submenu=self: submenu.change_hover(self), add="+")
   
        return optionButton

    def add_submenu(self, submenu_name: str, **kwargs) -> "CustomDropdownMenu":
        submenuButtonSeed = _CDMSubmenuButton(self, text=submenu_name, anchor="w",
                                              text_color=self.text_color,
                                              width=self.width, height=self.height, **kwargs)
        submenuButtonSeed.setParentMenu(self)
        self._options_list.append(submenuButtonSeed)
        self._configureButton(submenuButtonSeed)

        submenu = CustomDropdownMenu(
            master=self.master,
            height=self.height,
            width=self.width,
            widget=submenuButtonSeed,
            fg_color=self.fg_color,
            bg_color=self.bg_color,
            hover_color=self.hover_color,
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            border_color=self.border_color,
            separator_color=self.separator_color,
            text_color=self.text_color,
            font=self.font)
        
        submenuButtonSeed.setSubmenu(submenu=submenu)
        submenuButtonSeed.configure(command=submenu.toggleShow)
        submenu.is_submenu = True
        
        submenu.bind("<Enter>", lambda e, sub=self: self.change_hover(self), add="+")
        submenuButtonSeed.bind("<Enter>", lambda e, sub=submenu, button=submenuButtonSeed: self.after(500, lambda: sub._show_submenu(self, button)), add="+")
        submenuButtonSeed.bind("<Leave>", lambda e, sub=submenu: self.after(500, lambda: sub._left(self)), add="+")
        
        submenuButtonSeed.configure(cursor=self.cursor)
        
        submenuButtonSeed.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
        return submenu
        
    def _left(self, parent):
  
        if parent.hovered:
            parent.hovered = False
            return
        
        subMenus = parent._getSubMenus()
        
        for i in subMenus:
            i._hide()
            
    def change_hover(self, parent):
        parent.hovered = True
   
    def _show_submenu(self, parent, button) ->None:
        if self.winfo_viewable():
            return
        
        subMenus = parent._getSubMenus()
        
        for i in subMenus:
            i._hide()
            
        x,y = self.winfo_pointerxy()
        widget = self.winfo_containing(x,y)
    
        if (str(widget)!=str(button._canvas)) and (str(widget)!=str(button._text_label)) and (str(widget)!=str(button._image_label)):
            return
        
        self._show()
            
        
    def add_separator(self) -> None:
        separator = customtkinter.CTkFrame(
            master=self, 
            height=2,
            width=self.width,
            fg_color=self.separator_color, 
            border_width=0
        )
        separator.pack(
            side="top",
            fill="x",
            expand=True,
        )

    def _show(self, *args, **kwargs) -> None:
        dpi = self._get_widget_scaling()
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.place(
                in_=self.menu_seed_object.parent_menu,
                x=(self.menu_seed_object.winfo_x() + self.menu_seed_object.winfo_width())/dpi + self.padx +1,
                y=self.menu_seed_object.winfo_y()/dpi - self.pady)

        else:
            self.place(
                x=self.menu_seed_object.winfo_x()/dpi + self.padx,
                y=(self.menu_seed_object.winfo_y() + self.menu_seed_object.winfo_height())/dpi + self.pady)
        self.lift()
        self.focus()
        
    def _hide(self, *args, **kwargs) -> None:
        self.place_forget()
        
    def _hideParentMenus(self, *args, **kwargs) -> None:
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.menu_seed_object.parent_menu._hideParentMenus()
            self.menu_seed_object.parent_menu._hide()
            
    def _hideChildrenMenus(self, *args, **kwargs) -> None:
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            for option in self._options_list:
                if isinstance(option, _CDMSubmenuButton):
                    option.submenu._hide()
                    
    def _hideAllMenus(self, *args, **kwargs) -> None:
        self._hideChildrenMenus()
        self._hide()
        self._hideParentMenus()
        
    def _collapseSiblingSubmenus(self, button: _CDMOptionButton | _CDMSubmenuButton, *args, **kwargs) -> None:
        for option in self._options_list:
            if option != button and isinstance(option, _CDMSubmenuButton):
                option.submenu._hideChildrenMenus()
                option.submenu._hide()

    def toggleShow(self, *args, **kwargs) -> None:
    
        widget_base = self.menu_seed_object.master.winfo_name()
        if widget_base.startswith("!ctktitlemenu") or widget_base.startswith("!ctkmenubar"):
            for i in self.menu_seed_object.master.menu:
                if i!=self:
                    i._hide()
    
        if not self.winfo_viewable():
            self._show()
            self.lift()
        else:
            self._hideChildrenMenus()
            self._hide()
            
    def _configureButton(self, button: customtkinter.CTkButton) -> None:
        button.configure(fg_color="transparent")
        if self.fg_color:
            button.configure(fg_color=self.fg_color)
        if self.hover_color:
            button.configure(hover_color=self.hover_color)
        if self.font:
            button.configure(font=self.font)

        button.bind("<Enter>", partial(self._collapseSiblingSubmenus, button))
        
    def _getSubMenus(self) -> list["CustomDropdownMenu"]:
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            subMenusList = list()
            for option in self._options_list: 
                if isinstance(option, _CDMSubmenuButton):
                    subMenusList.append(option.submenu)
            return subMenusList
        else:
            return []

    def _get_coordinates(self, x_root, y_root) -> bool:
        return self.winfo_rootx() < x_root < self.winfo_rootx()+self.winfo_width() and \
            self.winfo_rooty() < y_root < self.winfo_rooty()+self.winfo_height()
    
    def _checkIfMouseLeft(self, event: tk.Event=None) -> None:
        if not self.winfo_viewable():
            return
        
        if not self._get_coordinates(event.x_root, event.y_root):
            if isinstance(self.menu_seed_object, _CDMSubmenuButton) and not self.menu_seed_object.parent_menu._get_coordinates(event.x_root, event.y_root):
                subMenus = self._getSubMenus()
                if subMenus == [] or all((not submenu._get_coordinates(event.x_root, event.y_root)) for submenu in subMenus):
                    self._hideAllMenus()
            
            elif not isinstance(self.menu_seed_object, _CDMSubmenuButton):
                subMenus = self._getSubMenus()
                if subMenus == [] or all((not submenu._get_coordinates(event.x_root, event.y_root)) for submenu in subMenus):
                    self._hideAllMenus()

    def configure(self, **kwargs):
      
        if "hover_color" in kwargs:
            self.hover_color = kwargs["hover_color"]

        if "font" in kwargs:
            self.font = kwargs["font"]

        if "text_color" in kwargs:
            self.text_color = kwargs["text_color"]

        if "bg_color" in kwargs:
            self.bg_color = kwargs.pop("bg_color")
            super().configure(fg_color=self.bg_color)

        if "fg_color" in kwargs:
            self.fg_color = kwargs["fg_color"]
            
        if "border_color" in kwargs:
            self.border_color = kwargs.pop("border_color")
            super().configure(border_color=self.border_color)
            
        if "border_width" in kwargs:
            self.border_width = kwargs.pop("border_width")
            super().configure(border_width=self.border_width)
            
        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
            super().configure(corner_radius=self.corner_radius)

        if "height" in kwargs:
            self.height = kwargs["height"]

        if "width" in kwargs:
            self.width = kwargs["width"]

        if "separator_color" in kwargs:
            self.separator_color = kwargs.pop("separator_color")
            for i in self.winfo_children():
                if type(i) is customtkinter.CTkFrame:
                    i.configure(fg_color=self.separator_color)

        if "padx" in kwargs:
            self.padx = kwargs.pop("padx")

        if "pady" in kwargs:
            self.pady = kwargs.pop("pady")

        for widget in self.winfo_children():
            if (type(widget) is _CDMOptionButton) or (type(widget) is _CDMSubmenuButton):
                widget.configure(**kwargs)

    def cget(self, param):
        if param=="hover_color":
            return self.hover_color

        if param=="font":
            return self.font

        if param=="text_color":
            return self.text_color

        if param=="bg_color":
            return self.bg_color

        if param=="border_color":
            return self.border_color 
            
        if param=="border_width":
            return self.border_width
            
        if param=="corner_radius":
            return self.corner_radius
        
        if param=="height":
            return self.height 

        if param=="width":
            return self.width

        if param=="separator_color":
            return self.separator_color

        if param=="padx":
            return self.padx 

        if param=="pady":
            return self.pady

        return super().cget(param)
