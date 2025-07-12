from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
from database import *

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
class Item(Widget):
    def __init__(self):
        self.bt_start = self.findChild(QPushButton,'bt_start')
        self.bt_like = self.findChild(QPushButton,'bt_like')
        self.lb_pic = self.findChild(QLabel,'lb_pic')
        self.lb_songname = self.findChild(QLabel, 'lb_songname')
        self.lb_athname = self.findChild(QLabel, 'lb_athname')     
class Home(QMainWindow):
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
        # clear the grid layout
        for i in reversed(range(self.song_layout.count())):
            widgetToRemove = self.song_layout.itemAt(i).widget()
            self.song_layout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for song in song_list:
            # Create widget in song list mode (Add button only)
            itemWidget = SongItemWidget(song["id"], song["name"], song["image_path"].replace("/", "\\"), song["artist_names"], is_playlist_mode=False)
            itemWidget.setFixedSize(400, 80)  # Set fixed size for each item
            itemWidget.play_song.connect(self.play_song)
            itemWidget.add_song_to_playlist.connect(self.add_to_playlist)
            self.song_layout.addWidget(itemWidget, row, column)
            column += 1
            if column == 2:  # Show 2 columns
                column = 0
                row += 1
        
    def search_song(self):
        name = self.txt_search.text()
        song_list = database.get_songs_by_name(name)
        self.render_song_list(song_list)
        
    def play_song(self, song_id):
        # Always refresh the playlist when playing a song
        self.current_playlist = database.get_user_playlist_songs(self.user_id)
        
        # Find the song in the current playlist
        self.current_song_index = -1  # Reset index
        for i, song in enumerate(self.current_playlist):
            if str(song['id']) == str(song_id):
                self.current_song_index = i
                break
        
        self.current_song = song_id
        song = database.get_song_by_id(song_id)
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
            msg = Alert()
            msg.error_message("No playlist is currently loaded")
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
            msg = Alert()
            msg.error_message("No playlist is currently loaded")
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