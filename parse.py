import os
import shlex, subprocess
import sys, getopt
import logging
import glob
from os.path import basename , dirname
import re
import shutil
import getopt 

opts, args = getopt.getopt(sys.argv[1:], 'x:y:')
#print(opts, args)
if len(sys.argv) == 1:
    file = "Callout.c"
else :
    file = sys.argv[1]
    
#print(sys.argv)
def List2Str(List, Seprator):
    returnStr=""
    if List:
        returnStr = List[0]
        del List[0]
        for x in List:
            returnStr = returnStr + Seprator+x
    return returnStr
def Interprate(TypeAndName):
    TypeAndName=TypeAndName.strip()
    returnDic = {"type":"", "name":""}
    x = re.split(" +", TypeAndName)
    if len(x) == 0:
        print("parse error")
    elif len(x) == 1:
        returnDic["type"] = "void"
        returnDic["name"] = "TypeAndName"
    elif len(x) ==2:
        returnDic["type"] = x[0]
        returnDic["name"] = x[1]
    else:
        returnDic["type"] = List2Str(x[0:len(x)-2], " ")
        returnDic["name"] = x[-1]  
    m =     returnDic["name"].find("*")
    if m != "-1":
        returnDic["type"] = returnDic["type"] + returnDic["name"][0:m+1]
        returnDic["name"] = returnDic["name"][m+1:]
    #print(x)
    #print(returnDic)
    return    returnDic
    
    return(returnStr)
def GetTest(file):
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
            
            Col[3] =Col[3].replace("extern","")
            Col[3] =Col[3].replace("static","")
            x =re.split("[(,)]", Col[3] )
            del x[-1]
            Args = x[:]
            Func = x[0]

            FuncDic = Interprate(Func)
            xx = Func.split()
            RetType = "void"
            #print(Func, 1)
            #print(line)
            if len(xx) == 1:
                FuncName = Func
            elif len(xx) == 2:
                RetType = xx[0]
                FuncName  = xx[1]
            else:
                print("Parsing error !!! ")
                
            RetType = FuncDic["type"]
            FuncName  = FuncDic["name"]
            #print(RetType,FuncName)
            del Args[0]
            x = filter(None, x) 
            #print(x)
            #print(x[1])
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
                    ##print(yy)
                    Var.append(yy[-1].strip())
            #print(List2Str(Var,","), 3)
            if Var:
                P = List2Str(Var,",")
            else:
                P = ""
            if RetType:
                FunCall = "Ret"+FuncName+"="+FuncName+"("+P +")"
            else:
                FunCall = FuncName+"("+List2Str(Var,",") +")"
                
            ReturnList.append(FunCall) 
            #print(ReturnList)    
            final = List2Str(ReturnList,";\n")
            
            final = final + ";\n"
            print(final)
            
            

                
        #print(Col)
        #for x in Col:
            #print(x)
    if not stderr_str:
        #print(stdout_str)
        print(file+ " Done !!! \n")
        print("*"*30)
        
def main():
    GetTest(file)
main()