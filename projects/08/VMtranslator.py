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
        return 'C_IF'
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

def CodeWriter(fo,cmd,jmp_num,filename):
    #書き込みのためのストリームをopen
    #fo = open(outfile,'a')
    if commandType(cmd) == 'C_PUSH':
        if arg1(cmd) == 'constant':
            file_write = push_constant(arg2(cmd))
        elif arg1(cmd) == 'static':
            file_write = static_push(arg2(cmd),filename)
        else:
            file_write = push_write(arg1(cmd),arg2(cmd))
        for c in file_write:
            fo.write(c)
    elif commandType(cmd) == 'C_POP':
        if arg1(cmd) == 'static':
            file_write = static_pop(arg2(cmd),filename)
        else:
            file_write = pop_write(arg1(cmd),arg2(cmd))
        for c in file_write:
            fo.write(c)
    elif commandType(cmd) == 'C_LABEL':
        fo.write('('+arg1(cmd)+')\n')
    elif commandType(cmd) == 'C_GO':
        fo.write('@'+arg1(cmd)+'\n')
        fo.write('0;JMP\n')
    elif commandType(cmd) == 'C_IF':
        fo.write('@SP\n')
        fo.write('M=M-1\n')
        fo.write('A=M\n')
        fo.write('D=M\n')
        fo.write('@'+arg1(cmd)+'\n')
        fo.write('D;JNE\n')
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
    


def add():
    to_write = []
    to_write.append('@SP\n')
    to_write.append('M=M-1\n')
    to_write.append('A=M\n')
    to_write.append('D=M\n')
    to_write.append('@SP\n')
    to_write.append('M=M-1\n')
    to_write.append('A=M\n')
    to_write.append('M=M+D\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')

    return to_write
def push_afteradd():
    to_write = []
    to_write.append('@SP\n')
    to_write.append('M=M-1\n')
    to_write.append('A=M\n')
    to_write.append('A=M\n')
    to_write.append('D=M\n')
    to_write.append('@SP\n')
    to_write.append('A=M\n')
    to_write.append('M=D\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')
    return to_write

def pop_afteradd():
    to_write = []
    to_write.append('@SP\n')
    to_write.append('M=M-1\n')
    to_write.append('M=M-1\n')
    to_write.append('A=M\n')
    to_write.append('D=M\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')
    to_write.append('A=M\n')
    to_write.append('A=M\n')
    to_write.append('M=D\n')
    to_write.append('@SP\n')
    to_write.append('M=M-1\n')

    return to_write
def push_constant(N):
    to_write = []
    to_write.append('@'+N+'\n')
    to_write.append('D=A\n')
    to_write.append('@SP\n')
    to_write.append('A=M\n')
    to_write.append('M=D\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')

    return to_write

def pointer_push(N):
    to_write = []
    if N == '0': #THIS への操作
        to_write.append('@THIS\n')
        to_write.append('D=M\n')
        to_write.append('@SP\n')
        to_write.append('A=M\n')
        to_write.append('M=D\n')
        to_write.append('@SP\n')
        to_write.append('M=M+1\n')
    elif N == '1': #THAT への操作
        to_write.append('@THAT\n')
        to_write.append('D=M\n')
        to_write.append('@SP\n')
        to_write.append('A=M\n')
        to_write.append('M=D\n')
        to_write.append('@SP\n')
        to_write.append('M=M+1\n')
    return to_write

def pointer_pop(N):
    to_write = []
    if N == '0': #THIS base addressを書き換える
        to_write.append('@SP\n')
        to_write.append('M=M-1\n')
        to_write.append('A=M\n')
        to_write.append('D=M\n')
        to_write.append('@THIS\n')
        to_write.append('M=D\n')
    if N == '1': #THIS base addressを書き換える
        to_write.append('@SP\n')
        to_write.append('M=M-1\n')
        to_write.append('A=M\n')
        to_write.append('D=M\n')
        to_write.append('@THAT\n')
        to_write.append('M=D\n')

    return to_write

def static_push(N,filename):
    to_write = []
    to_write.append('@'+filename+'.'+N+'\n')
    to_write.append('D=M\n')
    to_write.append('@SP\n')
    to_write.append('A=M\n')
    to_write.append('M=D\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')
    return to_write

def static_pop(N,filename):
    to_write = []
    to_write.append('@SP\n')
    #to_write.append('A=M\n')
    to_write.append('M=M-1\n')
    to_write.append('A=M\n')
    to_write.append('D=M\n')
    to_write.append('@'+filename+'.'+N+'\n')
    to_write.append('M=D\n')
    return to_write

def push_pop_adr(rg_name):
    to_write = []
    to_write.append('@'+rg_name+'\n')
    to_write.append('D=M\n')
    to_write.append('@SP\n')
    to_write.append('A=M\n')
    to_write.append('M=D\n')
    to_write.append('@SP\n')
    to_write.append('M=M+1\n')

    return to_write

def push_write(memory,N):
    if memory == 'local':
        to_write = push_constant(N)
        appendstr = push_pop_adr('LCL')
        appendstr += (add() + push_afteradd())
        to_write += appendstr
        return to_write
    elif memory == 'argument':
        to_write = push_constant(N)
        appendstr = push_pop_adr('ARG')
        appendstr += (add() + push_afteradd())
        to_write += appendstr
        return to_write
    elif memory == 'this':
        to_write = push_constant(N)
        appendstr = push_pop_adr('THIS')
        appendstr += (add() + push_afteradd())
        to_write += appendstr
        return to_write
    elif memory == 'that':
        to_write = push_constant(N)
        appendstr = push_pop_adr('THAT')
        appendstr += (add() + push_afteradd())
        to_write += appendstr
        return to_write
    elif memory == 'pointer':
        to_write = pointer_push(N)
        return to_write
    elif memory == 'temp':
        to_write = push_pop_adr('R'+str((int(N)+5)))
        return to_write


def pop_write(memory,N):
    to_write = []
    if memory == 'local':
        to_write = push_constant(N)
        to_write += push_pop_adr('LCL')
        to_write +=(add() + pop_afteradd())
        return to_write
    elif memory == 'argument':
        to_write = push_constant(N)
        to_write += push_pop_adr('ARG')
        to_write +=(add() + pop_afteradd())
        return to_write
    elif memory == 'this':
        to_write = push_constant(N)
        to_write += push_pop_adr('THIS')
        to_write +=(add() + pop_afteradd())
        return to_write
    elif memory == 'that':
        to_write = push_constant(N)
        to_write += push_pop_adr('THAT')
        to_write +=(add() + pop_afteradd())
        return to_write
    elif memory == 'pointer':
        to_write = pointer_pop(N)
        return to_write
    elif memory == 'temp':
        to_write.append('@SP\n')
        to_write.append('M=M-1\n')
        to_write.append('A=M\n')
        to_write.append('D=M\n')
        to_write.append('@R'+str((int(N)+5))+'\n')
        to_write.append('M=D\n')
        return to_write

fromParse = Parse()
path = '/Users/nora/work/nand2tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.asm'
filename = (path.split('/')[-1]).split('.')[0]
path = os.path.abspath(path)
fo = open(path,'w')
while len(fromParse) >= 1:
    jmp_num = 0
    cmdlist = fromParse.pop(0)
    for cmd in cmdlist:
        jmp_num = CodeWriter(fo,cmd,jmp_num,filename)
"""
fo.write('(INF_LOOP)\n')
fo.write('@INF_LOOP\n')
fo.write('0;JMP')
"""
fo.close()
