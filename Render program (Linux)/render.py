import os
import pathlib
import time
import math
import subprocess
import sys
from tqdm import tqdm
import colorama
import tkinter as tk
from tkinter import filedialog
import shutil
import json
files = []
filed = []
currentFrame = 0
totalFrame = 0
rFrames = 0
currentrFrames = 0
timeNow = 0
timeThen = 0
timeRemains = 0
hours = 0
minutes = 0
seconds = 0
timeRemainString = 0
timeRemainList = []
currentFiles = 0
fileReady = 0
shutdown = False
optimize = False

def fileCheck():
    root = tk.Tk()
    root.withdraw()

    filename = filedialog.askopenfilename(
        title="Select a file...",
        filetypes=[("Blend files", "*.blend")]
    )

    if filename:
        filed.append(filename)
        print(f"Added {filename} to the list.")

    root.destroy()

def prepare():
    with tqdm(range(len(filed)), dynamic_ncols=True, ascii="_123456789#", bar_format="File {n_fmt}/{total_fmt} | {percentage:.2f}% [{bar}]", leave=False) as totalBar:
        errorFiles = []
        for filer in filed:
            command = ['blender', '-b', f'"{filer}"', '-P', "prepare.py"]
            prepareScript = subprocess.run(' '.join(command), capture_output=True, text=True, shell=True)
            lines = prepareScript.stdout.splitlines()
            try:
                with open("/tmp/frameInfo.txt", "r") as frameData:
                    rFram = int(frameData.read())
            except FileNotFoundError:
                errorFiles.append(filer)
            else:
                os.remove("/tmp/frameInfo.txt")
                files.append({"filePath": filer, "rFrames": rFram})
                totalBar.update()
        if errorFiles != []:
            print(f"<!>\nThe prepare script could not find the frames in some or all of your Blender files.\n\nPlease double check them for errors, using the Blender version currently on PATH.\n A thing to watch out for is to make sure your blend file starts from frame 0. It can cause issues if it starts on other frame numbers.\n\nFiles affected:\n{'\n'.join(errorFiles)}")
            sys.exit(0)
        

def start(filePath, currentrFrames, totalBar):
    printFile = filePath.split('/')
    with tqdm(range(currentrFrames), dynamic_ncols=True, ascii="_123456789#", bar_format="Frame {n_fmt}/{total_fmt} | {percentage:.2f}% [{bar}] ({rate_fmt} > {elapsed} = {remaining})", leave=False) as currentBar:
        currentFrame = 0
        for i in range(currentrFrames):
            rendered = subprocess.Popen(f'blender -b "{filePath}" -f {currentFrame}', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            rendered.wait()
            currentFrame = currentFrame + 1
            os.system('clear')
            print('Rendering...\nDo NOT turn off this computer or remove storage media!\nThis may take several hours to complete.\n\nTotal Job')
            totalBar.update()
            print('\n\n' + filePath, end = "")
            currentBar.update()
    files.pop(0)
    
def complete():
    complete = time.strftime('%H:%M:%S %d/%m/%Y', time.localtime(time.time()))
    print(f':)\nRender complete! Completed on {complete}.')
    if shutdown:
        timer = 1800
        while timer != 0:
            print(f"\rThe PC will turn off in {timer // 60:02d}:{timer % 60:02d}", end = "", flush = True)
            time.sleep(1)
            countdown = countdown - 1
        os.system("shutdown now")

def begin(saveData):
    os.system('clear')
    totalFiles = len(files)
    print('Rendering...\nDo NOT turn off this computer or remove storage media!\nThis may take several hours to complete.\n\nTotal Job')
    with tqdm(range(totalFrame, saveData["rFrames"]), dynamic_ncols=True, ascii="_123456789#", bar_format="Frame {n_fmt}/{total_fmt} | {percentage:.2f}% [{bar}] ({rate_fmt} > {elapsed} = {remaining})", leave=False) as totalBar:
        for i in range(totalFiles):
            render = saveData["files"][0]
            filePath = render['filePath']
            currentrFrames = render['rFrames']
            currentFrame = 0
            print('\n\n' + filePath, end = "")
            start(filePath, currentrFrames, totalBar)
    complete()

def main():
    global rFrames
    os.system('clear')
    print('Please wait...')
    os.system('clear')
    strin = '\n'.join(files)
    os.system('clear')
    print(f'Main Menu\n################\n\nStart: Start the job\nAdd: Add files\nRemove <index>: Remove a file at the specified index\nList: List files\nShutdown: Shuts down the computer 30 minutes after the render job\nExit: Exit the program')
    while True:
        cmd = input("> ")
        if cmd.split()[0].lower() == "start":
            if len(filed) == 0:
                print("You can't start the render job because you have no files. Use 'add' to add some files first.")
            else:
                break
        elif cmd.split()[0].lower() == "add":
            fileCheck()
        elif cmd.split()[0].lower() == "remove":
            try:
                del filed[int(cmd.split()[1])]
            except (IndexError, ValueError):
                print("Could not delete the file at that index. Use List to list files.")
        elif cmd.split()[0].lower() == "list":
            strin = '\n'.join(filed)
            print(f'Files:\n\n{strin}')
        # elif cmd.split()[0].lower() == "optimize":
        #    if not optimize:
        #        if os.geteuid() != 0:
        #            print("Optimize requires the program to be ran as root. Please quit the program and restart it with sudo and try again.")
        #        else:
        #            optimize = True
        #            print("Optimization mode has been turned ON.")
        #    elif optimize:
        #        optimize = False
        #        print("Optimization mode has been turned OFF.")
        elif cmd.split()[0].lower() == "exit":
            sys.exit(0)
        elif cmd.split()[0].lower() == "shutdown":
            if not shutdown:
                shutdown = True
                print("The program will now shut down 30 minutes after the job is over.")
            else:
                shutdown = True
                print("The program will not shut down after the job is over.")
    os.system('clear')
    print('Preparing...')
    prepare()
    os.system('clear')
    count = 1
    if files != []:
        for entry in files:
            print(f'{count}: {entry["filePath"]} with {entry["rFrames"]} frames.')
            count += 1
        for dict in files:
            rFrames = rFrames + dict['rFrames']
        print(f'\nIn total there are {rFrames} frames.')
        print(f"\n\n# Notices for Rendering #\n\n- This device's performance will be severely degraded while rendering is in progress, as it will take all avaliable system resources. You should close all other windows before you start, and not use your device while the job is going.\n\n- If you have a supported GPU for Cycles, check out Cycles Render Devices from Blender's Preferences > System. This will put less load on your CPU.\n\n- The program does not choose a place for rendered files to go yet, nor does it choose it's format. It is suggested you double check where they go as well as their format, and if it's in video format, you do not turn off your computer while the job is in progress.")
        print("\n\nPress ENTER when you're ready or press CTRL+C if you changed your mind.")
        input()


    save = {"files": files,
            "totalFrame": totalFrame,
            "rFrames": rFrames
            }
    # if optimize:
    #    with open("/tmp/renderSave.json", "w") as saved:
    #        saved.write(json.dumps(save))
    #    os.execv(sys.executable, os.path.abspath(__file__), "--render"])
    #    sys.exit(0)
    test = json.dumps(save)
    begin(json.loads(test))

if not sys.platform.startswith("linux"):
     print(f"<!>\nYour operating system ({sys.platform}) doesn't support this build of the render program. This is a build for Linux operating systems.")
     sys.exit(0)
if shutil.which("blender") is None:
    print("<!>\nYour computer doesn't have Blender installed or Blender is not on PATH. Please check if Blender is installed on your device or if it's on PATH.")
    sys.exit(0)
if not (pathlib.Path(__file__).resolve().parent / "prepare.py").exists():
    print("<!>\nThe root directory of the render program is missing the prepare script, which it needs to grab frame data for your files from within Blender. Please check if the program installed correctly.")
    sys.exit(0)
main()
