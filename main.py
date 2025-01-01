import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QComboBox, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import yt_dlp
import subprocess

class VideoDownloader(QThread):
    download_progress = pyqtSignal(int)
    download_completed = pyqtSignal(str)
    download_failed = pyqtSignal(str)

    def __init__(self, url, output_path, download_video, download_audio, video_quality, audio_quality):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.download_video = download_video
        self.download_audio = download_audio
        self.video_quality = video_quality
        self.audio_quality = audio_quality

    def get_ffmpeg_path(self):
        # Return the path to ffmpeg in the 'tools' directory
        return os.path.join(os.path.dirname(__file__), 'tools', 'ffmpeg.exe')

    def run(self):
        def progress_hook(d):
            if d['status'] == 'downloading':
                percentage = d.get('_percent_str', '0.0').replace('%', '').strip()
                try:
                    progress = int(float(percentage))  # Chuyển đổi % thành số nguyên
                    self.download_progress.emit(progress)
                except ValueError:
                    self.download_progress.emit(0)

        try:
            if self.download_audio:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': self.audio_quality,
                        'ffmpeg_location': self.get_ffmpeg_path()
                    }],
                    'progress_hooks': [progress_hook],
                    'nocolor': True,
                    'outtmpl': os.path.join(self.output_path, '%(playlist_title)s/%(title)s.%(ext)s')
                }
                task = "Tải toàn bộ âm thanh MP3 thành công!"
            elif self.download_video:
                format_option = f'bestvideo[height<={self.video_quality}]+bestaudio[ext=m4a]/mp4'
                ydl_opts = {
                    'format': format_option,
                    'ffmpeg_location': self.get_ffmpeg_path(),
                    'progress_hooks': [progress_hook],
                    'nocolor': True,
                    'outtmpl': os.path.join(self.output_path, '%(playlist_title)s/%(title)s.%(ext)s')
                }
                task = "Tải toàn bộ video thành công!"
            else:
                raise ValueError("Không có tùy chọn nào được chọn.")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.download_progress.emit(100)  # Đảm bảo 100% khi hoàn tất
            self.download_completed.emit(task)
        except Exception as e:
            self.download_failed.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader - Tích hợp FFmpeg - Phạm Thanh Thiệu - 0988.927.177")
        self.setGeometry(300, 300, 600, 500)

        # Layout chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Widgets
        self.url_label = QLabel("Nhập URL của video/danh sách phát/kênh YouTube:")
        self.url_input = QLineEdit()
        self.folder_label = QLabel("Thư mục lưu trữ:")
        self.folder_button = QPushButton("Chọn thư mục")
        self.folder_button.clicked.connect(self.select_folder)

        self.download_video_checkbox = QCheckBox("Tải toàn bộ video")
        self.download_audio_checkbox = QCheckBox("Tải toàn bộ âm thanh MP3")

        self.video_quality_label = QLabel("Chọn chất lượng video:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(["2160 (4K)", "1080", "720", "480", "360", "240"])

        self.audio_quality_label = QLabel("Chọn chất lượng âm thanh (kbps):")
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["320", "192", "128"])

        self.download_button = QPushButton("Tải")
        self.download_button.clicked.connect(self.download_content)
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("")

        # Add các widget
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.folder_label)
        self.layout.addWidget(self.folder_button)
        self.layout.addWidget(self.download_video_checkbox)
        self.layout.addWidget(self.download_audio_checkbox)
        self.layout.addWidget(self.video_quality_label)
        self.layout.addWidget(self.video_quality_combo)
        self.layout.addWidget(self.audio_quality_label)
        self.layout.addWidget(self.audio_quality_combo)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.status_label)

        self.output_folder = ""
        self.downloader_thread = None

        # Kết nối checkbox để ẩn/hiện tùy chọn
        self.download_video_checkbox.stateChanged.connect(self.toggle_quality_options)
        self.download_audio_checkbox.stateChanged.connect(self.toggle_quality_options)

        # QSS Styling
        self.setStyleSheet("""
        QWidget {
            background-color: #f5f5f5;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
        }
        QLineEdit, QComboBox {
            border: 1px solid #aaa;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QCheckBox {
            padding: 5px;
        }
        QProgressBar {
            text-align: center;
            color: black;
        }
        QProgressBar::chunk {
            background-color: #0078d7;
            width: 20px;
        }
        QLabel {
            font-weight: bold;
        }
        """)

    def toggle_quality_options(self):
        if self.download_video_checkbox.isChecked():
            self.video_quality_combo.setEnabled(True)
            self.audio_quality_combo.setEnabled(False)
            self.audio_quality_label.setEnabled(False)
        elif self.download_audio_checkbox.isChecked():
            self.video_quality_combo.setEnabled(False)
            self.audio_quality_combo.setEnabled(True)
            self.audio_quality_label.setEnabled(True)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục lưu trữ")
        if folder:
            self.output_folder = folder

    def download_content(self):
        url = self.url_input.text().strip()
        if not self.output_folder:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục lưu trữ.")
            return

        download_video = self.download_video_checkbox.isChecked()
        download_audio = self.download_audio_checkbox.isChecked()
        video_quality = self.video_quality_combo.currentText().split(" ")[0] if download_video else None
        audio_quality = self.audio_quality_combo.currentText() if download_audio else None

        self.downloader_thread = VideoDownloader(
            url, self.output_folder, download_video, download_audio,
            video_quality, audio_quality
        )

        self.downloader_thread.download_progress.connect(self.progress_bar.setValue)
        self.downloader_thread.download_completed.connect(self.show_status)
        self.downloader_thread.download_failed.connect(self.show_error)
        self.downloader_thread.start()

    def show_status(self, message):
        self.status_label.setText(message)

    def show_error(self, error):
        QMessageBox.critical(self, "Lỗi", f"Quá trình tải thất bại: {error}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
