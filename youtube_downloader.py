import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QListWidget
from PyQt5.QtCore import QThread, pyqtSignal
from pytubefix import YouTube
import yt_dlp
from tkinter import messagebox as msgbox
from datetime import datetime

songs = []

class DownloadWorker(QThread):
    log_signal = pyqtSignal(str)
    log_signal1 = pyqtSignal(str)

    def __init__(self, songs, location, option_qual):
        super().__init__()
        self.songs = songs
        self.location = location
        self.option_qual = option_qual
        self.log_number = 0

    def run(self):
        for song in self.songs:
            self.log("🔍 Searching for: " + song)
            url = self.get_top_video_url(song)
            if url:
                self.log(f"✅ Found: {url}")
                self.download_youtube_video_mp4(url, self.location)
            else:
                self.log(f"Wrong-title(err-code:003): ❌ No result found for: {song}")
        self.log(f"✅ Download Ended", end=True)

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
            msgbox.showerror(f"Unexpected-err(err-code:002)",f"❌ Error while searching: {str(e)}")
        return None

    def download_youtube_video_mp4(self, video_url, output_path, file_extension='mp4'):
        try:
            yt = YouTube(video_url)
            if self.option_qual == "low":
                stream = yt.streams.filter(progressive=True, file_extension=file_extension).order_by('resolution').asc().first()
            elif self.option_qual == "high":
                stream = yt.streams.filter(progressive=True, file_extension=file_extension).order_by('resolution').desc().first()
            else:
                msgbox.showerror("Missing Option(err-code:001)", "❗ Please select a picture quality option (low/high)")
                return
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            stream.download(output_path)
            self.log(f"📥 Download complete: {yt.title}")
        except Exception as e:
            msgbox.showerror(f"Unexpected(err-code:002)", f"❌ Download error: {str(e)}")

    def log(self, message, end=False):
        self.log_signal.emit(f"[{self.log_number}] {message}")
        self.log_number += 1
        if end:
            self.log_signal1.emit(message)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Songs Downloader")
        self.setGeometry(100, 100, 400, 250)

        self.label = QLabel("YouTube Songs Downloader", self)
        self.log_label = QLabel("Logs will appear here", self)

        self.song_input = QLineEdit(self)
        self.song_input.setPlaceholderText("Enter song title")

        self.option_qual = QLineEdit(self)
        self.option_qual.setPlaceholderText("Enter picture quality (low or high)")

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Enter download path (e.g. C:/Users/user/Downloads)")

        self.add_button = QPushButton("Add to list", self)
        self.add_button.clicked.connect(self.add_song)

        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.start_download)

        self.list_widget = QListWidget(self)
        self.list_log = QListWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.song_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.path_input)
        layout.addWidget(self.option_qual)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_label)
        layout.addWidget(self.list_log)
        self.setLayout(layout)

    def add_song(self):
        song = self.song_input.text()
        if song:
            songs.append(song)
            self.label.setText(f"Added: {song}")
            self.list_widget.addItem(song)
        else:
            self.label.setText("❗ Please enter a song title")

    def start_download(self):
        path = self.path_input.text()
        option_qual = self.option_qual.text().strip().lower()

        if not path:
            self.label.setText("❗ Please enter a download path")
            msgbox.showwarning("Missing Path(warn-code:001)", "❗ Please enter a download path")
            return

        if not songs:
            msgbox.showwarning("Missing Songs(warn-code:002)", "❗ Please add at least one song to the list")
            return

        if option_qual not in ["low", "high"]:
            msgbox.showwarning("Missing Option(warn-code:003)", "❗ Please enter picture quality: 'low' or 'high'")
            return

        self.label.setText("⬇️ Starting download...")
        self.worker = DownloadWorker(songs, path, option_qual)
        self.worker.log_signal.connect(self.update_log)
        self.worker.log_signal1.connect(self.update_log1)
        self.worker.start()

    def update_log(self, message):
        self.log_label.setText(message)
        self.list_log.addItem(message + datetime.now().strftime("    [%Y/%m/%d] %H:%M:%S"))
        print(message)

    def update_log1(self, message):
        self.label.setText(message)
        print(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
