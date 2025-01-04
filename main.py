import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QComboBox, QProgressBar
)
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import yt_dlp


class VideoDownloader(QThread):
    download_progress = pyqtSignal(int)  # Tiến trình tải (%)
    download_completed = pyqtSignal(str)  # Thông báo tải xong
    download_failed = pyqtSignal(str)  # Thông báo lỗi

    def __init__(self, url, output_path, download_video, download_audio, video_quality, audio_quality):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.download_video = download_video
        self.download_audio = download_audio
        self.video_quality = video_quality
        self.audio_quality = audio_quality

    def get_ffmpeg_path(self):
        # Trả về đường dẫn tới ffmpeg.exe trong thư mục 'tools'
        return os.path.join(os.path.dirname(__file__), 'tools', 'ffmpeg.exe')

    def run(self):
        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded_bytes = d.get('downloaded_bytes', 0)
                total_bytes = d.get('total_bytes', None)
                if total_bytes:
                    percentage = int(downloaded_bytes / total_bytes * 100)
                    self.download_progress.emit(percentage)

        try:
            # Cấu hình chung cho yt-dlp
            ydl_opts = {
                'ffmpeg_location': self.get_ffmpeg_path(),
                'progress_hooks': [progress_hook],
                'nocolor': True,
                'outtmpl': os.path.join(self.output_path, '%(playlist_title)s/%(title)s.%(ext)s'),
                'restrictfilenames': False,  # Giữ nguyên tên file gốc
                'retries': 10  # Tăng số lần thử lại
            }

            if self.download_audio:
                # Tải âm thanh MP3
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': self.audio_quality,
                    }]
                })
                task = "Tải âm thanh MP3 thành công!"
            elif self.download_video:
                # Tải video MP4 với chất lượng cao nhất
                ydl_opts.update({
                    'format': f'bestvideo[height<={self.video_quality}]+bestaudio/best',
                    'merge_output_format': 'mp4'
                })
                task = "Tải video MP4 thành công!"
            else:
                raise ValueError("Không có tùy chọn nào được chọn.")

            # Chạy yt-dlp với cấu hình
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.download_progress.emit(100)  # Đảm bảo 100% khi hoàn tất
            self.download_completed.emit(task)
        except Exception as e:
            self.download_failed.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader - MP3 & MP4")
        self.setGeometry(300, 300, 600, 500)

        # Layout chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Widgets
        self.url_label = QLabel("Nhập URL của video/danh sách phát YouTube:")
        self.url_input = QLineEdit()

        self.folder_label = QLabel("Thư mục lưu trữ:")
        self.folder_button = QPushButton("Chọn thư mục")
        self.folder_button.clicked.connect(self.select_folder)

        self.download_video_checkbox = QCheckBox("Tải video MP4 (chất lượng cao nhất)")
        self.download_audio_checkbox = QCheckBox("Tải âm thanh MP3")

        self.video_quality_label = QLabel("Chọn chất lượng video:")
        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(["4320 (8K)", "2160 (4K)", "1080", "720", "480", "360", "240"])

        self.audio_quality_label = QLabel("Chọn chất lượng âm thanh (kbps):")
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["320", "192", "128"])

        self.download_button = QPushButton("Tải")
        self.download_button.clicked.connect(self.download_content)
        self.progress_bar = QProgressBar()
        self.status_label = QLabel("")

        # CSS cho giao diện
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 14px;
                background-color: #4682B4;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5A9BD5;
            }
            QCheckBox {
                font-size: 14px;
            }
            QProgressBar {
                height: 20px;
                text-align: center;
                font-size: 12px;
                background-color: #f3f3f3;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Add widgets
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
            self.folder_label.setText(f"Thư mục lưu trữ: {folder}")

    def download_content(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập URL của video/danh sách phát.")
            return

        if not self.output_folder:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục lưu trữ.")
            return

        download_video = self.download_video_checkbox.isChecked()
        download_audio = self.download_audio_checkbox.isChecked()
        video_quality = self.video_quality_combo.currentText().split(" ")[0] if download_video else None
        audio_quality = self.audio_quality_combo.currentText() if download_audio else None

        self.status_label.setText("Đang tải...")
        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # Tạo thread tải
        self.downloader_thread = VideoDownloader(
            url, self.output_folder, download_video, download_audio, video_quality, audio_quality
        )

        self.downloader_thread.download_progress.connect(self.progress_bar.setValue)
        self.downloader_thread.download_completed.connect(self.show_popup)
        self.downloader_thread.download_failed.connect(self.show_error)
        self.downloader_thread.start()

    def show_popup(self, message):
        QMessageBox.information(self, "Hoàn tất", message)
        self.reset_ui()

    def show_error(self, error):
        QMessageBox.critical(self, "Lỗi", f"Quá trình tải thất bại: {error}")
        self.reset_ui()

    def reset_ui(self):
        self.progress_bar.setValue(0)
        self.status_label.setText("")
        self.download_button.setEnabled(True)
        self.url_input.clear()
        self.download_video_checkbox.setChecked(False)
        self.download_audio_checkbox.setChecked(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
