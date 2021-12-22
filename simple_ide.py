
import sys
from JSON_PARSER import JsonParser
from Jlexer import lex
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QPlainTextEdit

global errCount
class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('Enter your sentence:')
        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.lbl2 = QLabel('The number of words is 0')
        self.btn1 = QPushButton('&Button1', self)
        self.btn1.setCheckable(True)
        self.btn1.toggle()
        self.btn1.clicked.connect(self.button1Function)
        self.te.textChanged.connect(self.text_changed)
        self.pte1 = QPlainTextEdit(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.te)
        vbox.addWidget(self.lbl2)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.pte1)
        vbox.addStretch()

        
        self.setLayout(vbox)
        self.setWindowTitle('QTextEdit')
        self.setGeometry(300, 300, 300, 400)
        self.show()

    def button1Function(self):
        text = self.te.toPlainText()
        processing_text =str(text)
        print(processing_text)

        try:
            tokens = lex(processing_text)
        except:
            print('Lex error 입력이 정확하지 않습니다.')
        else:
            jsonParser = JsonParser()
            jsonParser.parse(tokens)
 

    def text_changed(self):
        text = self.te.toPlainText()
        processing_text =str(text)
        self.pte1.clear()
        try:
            tokens = lex(processing_text)
        except:
            self.lbl2.setText('Invaild Token, Lexing failed')
            print('Lex error 입력이 정확하지 않습니다.')
        else:
            jsonParser = JsonParser()
            result = jsonParser.parse(tokens)
        
            if(result[0] == True):
                self.lbl2.setText('Succesfully Done parsing')
                print(1, result)
                
            elif(result[0] == False):
                error_text = "".join(result[1])
                print(2, error_text)
                self.lbl2.setText("Invailed Grammer, Paring failed!")
                self.pte1.insertPlainText(error_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
