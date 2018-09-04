import os,sys, math
import nuke

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

#Projekt Variabler

class LogoWidget(QWidget):
    def __init__(self, parent=None, mainDiameter=138, outerRingWidth=10,my_Knob="None"):
        QWidget.__init__(self, parent)

        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("QMovie to show animated gif")
        
        # set up the movie screen on a label
        self.movie_screen = QLabel()
        # expand and center the label 
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, 
            QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(Qt.AlignCenter)        
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout) 

        ag_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),"grapichs/h_gifwriterUI.gif")
        self.movie = QMovie(ag_file, QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        # optionally display first frame
        self.movie.start()

class Example(QWidget):
    def __init__(self, parent=None,myNode="none"):
        QWidget.__init__(self, None)
        self.Lift = LogoWidget()

        layout = QGridLayout()
        layout.addWidget(self.Lift,0,0)
        layout.setRowStretch(1,1)
        self.setLayout(layout)

class LogoKnob():
    def __init__( self ):
        self.instance = 0
        return None

    def makeUI( self ):
        self.instance = Example()
        return self.instance

