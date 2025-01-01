# **PyQt6 YouTube Downloader 🎥🎵**

Ứng dụng **PyQt6 YouTube Downloader** giúp tải video và âm thanh MP3 từ YouTube với giao diện đẹp, thân thiện và hỗ trợ các tùy chọn linh hoạt như chất lượng 4K, âm thanh MP3 cao cấp, và hiển thị tiến trình tải trực quan.

---

### 🛠️ Tải xuống và sử dụng

[![Click để tải](https://raw.githubusercontent.com/webdep24h/PingMonitorTool/main/images/Download.png)](https://drive.google.com/file/d/1nC9l42vyAcZieuZ7g73JpZ3LJm0Md0vq/view?usp=sharing)

Download tool tại: [PingMonitorTool](https://drive.google.com/file/d/1nC9l42vyAcZieuZ7g73JpZ3LJm0Md0vq/view?usp=sharing)

---
## **🚀 Tính năng**
- Tải video với độ phân giải tùy chọn: **2160p (4K)**, **1080p**, **720p**, v.v.
- Hỗ trợ tùy chọn tải **âm thanh MP3** với chất lượng lên đến **320kbps**.
- Hiển thị **% tiến trình tải** trực quan và chi tiết.
- Giao diện được xây dựng bằng **PyQt6**: dễ sử dụng và tương thích mọi hệ điều hành.
- Sử dụng **yt-dlp** và **FFmpeg** để xử lý tải xuống và chuyển đổi định dạng.

---

## **📂 Cấu trúc dự án**
```plaintext
PyQt6-Youtube-Downloader/
├── main.py              # File chính chạy ứng dụng
├── requirements.txt     # Danh sách các thư viện cần thiết
├── tools/               # Thư mục chứa FFmpeg
│   └── ffmpeg.exe       # Công cụ xử lý video/âm thanh
├── .gitignore           # File bỏ qua các thư mục/file không cần thiết
└── README.md            # File hướng dẫn
```

---

## **🛠️ Hướng dẫn cài đặt**

### **1. Yêu cầu hệ thống**
- **Python 3.11** trở lên.
- **Windows**, **macOS**, hoặc **Linux**.
- **FFmpeg** (đã được đính kèm trong thư mục `tools`).

---

### **2. Clone dự án từ GitHub**
1. Mở terminal hoặc command prompt.
2. Nhập lệnh sau để tải dự án:
   ```bash
   git clone https://github.com/webdep24h/PyQt6-Youtube-Downloader.git
   cd PyQt6-Youtube-Downloader
   ```

---

### **3. Tạo môi trường ảo và cài đặt thư viện**

#### **Tạo môi trường ảo**
1. Tạo môi trường ảo:
   ```bash
   python -m venv venv
   ```

2. Kích hoạt môi trường ảo:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

#### **Cài đặt thư viện**
1. Cài đặt các thư viện cần thiết từ `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. Kiểm tra xem thư viện đã được cài đặt thành công:
   ```bash
   pip list
   ```

---

### **4. Cấu hình FFmpeg**
1. FFmpeg đã được đính kèm trong thư mục `tools` của dự án:
   - Đường dẫn: `tools/ffmpeg.exe`.
2. Đảm bảo file `ffmpeg.exe` có mặt để ứng dụng hoạt động bình thường.

---

### **5. Chạy ứng dụng**
1. Sau khi cài đặt xong, chạy ứng dụng bằng lệnh:
   ```bash
   python main.py
   ```

2. Giao diện ứng dụng sẽ xuất hiện và bạn có thể bắt đầu tải video/âm thanh từ YouTube.

---

## **🎮 Cách sử dụng ứng dụng**

### **Bước 1**: Nhập URL video hoặc danh sách phát
- Dán URL video hoặc danh sách phát/kênh YouTube vào ô nhập liệu.

### **Bước 2**: Chọn thư mục lưu trữ
- Nhấn **"Chọn thư mục"** để chọn nơi lưu video hoặc âm thanh tải về.

### **Bước 3**: Chọn tùy chọn tải
- **Tải toàn bộ video**: Đánh dấu vào **"Tải toàn bộ video"**.
  - Chọn chất lượng video (2160p, 1080p, 720p, hoặc **"Cao nhất"** để tự động tải chất lượng tốt nhất).
- **Tải toàn bộ âm thanh**: Đánh dấu vào **"Tải toàn bộ âm thanh MP3"**.
  - Chọn chất lượng âm thanh (320kbps, 192kbps, hoặc 128kbps).

### **Bước 4**: Nhấn **"Tải"**
- Theo dõi tiến trình tải qua thanh tiến trình và thông báo trạng thái.

---

## **📄 File hướng dẫn**
1. **`main.py`**:
   - Chứa toàn bộ logic của ứng dụng, bao gồm giao diện PyQt6 và xử lý tải bằng yt-dlp.
2. **`requirements.txt`**:
   - Danh sách các thư viện cần thiết:
     ```plaintext
     pyqt6
     yt-dlp
     ```
3. **`tools/ffmpeg.exe`**:
   - Công cụ xử lý video và âm thanh bắt buộc.

---

## **💡 Mẹo sử dụng**
- **Cách tăng tốc độ tải**: 
  - Kết nối mạng ổn định.
  - Sử dụng `yt-dlp` để tối ưu tải (nó nhanh hơn nhiều so với các công cụ khác).
- **Cách khắc phục lỗi "Could not find ffmpeg"**:
  - Kiểm tra lại file `ffmpeg.exe` trong thư mục `tools`.
  - Thêm đường dẫn `tools` vào biến môi trường `PATH`.

---

## **📬 Hỗ trợ**
Nếu bạn gặp bất kỳ vấn đề nào, vui lòng liên hệ qua email:  
📧 **hotro@webdep24h.com**

---

## **📢 Đóng góp**
Nếu bạn muốn cải tiến ứng dụng, hãy:
1. Fork repository.
2. Tạo pull request với thay đổi của bạn.

---

## **📜 Bản quyền**
Ứng dụng được phát triển bởi **Phạm Thanh Thiệu**.  
Vui lòng giữ nguyên thông tin bản quyền khi sử dụng hoặc chỉnh sửa.

---

**Made with ❤️ by Phạm Thanh Thiệu.**