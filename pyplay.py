import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl

# other plugins installed
# sudo apt-get install libqt5multimedia5-plugins
# below command for installing QtMultimedia
# sudo apt-get install python3-PyQt5.QtMultimedia


STATIC_FOLDER = './material'

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyPlay')
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon(STATIC_FOLDER + '/play.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.gray)
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        '''Create Media player object'''
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videiowidget object
        videowidget = QVideoWidget()

        # create open button
        openBtn = QPushButton('Select Video')
        openBtn.clicked.connect(self.open_file)

        # create button for paying
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # create horizontal box layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        # set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        # create vertical box layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

        # media player signals (listeners)
        self.mediaPlayer.stateChanged.connect(self.mediastate_change)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    
    def open_file(self):
        '''Open the file functionality'''
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Video')

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)


    def play_video(self):
        '''Pause or play the video'''
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()


    def mediastate_change(self, state):
        '''Switch pause to play and play to pause button'''
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def position_changed(self, position):
        '''video slider functionality'''
        self.slider.setValue(position)

    
    def duration_changed(self, duration):
        '''calcurate duration elapsed to show on slider'''
        self.slider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    
    def handle_errors(self):
        self.playBtn.setEnable(False)
        self.label.setText(f"Error: {self.mediaPlayer.errorString()}")






app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())