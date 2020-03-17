
def Assembler(path):
    with open(path) as f:
        cmdlist = []
        symbollist = []
        ramstart = 16
        binarylist = []
        for s in f.readlines():
            #コメントアウトと空行以外をコマンドリストcmdlistに追加
            if (s[0]=='/' and s[1]=='/') or s == '\n':
                continue
            else:
                cmdlist.append(s.strip())
    symbollist = FirstSymbolCheck(cmdlist,symbollist)
    while hasMoreCommands(cmdlist):
        cmdnow = advance(cmdlist) 
        cmdtype = commandType(cmdnow)
        #cmdsymbol = symbol(cmdnow)
        if cmdtype == 'C_COMMAND':
            C_dest = dest(cmdnow)
            C_comp = comp(cmdnow)
            C_jump = jump(cmdnow)
            binary = C_Code(C_dest,C_comp,C_jump)
            binarylist.append(binary)
        elif cmdtype == 'A_COMMAND':
            binary,ramstart = A_Code(cmdnow,symbollist,ramstart)
            binarylist.append(binary)
        else:
            pass
        cmdlist.pop(0)
    for l in binarylist:
        print(l)


def hasMoreCommands(cmdl):
    if len(cmdl) >= 1:
        return True
    return False

def advance(cmdl):
    return cmdl[0]

def commandType(cmd):
    if cmd[0]=='@':
        return 'A_COMMAND'
    elif cmd[0]=='(' and cmd[-1]==')':
        return 'L_COMMAND'
    else:
        return 'C_COMMAND'
def dest(cmd):
    dest = cmd.split('=')
    d1,d2,d3 = '0'*3
    if len(dest)==1:
        return '000'
    else:
        if 'M' in dest[0]:
            d3 = '1'
        if 'D' in dest[0]:
            d2 = '1'
        if 'A' in dest[0]:
            d1 = '1'
    return d1+d2+d3
#汚コードにつき閲覧注意！！
def comp(cmd):
    comp = cmd.split('=')
    if len(comp) == 1:
        jmp = comp[0].split(';')
        check = jmp[0]
    else:
        check = comp[1]
    a,c1,c2,c3,c4,c5,c6 = '0'*7
    if 'M' in check:
        a = '1'
    if check == '0':
        c1,c3,c5 = '1'*3
    elif check == '1':
        c1,c2,c3,c4,c5,c6 = '1'*6
    elif check == '-1':
        c1,c2,c3,c5 = '1'*4
    elif check == 'D':
        c3,c4 = '1'*2
    elif check == 'A' or check == 'M':
        c1,c2 = '1'*2
    elif check == '!D':
        c3,c4,c6 = '1'*3
    elif check == '!A' or check == '!M':
        c1,c2,c6 = '1'*3
    elif check == '-D':
        c3,c4,c5,c6 = '1'*4
    elif check == '-A' or check == '-M':
        c1,c2,c5,c6 = '1'*4
    elif check == 'D+1':
        c2,c3,c4,c5,c6 = '1'*5
    elif check == 'A+1' or check == 'M+1':
        c1,c2,c4,c5,c6 = '1'*5
    elif check == 'D-1':
        c3,c4,c5 = '1'*3
    elif check == 'A-1' or check == 'M-1':
        c1,c2,c5 = '1'*3
    elif check == 'D+A' or check == 'D+M':
        c5 = '1'
    elif check == 'D-A' or check == 'D-M':
        c2,c5,c6 = '1'*3
    elif check == 'A-D' or check == 'M-D':
        c4,c5,c6 = '1'*3
    elif check == 'D&A' or check == 'D&M':
        pass
    elif check == 'D|A' or check == 'D|M':
        c2,c4,c6 = '1'*3

    return a+c1+c2+c3+c4+c5+c6
def jump(cmd):
    jmp = cmd.split(';')
    if len(jmp) == 1:
        return '000'
    else:
        check = jmp[1]
    j1,j2,j3 = '0'*3
    if check == 'JGT':
        j3 = '1'
    elif check == 'JEQ':
        j2 = '1'
    elif check == 'JGE':
        j2,j3 = '1'*2
    elif check == 'JLT':
        j1 = '1'
    elif check == 'JNE':
        j1,j3 = '1'*2
    elif check == 'JLE':
        j1,j2 = '1'*2
    elif check == 'JMP':
        j1,j2,j3 = '1'*3
    return j1+j2+j3

def C_Code(de,co,ju):
    return '111'+co+de+ju
def A_Code(cmd,symboltable,ram):
    if cmd[1:].isdecimal():
        value = int(cmd[1:])
        binary_value = change_to_binary(value)
        return binary_value,ram
    else:
        val = cmd[1:]
        for symbol in symboltable:
            if val == symbol[0]:
                binary_value = change_to_binary(symbol[1])
                return binary_value,ram
        symboltable.append([val,ram])
        binary_value = change_to_binary(ram)
        return binary_value,ram+1   


def change_to_binary(num):
    binary = format(num,'016b')
    return str(binary)

def FirstSymbolCheck(cmdlist,symbollist):
    #まず，定義済みシンボルを追加
    symbollist.append(['SP',0])
    symbollist.append(['LCL',1])
    symbollist.append(['ARG',2])
    symbollist.append(['THIS',3])
    symbollist.append(['THAT',4])
    symbollist.append(['R0',0])
    symbollist.append(['R1',1])
    symbollist.append(['R2',2])
    symbollist.append(['R3',3])
    symbollist.append(['R4',4])
    symbollist.append(['R5',5])
    symbollist.append(['R6',6])
    symbollist.append(['R7',7])
    symbollist.append(['R8',8])
    symbollist.append(['R9',9])
    symbollist.append(['R10',10])
    symbollist.append(['R11',11])
    symbollist.append(['R12',12])
    symbollist.append(['R13',13])
    symbollist.append(['R14',14])
    symbollist.append(['R15',15])
    symbollist.append(['SCREEN',16384])
    symbollist.append(['KBD',24576])
    cmd_row = 0
    for cmd in cmdlist:
        if cmdcheck(cmd): 
            symbollist.append([cmd[1:-1],cmd_row])
        else:
            cmd_row += 1
    return symbollist

def cmdcheck(cmd):
    if cmd[0] == '(' and cmd[-1] == ')':
        return True
    return False


asm = input("Input asm path:")
#とりあえず結果は標準出力
Assembler(asm)



