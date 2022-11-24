from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QListWidget, QSlider, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QBrush
from pygame import mixer
import sys, os
song_index = 0


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Player")

        self.setFixedHeight(450)
        self.setFixedWidth(305)
        self.setStyleSheet('background-color:#25503d')
        self.setWindowIcon(QIcon('icon.png'))
        self.make_widget()

    def make_widget(self):
        # Previous button : <<
        btn_previous = QPushButton(self)
        btn_previous.setGeometry(30, 85, 25, 25)
        btn_previous.setIcon(QIcon("Previous_Button.png"))
        btn_previous.setStyleSheet("QPushButton { background-color : #4aa17c }"
                                   "QPushButton:pressed { background-color : #bc7d00 }")
        btn_previous.clicked.connect(self.previous_song)

        # Pause Button: II
        self.btn_pause = QPushButton(self)
        self.btn_pause.setGeometry(140, 85, 25, 25)
        self.btn_pause.setIcon(QIcon("Pause_Button.png"))
        self.btn_pause.setStyleSheet("QPushButton { background-color : #4aa17c }"
                                "QPushButton:pressed { background-color : #bc7d00}")
        self.btn_pause.setCheckable(True)
        self.btn_pause.clicked.connect(self.pause_song)

        # Stop Button:
        btn_stop = QPushButton(self)
        btn_stop.setGeometry(180, 85, 25, 25)
        btn_stop.setIcon(QIcon("Stop_Button.png"))
        btn_stop.setStyleSheet("QPushButton { background-color : #4aa17c }"
                               "QPushButton:pressed { background-color : #bc7d00}")
        btn_stop.clicked.connect(self.stop_song)

        # Next Button: >>
        btn_next = QPushButton(self)
        btn_next.setGeometry(250, 85, 25, 25)
        btn_next.setIcon(QIcon("Next_Button.png"))
        btn_next.setStyleSheet("QPushButton { background-color : #4aa17c }"
                               "QPushButton:pressed { background-color : #bc7d00 }")
        btn_next.clicked.connect(self.next_song)

        # Add Playlist Button: >> ( add a song or a playlist to be listened)
        btn_add_playlist = QPushButton(self)
        btn_add_playlist.setGeometry(60, 400, 25, 25)
        btn_add_playlist.setIcon(QIcon("Add_Button.png"))
        btn_add_playlist.setStyleSheet("QPushButton { background-color : #4aa17c }"
                                       "QPushButton:pressed { background-color : #bc7d00 }")
        btn_add_playlist.clicked.connect(self.select_songs)

        # start button: >
        btn_start = QPushButton(self)
        btn_start.setGeometry(100, 85, 25, 25)
        btn_start.setIcon(QIcon("Start_Button.png"))
        btn_start.setStyleSheet("QPushButton { background-color : #4aa17c }"
                                "QPushButton:pressed { background-color : #bc7d00 }")
        btn_start.clicked.connect(self.start_song)
        # Show List Label Button:
        self.btn_show = QPushButton("Show Song List", self)
        self.btn_show.setGeometry(75, 144, 155, 17)
        self.btn_show.setIcon(QIcon("down_arrow.png"))
        self.btn_show.setStyleSheet("QPushButton {background-color : #181818 ; color: #4aa17c;}")
        self.btn_show.setCheckable(True)
        self.btn_show.clicked.connect(self.show_song_list)

        # My list widget :
        self.list_widget = QListWidget(self)
        self.list_widget.resize(200, 220)
        self.list_widget.move(52, 160)
        self.list_widget.setStyleSheet("background-color : #4aa17c;"
                                       "border:1px solid")

        # Label to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(52, 160, 200, 220)
        pixmap = QPixmap("tiger.png")
        self.image_label.setPixmap(pixmap)

        # Label to display the song is playing
        self.text_label = QLabel("Songs list is empty", self)
        # self.text_label.setGeometry(55, 30, 195, 25)
        self.text_label.move(55, 30)
        self.text_label.setMinimumSize(195, 30)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("background-color : #4aa17c;")

        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Initialize Mixer
        mixer.init()  # Starting the mixer

        # Slider for the volume control
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setGeometry(180, 407, 75, 15)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setSingleStep(1)
        self.volume_slider.valueChanged.connect(self.value_changed)
        self.volume_slider.sliderReleased.connect(self.slider_released)

    def value_changed(self, i):
        self.music_volume = i

    def show_song_list(self):
        if self.btn_show.isChecked():
            self.image_label.setHidden(True)
        else:
            self.image_label.setHidden(False)

    def slider_released(self):
        mixer.init()
        mixer.music.set_volume(self.music_volume / 100)  # Setting the volume

    def select_songs(self):
        self.song_index = 0
        opened_file = QFileDialog.getOpenFileNames(self, 'Open file')
        (self.f_names, f_type) = opened_file
        print(self.f_names, f_type, len(self.f_names))
        for i in range(len(self.f_names)):
            list_song = self.f_names[i]
            self.list_widget.addItem(f"{i+1} {os.path.basename(list_song)}")
        self.current_song_name = f'{self.f_names[self.song_index]}'

    def start_song(self):
        self.text_label.setText(f"{os.path.basename(self.current_song_name)}")
        mixer.music.load(self.current_song_name)  # Loading the song
        mixer.music.play()  # Start playing the song

    def pause_song(self):
        if self.btn_pause.isChecked():
            if mixer.music.get_busy():
                print("Pause Song")
                mixer.music.pause()
            else:
                self.btn_pause.toggle()
        else:
                print("Restart Song")
                mixer.music.unpause()

    def previous_song(self):
        self.song_index -= 1
        print(self.song_index, len(self.f_names))
        if self.song_index >= 0:
            print("Next Song")
            self.previous_song_name = f'{self.f_names[self.song_index]}'
        else:
            self.song_index = len(self.f_names) - 1
            print("Next Song")
            self.previous_song_name = f'{self.f_names[self.song_index]}'
        self.text_label.setText(f"{os.path.basename(self.previous_song_name)}")
        mixer.init()  # Starting the mixer
        mixer.music.load(self.previous_song_name)  # Loading the song
        mixer.music.set_volume(0.7)  # Setting the volume
        mixer.music.play()  # Start playing the song

    def next_song(self):
        self.song_index += 1
        print(self.song_index, len(self.f_names))
        if self.song_index < len(self.f_names):
            print("Next Song")
            self.next_song_name = f'{self.f_names[self.song_index]}'
        else:
            self.song_index = 0
            print("Next Song")
            self.next_song_name = f'{self.f_names[self.song_index]}'
        self.text_label.setText(f"{os.path.basename(self.next_song_name)}")
        mixer.init()  # Starting the mixer
        mixer.music.load(self.next_song_name)  # Loading the song
        mixer.music.set_volume(0.7)  # Setting the volume
        mixer.music.play()  # Start playing the song

    def stop_song(self):
        print("Stop Song")
        self.image_label.setHidden(False)
        mixer.music.stop()

    def add_list_item(self):
        for i in range(len(self.f_names) - 1):
            self.listWidget.addItem(f"{self.f_names[i]}")


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
# if __name__ == '__main__':
#     main()









