Bulk Render is a render program that takes multiple Blend files and renders their frame range in a queue!

# Installation
Requirements:
- The release build specifically for your OS
> Linux builds will get updates faster than Windows builds, as I'm a Linux user

- Python (Version is not enforced, but 3.12+ is suggested)
- Blender 3+
- The pip modules in requirements.txt
> - The modules can be installed with `pip install -r requirements.txt`, or `python -m pip install requirements.txt`
> - - Your OS might complain about this if you don't use a virtual environment, if you're on Linux.

prepare.py
> - The program needs this file so Blender can tell it how many frames a file has in it's range. If this file is missing, the program won't run. The prepare script is also not designed to be ran alone.

# Using the Program
If all loads well, you'll get to the Main Menu.

The commands are:
- `start`: Prepares the render job with the current list of files, and starts it when you're ready.
- `add`: Opens a file dialog to add `.blend` files to the list.
- `remove <index>`: Removes the file at the specified index. 
> The index is the position your files are on the list; starting from 0. So if my file is 4th on the list, it's index is 3.

- `list`: Shows the list of files.
- `shutdown`: Toggles a flag telling the render program to shut down your computer 30 minutes after the job is done.
> - Even with the flag ON, you can cancel the shutdown by pressing `Control+C` while the countdown ticks.

# Notices about the Program and Rendering:
- This program is just a bulk renderer, it uses Blender's command line to render your .blend files. It does it from frame 0 to the end of it's frame range as is with no changes.
- Blend files with Scenes called anything other than `Scene` is not fully supported yet. It only supports scenes called `Scene`.
- Scenes with frame ranges starting from frame 1 or higher is not supported yet, frame ranges will start at 0.
- The program does not handle the location where your output files go nor does it handle the format in which they're in. I suggest you do the format as .pngs, therefore you can cancel the render program and pick up where you left off by turning off the Overwrite setting in Blender. If you do it in a video format, **turning off your computer and/or removing the storage media the blend file is located can cause the video file to become corrupted!**
- **The render program has a known issue where Blender does one frame in the command line, then restarts to do the next.** This was an issue with the way Blender's command line works, and unfortunately, it **does bottleneck render times.**
