import os
import shlex, subprocess
import sys, getopt
import logging
import glob
from os.path import basename , dirname
import re
import shutil
file = "Callout.c"
def List2Str(List, Seprator):
    returnStr=""
    if List:
        returnStr = List[0]
        del List[0]
        for x in List:
            returnStr = returnStr + Seprator+x
            
    return(returnStr)
Build_Command = "indent -kr " +file
proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()

Build_Command = "ctags.exe  -x --fields=+S " +file
proc=subprocess.Popen(Build_Command, shell=False,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str, stderr_str = proc.communicate()

Lines = stdout_str.splitlines(True)
for line in Lines:
    Var = []
    #Col=line.split("   ")
    Col = re.split("  +", line)
    if Col[1] == "function":
        x =re.split("[(,)]", Col[3] )
        del x[-1]
        Args = x[:]
        Func = x[0]
        xx = Func.split()
        RetType = "void"
        #print(Func, 1)
        #print(xx, 2)
        if len(xx) == 1:
            FuncName = Func
        elif len(xx) == 2:
            RetType = xx[0]
            FuncName  = xx[1]
        else:
            print("Parsing error !!! ")
        del Args[0]
        x = filter(None, x) 
        #print(x)
        #print(Args)
        NoP = len(x)-1
        if (NoP == 1) and (x[1] == "void" or (not x[1])):
            NoP = 0
        #print(NoP)
        
        ReturnList = []
        if RetType != "void":
            ReturnList.append(RetType+" Ret"+FuncName)
        else:
            RetType = ""
        if NoP != 0:
            for Arg in Args:
                ReturnList.append(Arg.strip())
                yy = Arg.split()
                #print(yy)
                Var.append(yy[-1].strip())
        
        if RetType:
            FunCall = "Ret"+FuncName+"="+FuncName+"("+List2Str(Var,",") +")"
        else:
            FunCall = FuncName+"("+List2Str(Var,",") +")"
            
        ReturnList.append(FunCall) 
            
        final = List2Str(ReturnList,";\n")
        final = final + ";\n"
        #print(ReturnList)
        print(final)

            
    #print(Col)
    #for x in Col:
        #print(x)
if not stderr_str:
    #print(stdout_str)
    print("Done !!! \n")
    print("*"*30)