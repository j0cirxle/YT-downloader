import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit,QListWidget
from PyQt5.QtCore import QThread, pyqtSignal
from pytubefix import YouTube
import yt_dlp
from tkinter import *
import tkinter.messagebox as msgbox

songs = []
end = 0

class DownloadWorker(QThread):
    log_signal = pyqtSignal(str)
    log_signal1 = pyqtSignal(str)

    def __init__(self, songs, location):
        super().__init__()
        self.songs = songs
        self.location = location

    def run(self):
        for song in self.songs:
            self.log_signal.emit(f"🔍 Searching for: {song}")
            url = self.get_top_video_url(song)
            if url:
                self.log_signal.emit(f"✅ Found: {url}")
                self.download_youtube_video_mp4(url, self.location)
            else:
                self.log_signal.emit(f"❌ No result found for: {song}")
                msgbox.showerror(f"i can't found",f'❌ No result found for: {song}')
        self.log_signal1.emit(f"✅Download Ended")
    def get_top_video_url(self, query):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'default_search': 'ytsearch1',
            'extract_flat': 'in_playlist',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(query, download=False)
                if 'entries' in result and result['entries']:
                    video = result['entries'][0]
                    return f"https://www.youtube.com/watch?v={video['id']}"
        except Exception as e:
            self.log_signal.emit(f"❌ Error while searching: {str(e)}")
            msgbox.showerror(f"{str(e)}",'❌ Error while searching')
        return None

    def download_youtube_video_mp4(self, video_url, output_path, file_extension='mp4'):
        try:
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True, file_extension=file_extension).order_by('resolution').asc().first()
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            stream.download(output_path)
            self.log_signal.emit(f"📥 Download complete: {yt.title}")
        except Exception as e:
            self.log_signal.emit(f"❌ Download error: {str(e)}")
            msgbox.showerror(f"checking your WIFI status",f'❌ Download error: {str(e)}')


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Songs Downloader")
        self.setGeometry(100, 100, 400, 250)

        self.label = QLabel("YouTube Songs Downloader", self)
        self.log_label = QLabel("Logs will appear here", self)

        self.song_input = QLineEdit(self)
        self.song_input.setPlaceholderText("Enter song title")

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Enter download path (e.g. C:/Users/user/Downloads)")

        self.add_button = QPushButton("Add to list", self)
        self.add_button.clicked.connect(self.add_song)

        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.start_download)

        self.list_widget = QListWidget(self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.song_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.path_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_label)
        self.setLayout(layout)

    def add_song(self):
        song = self.song_input.text()
        if song:
            songs.append(song)
            self.label.setText(f"Added: {song}")
            self.list_widget.addItem(song)
            print(f"Current songs list: {songs}")
        else:
            self.label.setText("❗ Please enter a song title")

    def start_download(self):
        path = self.path_input.text()
        if not path:
            self.label.setText("❗ Please enter a download path")
            msgbox.showwarning("Where is a download path?",'❗ Please enter a download path')
            return
        if len(songs) == 0:
            msgbox.showwarning("Where is a song_list",'❗ Please enter a song_list')
            return

        self.label.setText("⬇️ Starting download...")
        self.worker = DownloadWorker(songs, path)
        self.worker.log_signal.connect(self.update_log)
        self.worker.log_signal1.connect(self.update_log1)
        self.worker.start()

    def update_log(self, message):
        self.log_label.setText(message)
        print(message)
    def update_log1(self, message):
        self.label.setText(message)
        print(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
