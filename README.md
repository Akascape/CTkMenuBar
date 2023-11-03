# CTkMenuBar
Modern menu bar widget library for customtkinter.

## Features
- Custom dropdown menus
- Add menu in top of title bar
- Classic and modern menubar with full customisability
- Add commands and submenus

## Installation

```
pip install CTkMenuBar
```
### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkMenuBar?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/CTkMenuBar/archive/refs/heads/main.zip)

## Menu Types
- ## CTkMenuBar

![menubar](https://github.com/Akascape/CTkMenuBar/assets/89206401/02c512b2-557f-4d59-86e0-a6eb9da3696c)

### Usage
```python
from CTkMenuBar import *
...
menu = CTkMenuBar(master=root)
menu.add_cascade("Menu")
...
```

### Methods
- **.add_cancade(text, ctk_button_args...)**: add new menu button in the menu bar
- .configure(*frame_kwargs)

### Arguments
| Parameter | Description |
|-----------| ------------|
| **master** | define the master widget, can be root or frame |
| bg_color | set the bg color of the menu bar |
| height | set height of the menu bar |
| width | set width of the menu bar buttons |
| padx | set internal padding between menu bar buttons |
| pady | set internal padding in top and bottom of menu bar |
| _*other frame parameters_ | other ctk frame parameters can also be passed |

- ## CTkTitleMenu

_This title menu is only supported in windows OS!_

![titlebar](https://github.com/Akascape/CTkMenuBar/assets/89206401/da6cd858-f700-476c-a2f0-93a1c6335a4d)

### Usage
```python
from CTkMenuBar import *
...
menu = CTkTitleMenu(master=root)
menu.add_cascade("Menu")
...
```

### Methods
- **.add_cancade(text, ctk_button_kwargs...)**: add new menu button in the menu bar

### Arguments
| Parameter | Description |
|-----------| ------------|
| **master** | define the master window, can be **root or toplevel** only |
| bg_color | set the bg color of the menu bar |
| title_bar_color | set color to the header (**only works with windows 11**), `RGB order: 0x00rrggbb` |
| width | set width of the menu bar buttons |
| padx | set internal padding between menu bar buttons |
| x_offset | set the x distance from the header |
| y_offset | set the y distance from the header |
| _*other frame parameters_ | other ctk frame parameters can also be passed |

## CustomDropdownMenu

This is the common dropdown menu class which is used by both ctkmenubar and ctktitlemenu. 

### Usage
```python
from CTkMenuBar import *
...
dropdown = CustomDropdownMenu(widget=button)
dropdown.add_option(option="value") 
dropdown.add_separator() 
submenu = dropdown.add_submenu("submenu") 
subment.add_option(option="value") 
...
```

### Methods
- **.add_option(option, command)**: add option to the dropdown and attach the command
- **.add_separator()**: add a separator line between the options
- **.add_submenu(submenu_name)**: add a submenu as option

### Arguments
| Parameter | Description |
|-----------| ------------|
| **widget** | attach the dropdown to the cascade widget |
| master | *optional*, change the spawn window if required |
| bg_color | set the bg color of the dropdown |
| fg_color | set the option button fg color |
| text_color | set the text color |
| hover_color | set hover color of the option button |
| separator_color | change the separator line color |
| font | change the font of the text |
| width | set width of the dropdown |
| height | set height of the dropdown |
| padx | set padding in x for the dropdown frame |
| pady | set padding in y for the dropdown frame |
| _*other frame parameters_ | other ctk frame parameters can also be passed |

_Credits goes to [LucianoSaldivia](https://github.com/LucianoSaldivia) for providing this dropdown menu class._
