import os
import sys
from enum import Enum

class JackAnalyzer:
    def __init__(self, input_file: str) -> None:
        self.input_file = input_file
        try:
            self._path = os.path.abspath(input_file)
        except IndexError:
            sys.exit("cannot find the file")
        self._f_write = open(input_file.split('.')[0]+'Token.xml','w')
        self.fromTokenizer = JackTokenizer(self.input_file)
    def show_tokenlist(self) -> None:
        token = self.fromTokenizer
        towrite = token.output_tokenlist()
        for tmp in towrite:
            self._f_write.write(tmp)
        

class Keyword:
    keyword = {"class","constructor","function","method","field","static",
            "var","int","char","boolean","void","true","false","null",
            "this","let","do","if","else","while","return"}

class Symbol:
    
    symbol = {"{","}","(",")","[","]",".",",",";",
            "+","-","*","/","&","|","<",">","=","~"}



class JackTokenizer:
    #入力ファイルを開く
    #入力ファイルはhogehoge.jack
    def __init__(self, input_file: str) -> None:
        self.f_read = open(input_file,'r')
        self.tokenlist = []
        self.forcompile = self._str_to_token(self.tokenlist)
    def _str_to_token(self, tokenlist: list) -> list:
        #入力のリストをトークンに分割
        inputstr = ""
        #コメントアウトの処理
        commentline: bool = False
        prestr = self.f_read.readline()
        while prestr:
            if commentline == False:
                if "//" in prestr:
                    if prestr.find("//") == 0:
                        prestr = self.f_read.readline()
                        continue
                    inputstr += prestr[0:prestr.find("//")]
                    prestr = self.f_read.readline()

                elif "/*" in prestr:
                    if prestr[2] == "*":
                        prestr = self.f_read.readline()
                        continue
                    else:
                        commentline = True
                        prestr = self.f_read.readline()
                        continue
                else: #コメントが無い行は追加する
                    inputstr += prestr
                    prestr = self.f_read.readline()
            else:
                if "*/" in prestr:
                    commentline = False
                prestr = self.f_read.readline()
        
        inputlist = inputstr.split()
       
        Stringtmp = ""
        StringConstant_flag = False
        for change in inputlist:
            if len(change) == 1:
                tokenlist.append(change)
                continue
            start = 0
            
            if StringConstant_flag:
                if not "\"" in change:
                    Stringtmp += (change + " ")
                else:
                    temp = change.split("\"")
                    Stringtmp += temp[0] + "\""
                    tokenlist.append(Stringtmp)
                    Stringtmp = ""
                    for i in temp[1]:
                        tokenlist.append(i)
                    StringConstant_flag = False
            else:
                for i in range(len(change)):
                    #文字列の一部では無い場合
                    if not StringConstant_flag:
                        if self._check_symbol(change[i]):
                            if start != i:
                                tokenlist.append(change[start:i])
                                tokenlist.append(change[i])
                            else:
                                tokenlist.append(change[i])
                            start = i+1
                        else:
                            if i == len(change)-1:
                                tokenlist.append(change[start:])
                            elif change[i] == "\"":
                                Stringtmp += change[i:] + " "
                                StringConstant_flag = True
                                break
        print(tokenlist)
        return tokenlist

    def _check_symbol(self,check: str) -> bool:
        if check in Symbol.symbol:
            return True
        return False
    def _return_to_Compilation(self) -> list:
        return self.tokenlist

    def hasMoreTokens(self) -> bool:
        if len(self.tokenlist) >= 1:
            return True
        return False
    
    def advance(self) -> str:
        return self.tokenlist.pop(0)

    def tokenType(self, check: str) -> str:
        if check in Keyword.keyword:
            return 'KEYWORD'
        elif check in Symbol.symbol:
            return 'SYMBOL'
        elif "\"" in check:
            return 'STRING_CONST'
        elif check.isdecimal():
            return 'INT_CONST'
        else:
            return 'IDENTIFIER'
    
    def keyword(self,token: str) -> str:
        return token
    def symbol(self, token: str) -> str:
        return token
    def identifier(self, token: str) -> str:
        return token
    def intval(self, token: str) -> str:
        return token
    def stringval(self, token: str) -> str:
        return token[1:-1]
    
    def output_tokenlist(self) -> list:
        output = ["<tokens>\n"]
        while self.hasMoreTokens():
            tmp = self.advance()
            tokentype = self.tokenType(tmp)
            if tokentype == 'KEYWORD':
                tag = 'keyword'
                towrite = self.keyword(tmp)
            elif tokentype == 'SYMBOL':
                tag = 'symbol'
                if self.symbol(tmp) == '<':
                    towrite = '&lt;'
                elif self.symbol(tmp) == '>':
                    towrite = '&gt;'
                elif self.symbol(tmp) == '&':
                    towrite = 'amp;'
                else:
                    towrite = self.symbol(tmp)
            elif tokentype == 'IDENTIFIER':
                tag = 'identifier'
                towrite = self.identifier(tmp)
            elif tokentype == 'INT_CONST':
                tag = 'integerConstant'
                towrite = self.intval(tmp)
            elif tokentype == 'STRING_CONST':
                tag = 'stringConstant'
                towrite = self.stringval(tmp)
            output.append("<" + tag + "> " + towrite + " </" + tag + ">\n" )
        output.append("</tokens>")
        return output

if __name__ == "__main__":
    args = sys.argv
    token = JackAnalyzer(args[1])
    token.show_tokenlist()
    #print(test[0:1])