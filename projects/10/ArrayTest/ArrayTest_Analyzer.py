import os
import sys
from enum import Enum

class JackAnalyzer:
    def __init__(self, input_file: str,output_file: str) -> None:
        self.input_file = input_file
        try:
            self._path = os.path.abspath(input_file)
        except IndexError:
            sys.exit("cannot find the file")
        self.output_file = output_file
        self._f_write = open(input_file.split('.')[0]+'Token.xml','w')
        self._f_truewrite = open(output_file.split('.')[0]+'True.xml','w')
        self.fromTokenizer = JackTokenizer(self.input_file)
        self.show_tokenlist()
        self.fromCompilationEngine = CompilationEngine(self.fromTokenizer, self._f_truewrite)
    def show_tokenlist(self) -> None:
        towrite = self.fromTokenizer.forcompile
        for tmp in towrite:
            self._f_write.write(tmp) 
    def compile(self):
        self.fromCompilationEngine.output_write()

class Keyword:
    keyword = {"class","constructor","function","method","field","static",
            "var","int","char","boolean","void","true","false","null",
            "this","let","do","if","else","while","return"}

class Symbol:
    
    symbol = {"{","}","(",")","[","]",".",",",";",
            "+","-","*","/","&",";","|","<",">","=","~"}
    op = {"+","-","*","/","","|","&amp;","&gt;","&lt;","="}
    unaryOp = {"-","~"}


class JackTokenizer:
    #入力ファイルを開く
    #入力ファイルはhogehoge.jack
    def __init__(self, input_file: str) -> None:
        self.f_read = open(input_file,'r')
        self.tokenlist = []
        self.tokenlist = self._str_to_token(self.tokenlist)
        self.forcompile = self.output_tokenlist()
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
                    if not "*/" in prestr:
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

class CompilationEngine:
    def __init__(self, tokenizer: JackTokenizer, output_stream) -> None:
        self.tokenizer = tokenizer
        self.output_stream = output_stream
        self.tokenlist = self.tokenizer.forcompile
        self.tokenlist.pop(0)
        self.tokenlist.pop(-1)
        self.index = 0
        self.compileresult = []
        self.compileClass()
    def compileClass(self) -> None:
        self.compileresult.append("<class>\n")
        if 'class' in self.tokenlist[self.index]:
            self.compileTerminal() #class
        else:
            sys.exit("class compile error")
        self.compileTerminal() #className
        self.compileTerminal() #{
        while 'static' in self.tokenlist[self.index] or 'field' in self.tokenlist[self.index]:
            self.compileClassVarDec()
        while 'constructor' in self.tokenlist[self.index] or 'function' in self.tokenlist[self.index] or 'method' in self.tokenlist[self.index]:
            self.compileSubroutine()
        self.compileTerminal() # '}'
        self.compileresult.append('</class>\n')
    def compileClassVarDec(self) -> None:
        self.compileresult.append("<classVarDec>\n")
        self.compileTerminal() # ('static' | 'field')
        self.compileTerminal() # type
        self.compileTerminal() # varName
        while not self.tokenlist[self.index] in ';':
            self.compileTerminal() # ','
            self.compileTerminal() # VarName
        self.compileTerminal() # ;
        self.compileresult.append("</classVarDec>\n")
    def compileSubroutine(self) -> None:
        self.compileresult.append("<subroutineDec>\n")
        self.compileTerminal() # ('constructor' | 'function' | 'method')
        self.compileTerminal() # ('void' | type)
        self.compileTerminal() # subroutineName
        self.compileTerminal() # '('
        self.compileParameterList() # parameterList
        self.compileTerminal() # ')'
        self.compileresult.append('<subroutineBody>\n')
        self.compileTerminal() # '{'
        while 'var' in self.tokenlist[self.index]:
            self.compileVarDec() # VarDec*
        self.compileStatements() # statements
        self.compileTerminal() # '}'
        self.compileresult.append('</subroutineBody>\n')
        self.compileresult.append("</subroutineDec>\n")
    def compileParameterList(self) -> None:
        self.compileresult.append('<parameterList>\n')
        while not ')' in self.tokenlist[self.index]:
            self.compileTerminal() #ParameterList
        self.compileresult.append('</parameterList>\n')
    def compileVarDec(self) -> None:
        self.compileresult.append('<varDec>\n')
        while not ';' in self.tokenlist[self.index]:
            self.compileTerminal()
        self.compileTerminal() # ';'
        self.compileresult.append('</varDec>\n')
    def compileStatements(self) -> None:
        self.compileresult.append('<statements>\n')
        while True:
            checknum = [0,1,2,3,4]
            print("statements:  ", self.tokenlist[self.index])
            if "let" == self.tokenlist[self.index].split()[1]:
                print(checknum[0])
                self.compileLet()
                print(checknum[0])
                continue
            elif "if" == self.tokenlist[self.index].split()[1]:
                print(checknum[1])
                self.compileIf()
                print(checknum[1])
                continue
            elif "while" == self.tokenlist[self.index].split()[1]:
                print(checknum[2])
                self.compileWhile()
                print(checknum[2])
                continue
            elif "do" == self.tokenlist[self.index].split()[1]:
                print(checknum[3])
                self.compileDo()
                print(checknum[3])
                continue
            elif "return" == self.tokenlist[self.index].split()[1]:
                print(checknum[4])
                self.compileReturn()
                print(checknum[4])
                continue
            else:
                self.compileresult.append('</statements>\n')
                break
                
    def compileDo(self) -> None:
        self.compileresult.append('<doStatement>\n')
        self.compileTerminal() # 'do'
        if "(" in self.tokenlist[self.index + 1]: #subroutineCall
                self.compileTerminal() # 'subroutineName
                self.compileTerminal() # '('
                self.compileExpressionList() # expressionList
                self.compileTerminal() # ')' 
        elif "." in self.tokenlist[self.index + 1]:
            self.compileTerminal() # (className | varName)
            self.compileTerminal() # '.'
            self.compileTerminal() # 'subroutineName
            self.compileTerminal() # '('
            self.compileExpressionList() # expressionList
            self.compileTerminal() # ')' 
        self.compileTerminal() # ';'
        self.compileresult.append('</doStatement>\n')
    def compileLet(self) -> None:
        self.compileresult.append('<letStatement>\n')
        self.compileTerminal() # 'let'
        self.compileTerminal() # 'varName'
        if "[" in self.tokenlist[self.index]:
            self.compileTerminal() # '['
            self.compileExpression() # expression
            self.compileTerminal() # ']'
        
        self.compileTerminal() # '='
        self.compileExpression() # expression
        self.compileTerminal() #';'
        self.compileresult.append('</letStatement>\n')
    def compileWhile(self) -> None:
        self.compileresult.append('<whileStatement>\n')
        self.compileTerminal() # 'while'
        self.compileTerminal() # '('
        self.compileExpression() # expression
        print(self.tokenlist[self.index])
        self.compileTerminal() # ')'
        self.compileTerminal() # '{'
        print("let's go")
        self.compileStatements() # statements
        self.compileTerminal() # '}'
        self.compileresult.append('</whileStatement>\n')
    def compileReturn(self) -> None:
        self.compileresult.append('<returnStatement>\n')
        self.compileTerminal() # 'return'
        if not ";" in self.tokenlist[self.index]:
            self.compileExpression() # expression
        self.compileTerminal() #';'
        self.compileresult.append('</returnStatement>\n')
    def compileIf(self) -> None:
        self.compileresult.append('<ifStatement>\n')
        self.compileTerminal() # 'if'
        self.compileTerminal() # '('
        self.compileExpression() # expression
        self.compileTerminal() # ')'
        self.compileTerminal() # '{'
        self.compileStatements() # statements
        self.compileTerminal() # '}'
        if "else" in self.tokenlist[self.index]:
            self.compileTerminal() # 'else'
            self.compileTerminal() # '{'
            self.compileStatements() # statements
            self.compileTerminal() # '}'
        self.compileresult.append('</ifStatement>\n')
    def compileExpression(self) -> None:
        self.compileresult.append('<expression>\n')
        self.compileTerm() # term
        while self.tokenlist[self.index].split()[1] in Symbol.op:
            self.compileTerminal() # op
            self.compileTerm() # term
        self.compileresult.append('</expression>\n')
    def compileTerm(self) -> None:
        self.compileresult.append('<term>\n')
        if not "identifier" in self.tokenlist[self.index]:
            if '(' in self.tokenlist[self.index]:
                self.compileTerminal() # '('
                self.compileExpression() # expression
                self.compileTerminal() # ')'
            elif self.tokenlist[self.index].split()[1] in Symbol.unaryOp:
                self.compileTerminal() # unaryOp
                self.compileTerm() # term
            else:
                self.compileTerminal()
        else:
            if "[" in self.tokenlist[self.index + 1]: #配列宣言
                self.compileTerminal() # varName
                self.compileTerminal() # '['
                self.compileExpression() # expression
                self.compileTerminal() # ']'
            elif "(" in self.tokenlist[self.index + 1]: #subroutineCall
                self.compileTerminal() # 'subroutineName
                self.compileTerminal() # '('
                self.compileExpressionList() # expressionList
                self.compileTerminal() # ')' 
            elif "." in self.tokenlist[self.index + 1]:
                self.compileTerminal() # (className | varName)
                self.compileTerminal() # '.'
                self.compileTerminal() # 'subroutineName
                self.compileTerminal() # '('
                self.compileExpressionList() # expressionList
                self.compileTerminal() # ')' 
            else:
                self.compileTerminal() # 変数
        self.compileresult.append('</term>\n')
    def compileExpressionList(self) -> None:
        self.compileresult.append('<expressionList>\n')
        if not ")" in self.tokenlist[self.index]:
            self.compileExpression() # expression
            while not ")" in self.tokenlist[self.index]:
                self.compileTerminal() # ','
                self.compileExpression() # expression
        self.compileresult.append('</expressionList>\n')
    def compileTerminal(self) -> None:
        if not self.tokenlist[self.index].split()[0][1:-1] in {"keyword","symbol","integerConstant","stringConstant","identifier"}:
            print(self.tokenlist[self.index].split()[0][1:-1])
            sys.exit("error")
        print(self.tokenlist[self.index])
        self.compileresult.append(self.tokenlist[self.index])
        self.index += 1
    def output_write(self) -> None:
        for towrite in self.compileresult:
            self.output_stream.write(towrite)
if __name__ == "__main__":
    args = sys.argv
    token = JackAnalyzer(args[1],args[1])
    token.show_tokenlist()
    token.compile()