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

class _CDMSubmenuButton(_CDMOptionButton):
    def setSubmenu(self, submenu: "CustomDropdownMenu"):
        self.submenu = submenu

class CustomDropdownMenu(customtkinter.CTkFrame):
    
    def __init__(self, 
                 widget: customtkinter.CTkBaseClass | _CDMSubmenuButton,
                 master: any = None,
                 border_width: int = 1,
                 width: int = 150,
                 height: int = 25,
                 bg_color = None,
                 corner_radius: int = 10,
                 border_color: str | tuple[str, str] = "grey50",
                 separator_color: str | tuple[str, str] = ["grey80","grey20"],
                 text_color: str | tuple[str, str] = ["black","white"],
                 fg_color: str | tuple[str, str] = "transparent",
                 hover_color: str | tuple[str, str] = ["grey75","grey25"], 
                 font: customtkinter.CTkFont = ("helvetica", 12),
                 padx: int = 3,
                 pady: int = 3,
                 **kwargs):
        
        if widget.master.winfo_name().startswith("!ctktitlemenu"):
            widget.master.master.bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
            master = widget.master if master is None else master
            widget.master.menu.append(self)
            
        elif widget.master.winfo_name().startswith("!ctkmenubar"):
            widget.winfo_toplevel().bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
            master = widget.master.master if master is None else master
            widget.master.menu.append(self)
        else:
            widget.winfo_toplevel().bind("<ButtonPress>", self._checkIfMouseLeft, add="+")
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
        
        optionButton.setParentMenu(self)
        self._options_list.append(optionButton)
        self._configureButton(optionButton)

        optionButton.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
        
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
            hover_color=self.hover_color,
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            border_color=self.border_color,
            separator_color=self.separator_color,
            text_color=self.text_color,
            font=self.font)
        
        submenuButtonSeed.setSubmenu(submenu=submenu)
        submenuButtonSeed.configure(command=submenu.toggleShow)
        
        submenuButtonSeed.bind("<Enter>", lambda e: self.after(500, lambda: submenu._show_submenu(self)))
        submenuButtonSeed.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))
        return submenu
    
    def _show_submenu(self, parent) ->None:
        subMenus = parent._getSubMenus()
        for i in subMenus:
            i._hide()
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
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.place(
                in_=self.menu_seed_object.parent_menu,
                x=self.menu_seed_object.winfo_x() + self.menu_seed_object.winfo_width() + self.padx +1,
                y=self.menu_seed_object.winfo_y() - self.pady)
        else:
            self.place(
                x=self.menu_seed_object.winfo_x() + self.padx ,
                y=self.menu_seed_object.winfo_y() + self.menu_seed_object.winfo_height() + self.pady)
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
                i._hide()
            
        if not self.winfo_manager():
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
