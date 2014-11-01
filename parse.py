import os
import shlex, subprocess
import sys, getopt
import logging
import glob
from os.path import basename , dirname
import re
import shutil
file = "Callout.c"

Build_Command = "indent -kr " +file
proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()

Build_Command = "ctags.exe  -x --fields=+S " +file
proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()

Lines = stdout_str.splitlines(True)
for line in Lines:
    #Col=line.split("   ")
    Col = re.split("  +", line)
    if Col[1] == "function":
        x =re.split("[(,)]", Col[3] )
        print(x)
    print(Col)
    for x in Col:
        print(x)
if not stderr_str:
    print(stdout_str)
    print("Done !!! \n")
    print("*"*30)