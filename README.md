The code used to hold keys is from [PDF on stack](https://stackoverflow.com/a/73419630/17670556)
without PDF I would have been forced to sacrifice one function or another of my program but thankfully his code
was there to save the day so if you ever see this PDF thank you very much!

#Macro Maker

I started this project almost two years ago at this point as a tool to
build houses in the sims by feeding dimensions into a command line and using
pyautogui to build it. I eventually realized essentially I was producing an extremely
basic version of a macro tool. That is when I scrapped the idea of a sims exclusive tool
and began working on the Macro Maker. When I began work on the initial design of the 
Macro Maker it was messy and redundant code. That was almost a year ago as of 17/February/2023,
and I have developed a lot as a programmer and decided to come revisit one of my oldest projects.

Macro Maker is typed in python using: tkinter, pynput, JSON, time, and threading.

Macro Maker records key presses and events chronologically while also recording duration
allowing for near exact replication of user input.

#Variables you may want to adjust:

Listener.TempData.mouse_movement_buffer: used to space out recorded mouse movements
as without this simply moving your mouse across a modern screen would record kilobytes of
data that truly are not necessary. The default buffer is set to 101 movements because the buffer index
is set to one and cannot be zero.
