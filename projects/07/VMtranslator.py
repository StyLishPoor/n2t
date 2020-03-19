import sys
import os
import glob

def Parse():
    #まず，vmファイルをopen
    args = sys.argv
    fd = []
    if len(args) < 2:
        sys.exit("引数足りないンゴ！")
    else:
        path = os.path.abspath(args[1])

    if os.path.isfile(path):
        filename = path
        f = open(filename,'r',encoding='utf-8')
        fd.append(f)
    if os.path.isdir(path):
        filelist = glob.glob(path+'/'+'*.vm')
        for filename in filelist:
            f = open(filename,'r',encoding='utf-8')
            fd.append(f)

    if len(fd) == 0:
        sys.exit("ファイル名かディレクトリ名が違うンゴ")
    #vmをコマンドに分割
    cmdalllist = []
    for f in fd:
        cmd_tmp = []
        for s in f.readlines():
            #コメントアウトと空行以外をコマンドリストcmdlistに追加
            if (s[0]=='/' and s[1]=='/') or s == '\n':
                continue
            else:
                cmd_tmp.append(s.strip())
        cmdalllist.append(cmd_tmp)
        """
    for cmdlist in cmdalllist:
        while hasMoreCommands(cmdlist):
            cmdnow = advance(cmdlist)
            cmdtype = commandType(cmdnow)
            
            firstarg = arg1(cmdnow)
            secondarg = arg2(cmdnow)
            """
    
    for f in fd:
        f.close()
    return cmdalllist

def hasMoreCommands(cmdl):
    if len(cmdl) >= 1:
        return True
    return False

def advance(cmdl):
    cmd = cmdl.pop(0)
    return cmd

def commandType(cmd):
    allcmd = cmd.split()
    if len(allcmd) == 1:
        if allcmd == 'return':
            return 'C_RETURN'
        else:
            return 'C_ARITHMETIC'
    if allcmd[0] == 'push':
        return 'C_PUSH'
    if allcmd[0] == 'pop':
        return 'C_POP'
    if allcmd[0] == 'label':
        return 'C_LABEL'
    if allcmd[0] == 'goto':
        return 'C_GO'
    if allcmd[0] == 'if-goto':
        return 'C_IF-GOTO'
    if allcmd[0] == 'function':
        return 'C_FUNCTION'
    if allcmd[0] == 'call':
        return 'C_CALL'

def arg1(cmd):
    if commandType(cmd) == 'C_ARITHMETIC':
        return cmd
    else:
        allcmd = cmd.split()
        return allcmd[1]

def arg2(cmd):
    allcmd = cmd.split()
    return allcmd[2]

def CodeWriter(fo,cmd,jmp_num):
    #書き込みのためのストリームをopen
    #fo = open(outfile,'a')
    if commandType(cmd) == 'C_PUSH':
        if arg1(cmd) == 'constant':
            fo.write('@'+arg2(cmd)+'\n')
            fo.write('D=A\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        else:
            #to be continued
            pass 
    elif commandType(cmd) == 'C_ARITHMETIC':
        if arg1(cmd) == 'add':
            #popの操作で抽象化できそう...
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=M+D\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'sub':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=M-D\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'eq':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M-D\n')
            #≠ならjmp
            fo.write('@JMP'+str(jmp_num)+'\n')
            fo.write('D;JNE\n')
            fo.write('D=-1\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('@END'+str(jmp_num)+'\n')
            fo.write('0;JMP\n')
            fo.write('(JMP'+str(jmp_num)+')\n')
            fo.write('D=0\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('(END'+str(jmp_num)+')\n')
            jmp_num += 1
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'lt':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M-D\n')
            #≠ならjmp
            fo.write('@JMP'+str(jmp_num)+'\n')
            fo.write('D;JGE\n')
            fo.write('D=-1\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('@END'+str(jmp_num)+'\n')
            fo.write('0;JMP\n')
            fo.write('(JMP'+str(jmp_num)+')\n')
            fo.write('D=0\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('(END'+str(jmp_num)+')\n')
            jmp_num += 1
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'gt':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M-D\n')
            #≠ならjmp
            fo.write('@JMP'+str(jmp_num)+'\n')
            fo.write('D;JLE\n')
            fo.write('D=-1\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('@END'+str(jmp_num)+'\n')
            fo.write('0;JMP\n')
            fo.write('(JMP'+str(jmp_num)+')\n')
            fo.write('D=0\n')
            fo.write('@SP\n')
            fo.write('A=M\n')
            fo.write('M=D\n')
            fo.write('(END'+str(jmp_num)+')\n')
            jmp_num += 1
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'and':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=M&D\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'or':
            #1pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('D=M\n')
            #2pop目
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=M|D\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'neg':
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=-M\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
        elif arg1(cmd) == 'not':
            fo.write('@SP\n')
            fo.write('M=M-1\n')
            fo.write('A=M\n')
            fo.write('M=!M\n')
            #SP進める
            fo.write('@SP\n')
            fo.write('M=M+1\n')
    return jmp_num    





fromParse = Parse()
path = './StackArithmetic/StackTest/StackTest.asm'
path = os.path.abspath(path)
fo = open(path,'w')
while len(fromParse) >= 1:
    jmp_num = 0
    cmdlist = fromParse.pop(0)
    for cmd in cmdlist:
        jmp_num = CodeWriter(fo,cmd,jmp_num)
"""
fo.write('(INF_LOOP)\n')
fo.write('@INF_LOOP\n')
fo.write('0;JMP')
"""
fo.close()
