
# Screen Sharing in Roblox

This project is a simple way of doing screen sharing in Roblox, while trying to keep the quality while being performant.


It uses 2 main forms of compression:
- Removing repetition of color data:
  
 (255,255,255), (255,255,255), (255,255,255) -> (255,255,255), 2

 - Removes colors that we're not changed compared to the last frame:

Last Frame:
  (255,255,255), (255,255,255), (255,255,255), (255,255,255)

New Frame: 
(255,255,255), (0,0,0), (255,255,255), (255,255,255)

Output: 
1.1, (0,0,0), 2.1

Hex is used to store the color, but to display how the compression works I used RGB values

## How To Use
Setting this up may require some knowledge, but I will try making it as simple as possible:
 1. If you don't already have Python installed, then install it: https://www.python.org/downloads/
  
  2. Install the required packages (Instructions at the Installation section)
  
  3. Open Screen.py and modify the settings to your liking

  4. Open a CMD line in the directory of the python file, in there type:
  ```bash
  py Screen.py
  ```
  This will run the python file, this part will send the Roblox server your screen

  5. Open up Screen.rbxl, and modify the HTTPAdress variable in the ServerScriptService script, so that it fits the correct IP that it will connect to. (The default setting is for the local host, if you don't want to modify the ip then you can leave this variable alone)

  6. Bit of a heads up: if you are using this in a Roblox server, you will need to port forward or use a service such as PlayIt.gg and then change the HTTPAdress variable in the     .rbxl file
  

## Installation

It's quite simple to install this, you only need a way to port forward (I recommend using PlayIt.gg, if you cannot do it yourself)

You will also need to install the Python packages: 
```bash
pip install -r requirements.txt
```
(run the command in the path of the requirements.txt file)



## Notes
-

- I apologize if this is not properly documentated, since the original meaning behind making this was not to publicize it.

- I am by no way a great python programmer, so I once again apologize for the sloppy documentation and code

- Nonetheless I hope you enjoy it and I would especially love if you would even share your work with this and maybe even contribute to it ;)
## License

[MIT](https://choosealicense.com/licenses/mit/)
