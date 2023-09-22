
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
1.1, (250,255,250), 2.1

Hex is used to store the color, but to display how the compression works I used RGB values





Notes:
-

- I apologize if this is not properly documentated, since the original meaning behind making this was not to publicize it.

- I am by no way a great python programmer, so I once again apologize for the sloppy documentation and code

- Nonetheless I hope you enjoy it and I would especially love if you would even share your work with this and maybe even contribute to it ;)
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Installation

It's quite simple to install this, you only need a way to port forward (I recommend using PlayIt.gg, if you cannot do it yourself)

You will also need to install the Python packages:
```bash
pip install -r requirements.txt
```
(run the command in the path of the requirements.txt file)
    
