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
    """
    Internal button class for dropdown menu options.
    
    This class extends CTkButton to provide custom functionality for dropdown menu options,
    including parent menu reference and custom configuration methods.
    """
    
    def setParentMenu(self, menu: "CustomDropdownMenu"):
        """
        Set the parent menu for this option button.
        
        Args:
            menu (CustomDropdownMenu): The parent dropdown menu instance.
        """
        self.parent_menu = menu

    def cget(self, param):
        """
        Get configuration value for the button.
        
        Args:
            param (str): The parameter name to retrieve.
            
        Returns:
            The value of the specified parameter. Returns text value for 'option' parameter,
            otherwise delegates to parent class cget method.
        """
        if param=="option":
            return self.cget("text")
        return super().cget(param)
    
    def configure(self, **kwargs):
        """
        Configure the button with custom options.
        
        Args:
            **kwargs: Configuration options. 'option' key will be mapped to 'text' parameter.
        """
        if "option" in kwargs:
            super().configure(text=kwargs.pop("option"))
        super().configure(**kwargs)
        
class _CDMSubmenuButton(_CDMOptionButton):
    """
    Internal button class for dropdown menu submenu options.
    
    This class extends _CDMOptionButton to provide submenu functionality,
    allowing buttons to open child dropdown menus.
    """
    
    def setSubmenu(self, submenu: "CustomDropdownMenu"):
        """
        Set the submenu for this button.
        
        Args:
            submenu (CustomDropdownMenu): The submenu instance to associate with this button.
        """
        self.submenu = submenu
        
    def cget(self, param):
        """
        Get configuration value for the submenu button.
        
        Args:
            param (str): The parameter name to retrieve.
            
        Returns:
            The value of the specified parameter. Returns text value for 'submenu_name' parameter,
            otherwise delegates to parent class cget method.
        """
        if param=="submenu_name":
            return self.cget("text")
        return super().cget(param)
    
    def configure(self, **kwargs):
        """
        Configure the submenu button with custom options.
        
        Args:
            **kwargs: Configuration options. 'submenu_name' key will be mapped to 'text' parameter.
        """
        if "submenu_name" in kwargs:
            super().configure(text=kwargs.pop("submenu_name"))
        super().configure(**kwargs)
        
class CustomDropdownMenu(customtkinter.CTkFrame):
    """
    A custom dropdown menu widget for CTkMenuBar.
    
    This class creates a customizable dropdown menu that can be attached to any widget.
    It supports nested submenus, separators, and various styling options.
    
    Attributes:
        menu_seed_object: The widget that triggers this dropdown menu
        _options_list: List of option buttons and submenu buttons in this menu
        is_submenu: Boolean indicating if this is a submenu
        hovered: Boolean indicating if the menu is currently being hovered over
    """
    
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
        """
        Initialize a CustomDropdownMenu instance.
        
        Args:
            widget: The widget that will trigger this dropdown menu
            master: Parent widget (auto-determined if None)
            border_width: Width of the menu border
            width: Width of the dropdown menu
            height: Height of menu items
            bg_color: Background color of the menu
            corner_radius: Corner radius for rounded corners
            border_color: Color of the menu border
            separator_color: Color of separator lines
            text_color: Color of menu text
            fg_color: Foreground color
            hover_color: Color when hovering over items
            font: Font for menu text
            padx: Horizontal padding
            pady: Vertical padding
            cursor: Mouse cursor type
            **kwargs: Additional arguments passed to parent CTkFrame
        """
        
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
        """
        Execute the command for a selected option and hide all menus.
        
        Args:
            command: The callback function to execute when option is selected
        """
        self._hideAllMenus()
        if command:
            command()
        
    def dummy():
        """
        Default empty function used as placeholder for menu options without commands.
        
        This function serves as a no-op callback for menu items that don't need
        to execute any specific action when selected.
        """
        pass
    
    def add_option(self, option: str, command: Callable=dummy, **kwargs) -> None:
        """
        Add a menu option button to the dropdown menu.
        
        Args:
            option (str): The text label for the menu option
            command (Callable): The callback function to execute when option is selected
            **kwargs: Additional configuration options for the button
            
        Returns:
            _CDMOptionButton: The created option button widget
        """
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
        """
        Add a submenu to the dropdown menu.
        
        Args:
            submenu_name (str): The text label for the submenu button
            **kwargs: Additional configuration options for the submenu button
            
        Returns:
            CustomDropdownMenu: The created submenu instance
        """
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
    
        submenuButtonSeed.configure(cursor=self.cursor)
        
        submenuButtonSeed.pack(
            side="top",
            fill="both", 
            expand=True,
            padx=3+(self.corner_radius/5),
            pady=3+(self.corner_radius/5))

        submenu._timer_id = None
        def show_submenu_delayed():
            if submenu._timer_id:
                self.after_cancel(submenu._timer_id)
            submenu._timer_id = self.after(500, lambda: submenu._show_submenu(self, submenuButtonSeed))

        def hide_submenu_delayed():
            if submenu._timer_id:
                self.after_cancel(submenu._timer_id)
            submenu._timer_id = self.after(500, lambda: submenu._left(self))

        submenuButtonSeed.bind("<Enter>", lambda e: show_submenu_delayed(), add="+")
        submenuButtonSeed.bind("<Leave>", lambda e: hide_submenu_delayed(), add="+")
        return submenu
        
    def _left(self, parent):
        """
        Handle mouse leave event for submenu hiding logic.
        
        Args:
            parent: The parent menu instance
        """
  
        if parent.hovered:
            parent.hovered = False
            return
        
        subMenus = parent._getSubMenus()
        
        for i in subMenus:
            i._hide()
            
    def change_hover(self, parent):
        """
        Set the hovered state for the parent menu.
        
        Args:
            parent: The parent menu instance to set as hovered
        """
        parent.hovered = True
   
    def _show_submenu(self, parent, button) ->None:
        """
        Show the submenu when hovering over a submenu button.
        
        Args:
            parent: The parent menu instance
            button: The submenu button that was hovered over
        """
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
        """
        Add a visual separator line to the dropdown menu.
        
        Creates a thin horizontal line that visually separates menu items.
        """
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

    def remove_option(self, option_name: str) -> bool:
        """
        Remove a menu option or submenu by its text name.
        
        Searches through all menu options and submenus to find and remove
        the item with the specified text. Also removes any associated submenus.
        
        Args:
            option_name (str): The text name of the option to remove
            
        Returns:
            bool: True if the option was found and removed, False otherwise
        """
        for i, option in enumerate(self._options_list):
            if option.cget("text") == option_name:
                # If it's a submenu button, destroy the submenu first
                if isinstance(option, _CDMSubmenuButton):
                    option.submenu.clean()
                    option.submenu.destroy()
                
                # Remove from options list and destroy the button
                self._options_list.pop(i)
                option.destroy()
                return True
        return False
    
    def clean(self) -> None:
        """
        Remove all menu options, submenus, and separators from the dropdown menu.
        
        This method clears the entire menu content, destroying all buttons,
        submenus, and separators. The menu frame itself remains intact but empty.
        """
        # Hide the menu first to prevent display issues
        self._hide()
        
        # Destroy all submenu instances first
        for option in self._options_list:
            if isinstance(option, _CDMSubmenuButton):
                option.submenu.clean()
                option.submenu.destroy()
        
        # Clear the options list
        self._options_list.clear()
        
        # Destroy all child widgets (buttons, separators, etc.)
        for child in self.winfo_children():
            child.destroy()

    def _show(self, *args, **kwargs) -> None:
        """
        Show the dropdown menu at the appropriate position.
        
        Calculates and sets the position of the menu relative to its seed object.
        For submenus, positions to the right of the parent. For main menus,
        positions below the trigger widget.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
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
        """
        Hide the dropdown menu by removing it from its parent.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self.place_forget()
        
    def _hideParentMenus(self, *args, **kwargs) -> None:
        """
        Hide all parent menus recursively.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if isinstance(self.menu_seed_object, _CDMSubmenuButton):
            self.menu_seed_object.parent_menu._hideParentMenus()
            self.menu_seed_object.parent_menu._hide()
            
    def _hideChildrenMenus(self, *args, **kwargs) -> None:
        """
        Hide all child submenus of this menu.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            for option in self._options_list:
                if isinstance(option, _CDMSubmenuButton):
                    option.submenu._hide()
                    
    def _hideAllMenus(self, *args, **kwargs) -> None:
        """
        Hide all menus including children, self, and parents.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        self._hideChildrenMenus()
        self._hide()
        self._hideParentMenus()
        
    def _collapseSiblingSubmenus(self, button: _CDMOptionButton | _CDMSubmenuButton, *args, **kwargs) -> None:
        """
        Collapse sibling submenus when hovering over a different menu item.
        
        Args:
            button: The currently hovered button
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        for option in self._options_list:
            if option != button and isinstance(option, _CDMSubmenuButton):
                option.submenu._hideChildrenMenus()
                option.submenu._hide()

    def toggleShow(self, *args, **kwargs) -> None:
        """
        Toggle the visibility of the dropdown menu.
        
        Shows the menu if it's hidden, hides it if it's visible. Also handles
        hiding other menus when part of a menu bar or title menu.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
    
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
        """
        Configure styling and behavior for a menu button.
        
        Args:
            button (customtkinter.CTkButton): The button to configure
        """
        button.configure(fg_color="transparent")
        if self.fg_color:
            button.configure(fg_color=self.fg_color)
        if self.hover_color:
            button.configure(hover_color=self.hover_color)
        if self.font:
            button.configure(font=self.font)

        button.bind("<Enter>", partial(self._collapseSiblingSubmenus, button))
        
    def _getSubMenus(self) -> list["CustomDropdownMenu"]:
        """
        Get a list of all submenus associated with this menu.
        
        Returns:
            list[CustomDropdownMenu]: List of submenu instances, empty list if none exist
        """
        if any(isinstance(option, _CDMSubmenuButton) for option in self._options_list):
            subMenusList = list()
            for option in self._options_list: 
                if isinstance(option, _CDMSubmenuButton):
                    subMenusList.append(option.submenu)
            return subMenusList
        else:
            return []

    def _get_coordinates(self, x_root, y_root) -> bool:
        """
        Check if given root coordinates are within this menu's bounds.
        
        Args:
            x_root (int): X coordinate in root window coordinates
            y_root (int): Y coordinate in root window coordinates
            
        Returns:
            bool: True if coordinates are within menu bounds, False otherwise
        """
        return self.winfo_rootx() < x_root < self.winfo_rootx()+self.winfo_width() and \
            self.winfo_rooty() < y_root < self.winfo_rooty()+self.winfo_height()
    
    def _checkIfMouseLeft(self, event: tk.Event=None) -> None:
        """
        Check if mouse has left the menu area and hide menus accordingly.
        
        This method is bound to mouse events and determines when to hide the menu
        based on mouse position relative to the menu and its submenus.
        
        Args:
            event (tk.Event, optional): The mouse event containing position information
        """
        try:
            if not self.winfo_viewable():
                return
        except tk.TclError:
            # Widget has been destroyed, nothing to do
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
        """
        Configure the dropdown menu with various styling and behavior options.
        
        This method allows updating menu appearance and behavior after creation.
        Configuration changes are applied to both the menu and its child widgets.
        
        Args:
            **kwargs: Configuration options including:
                - hover_color: Color when hovering over menu items
                - font: Font for menu text
                - text_color: Color of menu text
                - bg_color: Background color of the menu
                - fg_color: Foreground color
                - border_color: Color of the menu border
                - border_width: Width of the menu border
                - corner_radius: Corner radius for rounded corners
                - height: Height of menu items
                - width: Width of the dropdown menu
                - separator_color: Color of separator lines
                - padx: Horizontal padding
                - pady: Vertical padding
        """
      
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
        """
        Get configuration value for the dropdown menu.
        
        Args:
            param (str): The parameter name to retrieve
            
        Returns:
            The value of the specified parameter. Supports custom parameters like
            hover_color, font, text_color, bg_color, border_color, border_width,
            corner_radius, height, width, separator_color, padx, and pady.
            For other parameters, delegates to parent class cget method.
        """
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
