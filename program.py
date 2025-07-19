from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
from PyQt6.QtMultimedia import *
import sys
from database import *
from PyQt6.QtCore import pyqtSignal

class MessageBox():
    def success_box(self,message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
    
    def error_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))

    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    def login(self):
        msg = MessageBox()
        email = self.email.text().strip()
        password = self.password.text().strip()

        if email =="":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        if password =="":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        user = get_user_by_email_and_password(email, password)
        if user is not None:
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
        else:
            msg.error_box("Sai email hoặc mật khẩu")

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()
    
    def show_home(self, user_id):
        self.home = Home(user_id)
        self.home.show()
        self.close()
class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)

        self.name = self.findChild(QLineEdit, "txt_name")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        self.btn_eye_cp.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_eye_cp))

    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    def register(self):
        msg = MessageBox()
        name = self.name.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if name =="":
            msg.error_box("Họ tên không được để trống")
            self.name.setFocus()
            return
        if email =="":
            msg.eror_box("Email không được để trống")
            self.email.setFocus()
            return
        if password =="":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        if confirm_password =="":
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return
        if password != confirm_password:
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
        if not self.validate_email(email):
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return
        check_email = get_user_by_email(email)
        if check_email is not None:
            msg.error_box("Email đã tồn tại")
            return
        create_user(name, email, password)
        msg.success_box("Đăng ký thành công")
        self.show_login()

    def validate_email(self, s):
        idx_at = s.find('@')
        if idx_at == -1:
            return False
        return '.' in s[idx_at+1:]

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class SongItemWidget(QWidget):
    play_song = pyqtSignal(str)
    add_song_to_playlist = pyqtSignal(str)
    remove_song_from_playlist = pyqtSignal(str)

    def __init__(self, song_id, song_name, image_path, artist_names, is_playlist_mode=False):
        super().__init__()
        uic.loadUi("ui/song.ui", self)
        
        # Store song data
        self.song_id = song_id
        self.song_name = song_name
        self.image_path = image_path
        self.artist_names = artist_names
        self.is_playlist_mode = is_playlist_mode
        
        # Find UI elements
        self.name = self.findChild(QLabel, "lbl_name")
        self.artist = self.findChild(QLabel, "lbl_artist")
        self.image = self.findChild(QLabel, "lbl_image")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_playlist = self.findChild(QPushButton, "btn_add")
        
        # Set initial values
        self.name.setText(self.song_name)
        self.artist.setText(self.artist_names)
        self.image.setPixmap(QPixmap(self.image_path.replace("/", "\\")))
        
        # Connect signals
        self.btn_play.clicked.connect(self.play)
        self.btn_playlist.clicked.connect(self.handle_playlist_action)
        
        # Set button text based on mode
        self.setup_playlist_button()
        
        # Set minimum size
        self.setMinimumSize(191, 262)
    
    def play(self):
        self.play_song.emit(str(self.song_id))

    def handle_playlist_action(self):
        if self.is_playlist_mode:
            self.remove_song_from_playlist.emit(str(self.song_id))
        else:
            self.add_song_to_playlist.emit(str(self.song_id))
    
    def setup_playlist_button(self):
        if self.is_playlist_mode:
            self.btn_playlist.setText("Remove")
            self.btn_playlist.setProperty("class", "remove")
        else:
            self.btn_playlist.setText("Add")
            self.btn_playlist.setProperty("class", "")

class PlaylistItemWidget(QWidget):
    play_song = pyqtSignal(str)
    delete_song = pyqtSignal(str)

    def __init__(self, song_id, song_name, image_path, artist_names):
        super().__init__()
        uic.loadUi("ui/playlist.ui", self)
        self.song_id = song_id
        self.song_name = song_name
        self.image_path = image_path
        self.artist_names = artist_names

        self.lbl_name = self.findChild(QLabel, "lbl_name")
        self.lbl_artist = self.findChild(QLabel, "lbl_artist")
        self.lbl_img = self.findChild(QLabel, "lbl_img")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_delete = self.findChild(QPushButton, "btn_delete")

        self.lbl_name.setText(self.song_name)
        self.lbl_artist.setText(self.artist_names)
        pixmap = QPixmap(self.image_path.replace("/", "\\"))
        if not pixmap.isNull():
            self.lbl_img.setPixmap(pixmap.scaled(self.lbl_img.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.lbl_img.setText("")

        self.btn_play.clicked.connect(self.on_play)
        self.btn_delete.clicked.connect(self.on_delete)

    def on_play(self):
        self.play_song.emit(str(self.song_id))

    def on_delete(self):
        self.delete_song.emit(str(self.song_id))

class PlaylistWidget(QWidget):
    play_song_signal = pyqtSignal(str)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.songs_container = QWidget()
        self.songs_layout = QVBoxLayout(self.songs_container)
        self.songs_layout.setSpacing(8)
        self.songs_layout.setContentsMargins(8, 8, 8, 8)
        self.songs_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.songs_container)
        self.layout.addWidget(self.scroll_area)
        self.load_songs()

    def load_songs(self):
        # Clear existing widgets
        for i in reversed(range(self.songs_layout.count())):
            widget = self.songs_layout.itemAt(i).widget()
            if widget is not None:
                self.songs_layout.removeWidget(widget)
                widget.setParent(None)
        # Get user's playlist songs
        songs = get_user_playlist_songs(self.user_id)
        for song in songs:
            item = PlaylistItemWidget(song['id'], song['name'], song['image_path'], song['artist_names'])
            item.play_song.connect(self.on_play_song)
            item.delete_song.connect(self.on_delete_song)
            self.songs_layout.addWidget(item)

    def on_play_song(self, song_id):
        self.play_song_signal.emit(song_id)

    def on_delete_song(self, song_id):
        remove_song_from_user_playlist(self.user_id, song_id)
        self.load_songs()
class Home(QMainWindow):
    play_song_signal = pyqtSignal(str)  # Add signal at class level

    def __init__(self, user_id):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        self.msg = MessageBox()

        self.user_id = user_id
        self.user = get_user_by_id(user_id)
        self.loadAccountInfo()

        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_account = self.findChild(QPushButton, "btn_nav_account")
        self.btn_nav_playlist = self.findChild(QPushButton, "btn_nav_playlist")
        self.lb_avatar = self.findChild(QLabel, "lb_avatar")

        self.btn_upload = self.findChild(QPushButton, "btn_upload")
        self.btn_save = self.findChild(QPushButton, "btn_save")
        
        self.btn_nav_home.clicked.connect(lambda: self.navMainScreen(0))
        self.btn_nav_playlist.clicked.connect(lambda: self.navMainScreen(1))
        self.btn_nav_account.clicked.connect(lambda: self.navMainScreen(2))
        self.btn_upload.clicked.connect(self.update_avatar)
        self.btn_save.clicked.connect(self.save_account_info)
        
        self.setup_audio_ui()
        self.load_initial_songs()
        
    def setup_audio_ui(self):
        # Find player control buttons
        self.btn_prev_song = self.findChild(QPushButton, 'btn_prev_song')
        self.btn_next_song = self.findChild(QPushButton, 'btn_next_song')
        
        # Connect player control buttons
        self.btn_prev_song.clicked.connect(self.previous_song)
        self.btn_next_song.clicked.connect(self.next_song)
        
        # Setup song container with scroll area
        self.btn_search = self.findChild(QPushButton, 'btn_search')
        self.txt_search = self.findChild(QLineEdit, 'txt_search')
        self.song_container = self.findChild(QWidget, 'song_container')
        
        # Setup scroll area
        self.scroll_area = QScrollArea(self.song_container)
        self.scroll_area.setWidgetResizable(True)
        
        # Create scroll content
        self.scroll_content = QWidget()
        self.song_layout = QGridLayout(self.scroll_content)
        self.song_layout.setSpacing(20)
        self.song_layout.setContentsMargins(20, 20, 20, 20)
        
        # Setup scroll area layout
        self.scroll_area.setWidget(self.scroll_content)
        scroll_layout = QVBoxLayout(self.song_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(self.scroll_area)
        
        # Setup playlist container
        self.playlist_container = self.findChild(QWidget, 'playlist_container')
        self.playlist_widget = PlaylistWidget(self.user_id)
        self.playlist_widget.play_song_signal.connect(self.play_song)  # Connect playlist signal
        playlist_layout = QVBoxLayout(self.playlist_container)
        playlist_layout.setContentsMargins(0, 0, 0, 0)
        playlist_layout.addWidget(self.playlist_widget)
        
        # Connect signals
        self.btn_search.clicked.connect(self.search_song)
        
        # Initialize media player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Initialize playlist and current index
        self.current_playlist = get_user_playlist_songs(self.user_id)
        self.current_song_index = -1
        
        # Connect player signals
        self.player.errorOccurred.connect(self.handle_player_error)
        self.player.playbackStateChanged.connect(self.mediaStateChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        
        # Initialize UI elements
        self.playBtn = self.findChild(QPushButton, "btn_play")
        self.volumeBtn = self.findChild(QPushButton, "btn_volume")
        self.volumeBar = self.findChild(QSlider, "slider_volume")
        self.durationBar = self.findChild(QSlider, "slider_duration")
        self.timeLabel = self.findChild(QLabel, "lbl_time")
        self.curr_name = self.findChild(QLabel, "lbl_curr_name")
        self.curr_img = self.findChild(QLabel, "lbl_curr_img")
        self.curr_artist = self.findChild(QLabel, "lbl_curr_artist")
        
        # Initialize icons
        try:
            self.playIcon = QIcon("img/play-solid.svg")
            self.pauseIcon = QIcon("img/pause-solid.svg")
            self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
            self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
            self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
            self.muteIcon = QIcon("img/volume-off-solid.svg")
        except:
            print("Warning: Could not load some icons")
            self.playIcon = None
            self.pauseIcon = None
            self.volumeHighIcon = None
            self.volumeLowIcon = None
            self.volumeOffIcon = None
            self.muteIcon = None
        
        # Set initial volume
        self.playBtn.setIcon(self.playIcon)
        self.playBtn.clicked.connect(self.togglePlay)
        self.volumeBtn.setIcon(self.volumeOffIcon)
        self.volumeBtn.clicked.connect(self.toggleMute)

        self.volumeBar.valueChanged.connect(self.setVolume)
        self.durationBar.sliderMoved.connect(self.setPosition)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.playbackStateChanged.connect(self.mediaStateChanged)
        self.volumeBar.setValue(50)
        self.durationBar.setValue(0)
        self.audio_output.setVolume(0.5)
        self.current_volume = 50

    def clear_song_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.setParent(None)

    def add_songs_to_layout(self, song_list, layout, columns=3, is_playlist_mode=False):
        row = 0
        col = 0
        for song in song_list:
            item = SongItemWidget(
                song['id'],
                song['name'],
                song['image_path'].replace("/", "\\"),
                song['artist_names'],
                is_playlist_mode=is_playlist_mode
            )
            item.setFixedSize(191, 262)
            item.play_song.connect(self.play_song)
            item.add_song_to_playlist.connect(self.add_to_playlist)
            item.remove_song_from_playlist.connect(self.remove_from_playlist)
            layout.addWidget(item, row, col)
            col += 1
            if col == columns:
                col = 0
                row += 1

    def load_initial_songs(self):
        self.clear_song_layout(self.song_layout)
        songs = get_first_15_songs()
        self.add_songs_to_layout(songs, self.song_layout, columns=4, is_playlist_mode=False)

    def navMainScreen(self, index):
        self.main_widget.setCurrentIndex(index)

    def loadAccountInfo(self):
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
        self.txt_dob = self.findChild(QDateEdit, "txt_dob")
        self.txt_dob.setDisplayFormat("dd-MM-yyyy")
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_dob.setDate(QDate.fromString(self.user["birthday"], "dd-MM-yyyy"))
        
        if self.user["avatar"]:
            self.lb_avatar.setPixmap(QPixmap(self.user["avatar"]))
        
        if not self.user["gender"]:
            self.txt_gender.setCurrentIndex(0)
        elif self.user["gender"] == "Male":
            self.txt_gender.setCurrentIndex(1)
        elif self.user["gender"] == "Female":
            self.txt_gender.setCurrentIndex(2)
        else:
            self.txt_gender.setCurrentIndex(3)

    def add_to_playlist(self, song_id):
        try:
            # Check if song is already in playlist
            if is_song_in_user_playlist(self.user_id, song_id):
                self.msg.error_box("This song is already in your playlist")
                return
                
            # Add song to playlist
            add_song_to_user_playlist(self.user_id, song_id)
            
            # Update current playlist
            self.current_playlist = get_user_playlist_songs(self.user_id)
            
            # Always refresh playlist widget to keep it in sync
            self.playlist_widget.load_songs()
            
            # Show success message
            self.msg.success_box("Song added to playlist successfully")
            
        except Exception as e:
            print(f"Error adding song to playlist: {e}")
            self.msg.error_box("Failed to add song to playlist")

    def remove_from_playlist(self, song_id):
        try:
            # Remove song from playlist
            remove_song_from_user_playlist(self.user_id, song_id)
            
            # Update current playlist
            self.current_playlist = get_user_playlist_songs(self.user_id)
            
            # Always refresh playlist widget to keep it in sync
            self.playlist_widget.load_songs()
            
            # Show success message
            self.msg.success_box("Song removed from playlist successfully")
            
        except Exception as e:
            print(f"Error removing song from playlist: {e}")
            self.msg.error_box("Failed to remove song from playlist")

    def update_song_item_state(self, song_id, is_in_playlist):
        # Find and update the song item in the current view
        for i in range(self.song_layout.count()):
            item = self.song_layout.itemAt(i).widget()
            if isinstance(item, SongItemWidget) and str(item.song_id) == str(song_id):
                item.is_playlist_mode = is_in_playlist
                item.setup_playlist_button()
                break
    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self, "Select Image","", "Image Files(*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.lb_avatar.setPixmap(QPixmap(file))
            update_user_avatar(self.user_id, file)

    def save_account_info(self):
        name = self.txt_name.text().strip()
        dob = self.txt_dob.date().toString("dd-MM-yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.user_id, name, gender, dob)
        self.msg.success_box("Cập nhật thông tin thành công")
        
    def render_song_list(self, song_list:list):
        self.clear_song_layout(self.song_layout)
        self.add_songs_to_layout(song_list, self.song_layout, columns=3, is_playlist_mode=False)
        
    def search_song(self):
        name = self.txt_search.text()
        song_list = get_songs_by_name(name)
        self.render_song_list(song_list)
        
    def play_song(self, song_id):
        # Always refresh the playlist when playing a song
        self.current_playlist = get_user_playlist_songs(self.user_id)
        
        # Find the song in the current playlist
        self.current_song_index = -1  # Reset index
        for i, song in enumerate(self.current_playlist):
            if str(song['id']) == str(song_id):
                self.current_song_index = i
                break
        
        self.current_song = song_id
        song = get_song_by_id(song_id)
        file_path = QUrl.fromLocalFile(song["file_path"].replace("/", "\\"))
        self.player.setSource(file_path)
        self.player.play()
        
        if self.playBtn and self.pauseIcon:
            self.playBtn.setIcon(self.pauseIcon)
        elif self.playBtn:
            self.playBtn.setText("Pause")
        
        self.curr_name.setText(f"Now playing: {song['name']}")
        self.curr_img.setPixmap(QPixmap(song["image_path"].replace("/", "\\")))
        self.curr_artist.setText(f"Artist: {song['artist_names']}")
        
    def handle_player_error(self, error, error_string):
        print(f"Media player error: {error} - {error_string}")
        
    def mediaStateChanged(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        # Convert position and duration from milliseconds to hh:mm:ss format
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.player.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self, duration):
        self.durationBar.setRange(0, duration)
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.player.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def setPosition(self, position):
        if self.player.duration() > 0:  # Only set position if media is loaded
            self.player.setPosition(position)
        
    def setVolume(self, volume):
        # Convert the slider value to a float between 0.0 and 1.0
        volume = volume / 100.0
        self.audio_output.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audio_output.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audio_output.setMuted(False)
    
    def toggleMute(self):
        if self.audio_output.isMuted():
            self.audio_output.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audio_output.setMuted(True)
            self.volumeBtn.setIcon(self.muteIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def togglePlay(self):
        print("tessttttt")
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.playBtn.setIcon(self.playIcon)
        else:
            self.player.play()
            self.playBtn.setIcon(self.pauseIcon)

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def next_song(self):
        if not self.current_playlist:
            self.msg.error_box("No playlist is currently loaded")
            return
            
        if self.current_song_index < len(self.current_playlist) - 1:
            next_song = self.current_playlist[self.current_song_index + 1]
            self.play_song(next_song['id'])
        else:
            # Loop back to the start of the playlist
            first_song = self.current_playlist[0]
            self.play_song(first_song['id'])

    def previous_song(self):
        if not self.current_playlist:
            self.msg.error_box("No playlist is currently loaded")
            return
            
        if self.current_song_index > 0:
            prev_song = self.current_playlist[self.current_song_index - 1]
            self.play_song(prev_song['id'])
        else:
            # Go to the last song in the playlist
            last_song = self.current_playlist[-1]
            self.play_song(last_song['id'])

if __name__ == "__main__":
    app = QApplication([])
    login = Login()
    login = Home(1)
    login.show()
    app.exec()