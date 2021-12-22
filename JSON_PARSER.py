from Jlexer import lex
import sys

class JsonParser:
    def __init__(self):
        self.errCount = 0
        self.stack = list()
        self.stack.append(0)
        self.inputs = list()
        self.errorStack = list()
 
        self.parsingTable = [
            {'{' : ['S', 5], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['S', 4], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['acc', 0], 'S': ['G', 1], 'O': ['G', 3], 'M': [], 'P': [], 'A': ['G', 2], 'E': [], 'V': [] } # 0
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['acc', 0], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 1], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['E',  4], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] } #3
            ,    {'{' : ['S',  5], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['S',  9], ':': ['E', 14], '[': ['S',  4], ']': ['S',  6], 'number': ['S', 10], 'True': ['S', 13], 'False': ['S', 14], 'null': ['S', 15], '$': ['E', 2], 'S': [], 'O': ['G', 11], 'M': [], 'P': [], 'A': ['G', 12], 'E': ['G', 7], 'V': ['G', 8] } # 4
            ,    {'{' : ['E', 14], '}' : ['S', 16] , ',' : ['E', 14], 'string': ['S', 19], ':': ['E', 14], '[': ['E', 14], ']': ['E',  3], 'number': ['E', 11], 'True': ['E', 11], 'False': ['E', 11], 'null': ['E', 11], '$': ['E', 3], 'S': [], 'O': [], 'M': ['G', 17], 'P': ['G', 18], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R',  8] , ',' : ['R',  8], 'string': ['E',  1], ':': ['E', 14], '[': ['E', 14], ']': ['R',  8], 'number': ['E',  1], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 8], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['S', 20], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['S', 21], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 10], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R', 12] , ',' : ['R', 12], 'string': ['E',  1], ':': ['E', 14], '[': ['E', 14], ']': ['R', 12], 'number': ['E',  1], 'True': ['E', 11], 'False': ['E', 11], 'null': ['E', 11], '$': ['E', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] } # 9
            ,    {'{' : ['E', 14], '}' : ['R', 13] , ',' : ['R', 13], 'string': ['E',  1], ':': ['E', 14], '[': ['E',  1], ']': ['R', 13], 'number': ['E',  1], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R', 14] , ',' : ['R', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R', 15] , ',' : ['R', 15], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 15], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 2], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R', 16] , ',' : ['R', 16], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 16], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R', 17] , ',' : ['R', 17], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 17], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E' ,3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] } # 14
            ,    {'{' : ['E', 14], '}' : ['R', 18] , ',' : ['R', 18], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 18], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R',  3] , ',' : ['R',  3], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['S', 22] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': [], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R',  5] , ',' : ['S', 23], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 3], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 10], '}' : ['E', 12] , ',' : ['E', 14], 'string': ['E', 10], ':': ['S', 24], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['E', 13], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] } # 19
            ,    {'{' : ['E', 14], '}' : ['R',  9] , ',' : ['R',  9], 'string': ['E',  1], ':': ['E', 14], '[': ['E', 14], ']': ['R',  9], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 9], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['S',  5], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['S',  9], ':': ['E', 14], '[': ['S',  4], ']': ['E',  7], 'number': ['S', 10], 'True': ['S', 13], 'False': ['S', 14], 'null': ['S', 15], '$': ['E', 7], 'S': [], 'O': ['G', 11], 'M': [], 'P': [], 'A': ['G',12], 'E': ['G', 25], 'V': ['G', 8] }
            ,    {'{' : ['E',  1], '}' : ['R',  4] , ',' : ['R',  4], 'string': ['E',  1], ':': ['E', 14], '[': ['E', 14], ']': ['R',  4], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': ['R', 4], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E',  9], '}' : ['E',  7] , ',' : ['E',  8], 'string': ['S', 19], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 11], 'True': ['E', 11], 'False': ['E', 11], 'null': ['E', 11], '$': ['E', 7], 'S': [], 'O': [], 'M': ['G', 26], 'P': ['G', 18], 'A': [], 'E': [], 'V': [] } # 23
            ,    {'{' : ['S',  5], '}' : ['E',  6] , ',' : ['E', 14], 'string': ['S',  9], ':': ['E', 14], '[': ['S',  4], ']': ['E', 14], 'number': ['S', 10], 'True': ['S', 13], 'False': ['S', 14], 'null': ['S', 15], '$': ['E', 6], 'S': [], 'O': ['G', 11], 'M': [], 'P': [], 'A': ['G', 12], 'E': [], 'V': ['G', 27] } # 24
            ,    {'{' : ['E', 14], '}' : ['E', 14] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['R', 11], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': [], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R',  6] , ',' : ['E', 14], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E', 14], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': [], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] }
            ,    {'{' : ['E', 14], '}' : ['R',  7] , ',' : ['R',  7], 'string': ['E', 14], ':': ['E', 14], '[': ['E', 14], ']': ['E',  3], 'number': ['E', 14], 'True': ['E', 14], 'False': ['E', 14], 'null': ['E', 14], '$': [], 'S': [], 'O': [], 'M': [], 'P': [], 'A': [], 'E': [], 'V': [] } # 27
            ]
        

    def shift(self, num) :
        sym = self.inputs[0]
        self.stack.append(sym)
        self.inputs.pop(0)
        self.stack.append(num)

    def goto(self, num) :
        self.stack.append(num)

    def reduction(self, num) :
        if num == 1 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("S")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 2 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("S")
            self. ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 3 :
            for i in range(0, 4) :
                self.stack.pop()
            self.stack.append("O")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 4 :
            for i in range(0, 6) :
                self.stack.pop()
            self.stack.append("O")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 5 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("M")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 6 :
            for i in range(0, 6) :
                self.stack.pop()
            self.stack.append("M")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 7 :
            for i in range(0, 6) :
                self.stack.pop()
            self.stack.append("P")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 8 :
            for i in range(0, 4) :
                self.stack.pop()
            self.stack.append("A")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 9 :
            for i in range(0, 6) :
                self.stack.pop()
            self.stack.append("A")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 10 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("E")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 11 :
            for i in range(0, 6) :
                self.stack.pop()
            self.stack.append("E")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 12 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 13 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 14 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 15 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 16 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 17 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1]) 
        if num == 18 :
            for i in range(0, 2) :
                self.stack.pop()
            self.stack.append("V")
            self.ParsingProduct(self.stack[len(self.stack)-2], self.stack[-1])

    global LB_Trigger

    def error(self, num) :
        
        self.parseResult = False
        if num == 1 :
            error_message = str("Error : Comma between pairs/objects expected!\n")
            self.errorStack.append(error_message)
            self.inputs.insert(0, ',')
            self.errCount = self.errCount + 1
        if num == 2 :
            error_message = str("Error : Right Square Bracket Expected!\n" )
            self.errorStack.append(error_message)
            self.inputs.insert(0, ']')
            self.errCount = self.errCount + 1
        if num == 3 :
            error_message = str("Error : Right Curl Bracket Expected!\n")
            self.errorStack.append(error_message)
            self.inputs.insert(0, '}')
            self.errCount = self.errCount + 1
        if num == 4 :
            LB_Trigger = 1
            error_message = str("Error : Not Array Format, but more than one Object exist. May lead Left Square Bracket Missing error.\n")
            self.errorStack.append(error_message)
            self.inputs.pop(0)
            self.stack.pop()
            self.stack.append(0)
            self.errCount = self.errCount + 1
        if num == 5 :
            self.inputs.pop(0)
            self.reduction(2)
            error_message = str("Error : Left Square Bracket Expected!\n")
            self.errorStack.append(error_message)
            self.errCount = self.errCount + 1
        if num == 6 :
            error_message = str("Error : value Next to Colon Expected!\n")
            self.errorStack.append(error_message)
            self.inputs.insert(0, 'string')
            self.errCount = self.errCount + 1
        if num == 7 :
            error_message = str("Error : Unexpected Comma / Missing elements exists!\n")
            self.errorStack.append(error_message)
            self.stack.pop()
            self.stack.pop()
            self.errCount = self.errCount + 1
        if num == 8 :
            self.inputs.pop(0)
            error_message = str("Error : Unexpected Comma / Missing elements exists!\n")
            self.errorStack.append(error_message)
            self.errCount = self.errCount + 1
        if num == 9 :
            error_message = str("Error : Unexpected Right Curl Bracket!\n")
            self.errorStack.append(error_message)
            self.stack.pop()
            self.stack.pop()
            self.inputs.insert(0, ',')
            self.inputs.insert(0, '}')
            self.errCount = self.errCount + 1
        if num == 10 :
            error_message = str("Error : Colon between pairs expected!\n")
            self.errorStack.append(error_message)
            self.inputs.insert(0, ':')
            self.errCount = self.errCount + 1
        if num == 11 :
            error_message = str("Error : Non-string key not allowed!\n")
            self.errorStack.append(error_message)
            self.inputs[0] = 'string'
            self.errCount = self.errCount + 1
        if num == 12 :
            error_message = str("Error : Invalid 'key:value' format!\n")
            self.errorStack.append(error_message)
            for i in range(0, 4) :
                self.stack.pop()
                self.errCount = self.errCount + 1
        if num == 13 :
            error_message = str("Error : Invalid form Exists.\n")
            self.errorStack.append(error_message)
            self.inputs.pop(0)
            self.errCount = self.errCount + 1
        if num == 14 :
            error_message = "Error : Unexpected token :" + str(self.inputs.pop(0)) + "\n"
            self.errorStack.append(error_message)
            self.errCount = self.errCount + 1
            
    def ParsingProduct(self, state, token) :
        self.parsingTable[state][token]
        if self.parsingTable[state][token][0] == "S" :
            self.shift(self.parsingTable[state][token][1])
        elif self.parsingTable[state][token][0] == "R" :
            self.reduction(self.parsingTable[state][token][1])
        elif self.parsingTable[state][token][0] == "acc" :
         
            print("Parsing End!\n")
            self.inputs.pop()
        elif self.parsingTable[state][token][0] == "G" :
            self.goto(self.parsingTable[state][token][1])
        else :
         
            self.error(self.parsingTable[state][token][1])

    def parse(self, tokens) :
        
        for i in range(0, len(tokens)) :
            self.inputs.append(tokens[i])
        #print(inputs)
        self.Do_Parse()
        if(len(self.errorStack) == 0):
            result_bool = True
            return [result_bool, []]
        else:
            print("====")
            result_bool = False
            return [result_bool, self.errorStack]

    def Do_Parse(self) :
        CharNum = 1
        while(len(self.inputs) > 0) :
            #print("Trial" ,CharNum, "\n", stack ,"\n", inputs ,"\n\n")
            self.ParsingProduct(self.stack[-1], self.inputs[0])

        

if __name__== '__main__' :
   
    errCount = 0
    lines = []
    jsonParser = JsonParser()
    print("Input you JSON format file.\n=====================================\n")
    while True:
        line = input()
        if line:
            lines.append(line)
        
        else:
            break
    JsonSentence = '\n'.join(lines)
    print("\n=====================================\n")
    try:
        tokens = lex(JsonSentence)
    except:
        print('Lex error 입력이 정확하지 않습니다.')
    else:
        jsonParser.parse(tokens)

    if errCount == 0 :
        print("Parsing Finished without any ERROR. Correct Format!\n")
    else :
        print("Parsing Finished with", errCount, "ERRORs.\n")
