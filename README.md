# CTkMenuBar
Modern menu bar widget library for customtkinter.

## Features
- Custom dropdown menu
- Add option in top of title bar
- Classic menubar with all customisability
- Add commands and submenus 

## Installation

### [<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Akascape/CTkMenuBar?&color=white&label=Download%20Source%20Code&logo=Python&logoColor=yellow&style=for-the-badge"  width="400">](https://github.com/Akascape/CTkMenuBar/archive/refs/heads/main.zip)

**Download the source code, paste the `CTkMenuBar` folder in the directory where your program is present.**
## Widget Types:
- **CTkMenuBar**

![menubar](https://github.com/Akascape/CTkMenuBar/assets/89206401/dd67a97b-d75d-4c7a-8a96-03535511e510)

# Usage
```python
from CTkMenuBar import *
...
menu = CTkMenuBar(master=root)
menu.add_cascade("Menu")
...
```

# Methods
- .add_cancade(text="Menu_Name", *ctk_button_kwargs)
- .configure(*frame_kwargs)

# Arguments
| Parameter | Description |
|-----------| ------------|
| **master** | define the master widget, can be root or frame |
| bg_color | set the bg color of the menu bar |
| height | set height of the menu bar |
| width | set width of the menu bar buttons |
| padx | set internal padding between menu bar buttons |
| pady | set internal padding in top and bottom of menu bar |
| _*other frame parameters_ | other ctk frame parameters can also be passed |

- **CTkTitleMenu**

_This title menu is only supported in windows OS_

![titlebar](https://github.com/Akascape/CTkMenuBar/assets/89206401/345901bb-1428-4d1a-bf3e-5c4c46f03f31)

# Usage
```python
from CTkMenuBar import *
...
menu = CTkTitleMenu(master=root)
menu.add_cascade("Menu")
...
```

# Methods
- .add_cancade(text="Menu_Name", *ctk_button_kwargs)

# Arguments
| Parameter | Description |
|-----------| ------------|
| **master** | define the master window, can be **root or toplevel** only |
| bg_color | set the bg color of the menu bar |
| title_bar_color | set color to the header (only works with window 11), `RGB order: 0x00rggbb` |
| width | set width of the menu bar buttons |
| padx | set internal padding between menu bar buttons |
| x_offset | set the x distance from the header |
| y_offset | set the y distance from the header |
| _*other frame parameters_ | other ctk frame parameters can also be passed |
