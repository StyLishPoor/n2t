import os
import sys
from enum import Enum

class JackAnalyzer:
    def __init__(self, input_file: str) -> None:
        try:
            self._path = os.path.abspath(input_file)
        except IndexError:
            sys.exit("cannot find the file")
        tokenizer = JackTokenizer(input_file)

        self._f_write = open(input_file.split('.')[0]+'.xml','w')

class Symbol(str,Enum):
    """
    CBL = "{"
    CBR = "}"
    RBL = "("
    RBR = ")"
    SBL = "["
    SBR = "]"
    DOT = "."
    COM = ","
    SCR = ";"
    PLS = "+"
    MNS = "-"
    MUL = "*"
    DIV = "/"
    AND = "&"
    OR  = "|"
    SML = "<"
    BIG = ">"
    EQL = "="
    OTR = "~"
    """
    symbol = {"{","}","(",")","[","]",".",",",";",
            "+","-","*","/","&","|","<",">","=","~"," "}


class JackTokenizer:
    #入力ファイルを開く
    #入力ファイルはhogehoge.jack
    def __init__(self, input_file: str) -> None:
        self.f_read = open(input_file,'r')
        self.tokenlist = []
        self.forcompile = self._str_to_token(self.tokenlist)
        #print(self.forcompile)

    def _str_to_token(self, tokenlist: list) -> list:
        #入力のリストをトークンに分割
        original = self.f_read.readlines()
        #print(original)
        for change in original:
            start = 0
            for i in range(len(change)):
                if change[i]._check_symbol:
                    tokenlist.append(change[start:i])
                    tokenlist.append(change[i])
                    start = i+1
                elif change[i] == " " or change[i] == "\n":
                    tokenlist.append(change[start:i])
                else:
                    pass
        return tokenlist

    def _check_symbol(self,check: str) -> bool:
        if check in Symbol.symbol:
            return True
        return False

    def hasMoreToken(self) -> bool:
        ...
    


class CompilationEngine:
    def __init__(self,input_token: list, output_stream) -> None:
        ...

if __name__ == "__main__":
    args = sys.argv
    print(args)
    token = JackAnalyzer(args[1])