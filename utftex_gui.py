
import sys, traceback  # traceback used for handling exceptions
import datetime
import os
import subprocess
import time

import PySide6
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QFontDialog)
from PySide6 .QtWidgets import QMessageBox as qmb
from PySide6.QtUiTools import loadUiType

app = None

from enum import Enum

class enumComment(Enum):
    NoComment   = 1
    Python = 2
    Matlab = 3


class UTFTexGui(QMainWindow, loadUiType('utftexgui.ui')[0]):
    def __init__(self):

        super().__init__()
        self.setupUi(self)

        self.bgrpComment.setId(self.rdbNoComment, enumComment.NoComment.value)
        self.bgrpComment.setId(self.rdbPython, enumComment.Python.value)
        self.bgrpComment.setId(self.rdbMatlab, enumComment.Matlab.value)
                
        self.setTitle()


    def setTitle(self):
        print('cwd  ', os.getcwd())
        fullpath = os.path.join(os.getcwd(), 'utftex_gui.exe')

        # ~ major,minor,subminor,revision=filever.get_version_number(fullpath)
        major,minor,subminor,revision=0,0,0,0
        tstring = 'UTFTeX Gui %d.%d.%d' % (major, minor, subminor)
        self.setWindowTitle(tstring)


    def closeEvent(self, *args, **kwargs):

        print('closing now')



    @Slot()
    def on_btnGenerate_clicked(self):
        import subprocess
        
        cmd = self.txtInput.toPlainText()
        # ~ print(cmd)
        # ~ print(repr(cmd))
        
        result = subprocess.run(['utftex.exe', cmd], 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        output = output.replace('\r', '')
        self.output = output
        
        self.on_bgrpComment_idClicked(self.bgrpComment.checkedId())
        
        # ~ print(repr(output))
  
    @Slot(int)
    def on_bgrpComment_idClicked(self, b_id):
        # print(f'clicked {b_id}')
        
        output = self.output
        output = output.split('\n')
        
        # look at first character in output. if it has a comment character
        # that means we must strip comment characters from output before starting
        if self.output[0] in ['#', '%']:
            for i, line in enumerate(output):
                output[i] = line[4:]
        
        # need to modify output for comments
        if b_id == enumComment.NoComment.value:
            pass
        else:
            # Python or Matlab
            if b_id == enumComment.Python.value:
                prefix = '##  '
            elif b_id == enumComment.Matlab.value:
                prefix = '%%  '
            
            for i, line in enumerate(output):
                output[i] = prefix + line
        
        
        output = '\n'.join(output)
            
        self.output = output
        self.txtOutput.setPlainText(output)

    @Slot()
    def on_btnFont_clicked(self):
        
        # using Consolas as a default font. This is a good choice for Windows,
        # but not all Linux systems will have Consolas. 
        # Maybe for Linux, Deja Vu Sans Mono is better?
        default = QFont('Consolas', 12) 
        
        # note: for PyQt6 "ok, font" should be changed to "font, ok"
        ok, font = QFontDialog.getFont(default, self, '',
                       QFontDialog.FontDialogOption.MonospacedFonts)

        if ok:
            self.txtInput.setFont(font)
            self.txtOutput.setFont(font)

    @Slot()
    def on_btnHelp_clicked(self):
        
        # help text is largely adapted from AsciiTeX help text.
        
        helpText = """
HELP - DESCRIPTION OF UTFTeX SYNTAX

       \\frac{a}{b}
       A fraction of a and b.
       
       \\alpha  \\beta
       Greek letters alpha and beta
       
       \\vec x
       vector x. x with a right arrow on top

       a^{b}
       A superscript. One can also omit the braces. In this  case  the first
       character following ^ will be superscripted.

       a_{b}
       A  subscript.  Works  just  like the superscript (well, not exactly of
       course).

       \sqrt[n]{a}
       A n-th root of a, the argument [n] is optional. Without it it  produces
       the square root of a.

       \sum
       Expands to a sigma

       \prod
       Expands to the product mark (pi).

       \int
       Expands to the integral mark.

       \oint
       A closed path integral.

       \left( , \\right)
       Expands to braces which adept to the height of their content. Available
       left braces are: ([{| The correspondingright  braces  are:  )]}|  All
       brace  types can be opened by \left.  or closed by \\right.  , producing
       a single right or left brace, respectively.

       \leadsto
       Expands to an arrow (~>), May look ugly depending on your fonts.

       \\to
       Expands to an arrow (->).

       \overline{X}
       Draws a line above expression X

       \\underline{X}
       Draws a line under expression X

       \lceil
       Left ceiling symbol

       \\rceil
       Right ceiling symbol

       \lfloor
       Left floor symbol

       \\rfloor
       Right floor symbol

       \\\\
       Insert a line break.

       \\begin{array}[pos]{column alignments}
          a00 & a01 & ... a0n \\\\
          a10 & a11 & ... a1n \\\\
          ... & ... & ... ... \\\\
          am0 & am1 & ... amn
       \end{array}
       Makes an array. The optional argument pos sets  the  alignment  of  the
       array  to t(op), b(ottom) or c(enter). The column alignments consist of
       one character per column, l(eft), c(enter), or r(ight). Currently asci-
       iTeX  does  notsupport vertical or horizontal lines, e.g. the column-
       alignment specification "{|c|}" will lead to  errors.  Note,  that  the
       string  \\begin{array}  must  not contain spaces. Cells of the array may
       contain formulas and sub-arrays.

       \\a
       Escapes the character a. Useful for inserting characters like ^, and  _
       in your equation.

EXAMPLES
       You can copy and paste some of these examples in the equation input 
       field and hit generate to see what it does.

\\frac{1}{1+x}

\lfloor x \\rfloor = x -\\frac{1}{2} + \sum_{k=1}^{\infty}
\\frac{sin(2 Pi k x)}{pi k}

\\begin{array}{ccc}
x_{11} & x_{12} & x_{13}\\\\
x_{21} & x_{22} & x_{23}\\\\
x_{31} & x_{32} & x_{33}
\end{array}

\left[
\\begin{array}{ccc}
x_{11} & x_{12} & x_{13}\\\\
x_{21} & x_{22} & x_{23}\\\\
x_{31} & x_{32} & x_{33}
\end{array}
\\right]

\int_0^W \\frac{np}{n+p}dx = \int_0^W \\frac{n_0}{exp \left( 
\\frac{E_0(x-x_0)}{kT} \\right)+exp \left( -\\frac{E_0(x-x_0)}{kT}\\right)}
dx=\\frac{n_0kT}{E_0} \left[ arctan \left( exp 
\left[\\frac{E_0(x-x_0)}{kT}\\right]\\right)\\right]^{x=W}_{x=0}~ 
\\frac{n_0kT}{E_0} pi

f(x) = \left{\\begin{array}{lr} 
\\frac{1}{x+1} +12 & \-12<x<0\\\\
 & \\ 13-x & x<\-12, x>0
\end{array}\\right.

a = \\frac{1}{\sqrt{2} + 
\\frac{1}{\sqrt{2} + 
\\frac{1}{\sqrt{2} + 
\\frac{1}{\sqrt{2} + ...
}}}}


"""
        self.txtOutput.setPlainText(helpText)



    def about(self):
        qmb.about(self, "About UTFTexGui",
                ''' UTFTexGui was written by the great Bill Eaton,
                    an engineer without compare''')

def main():
    global app

    app = QApplication(sys.argv)  # A new instance of QApplication
    gui = UTFTexGui()             
    gui.show()                  

    sys.exit(app.exec() )                    # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
