import bpy
import os
with open("/tmp/frameInfo.txt", "w") as frameData:
    frameData.write(str(bpy.data.scenes["Scene"].frame_end + 1))
