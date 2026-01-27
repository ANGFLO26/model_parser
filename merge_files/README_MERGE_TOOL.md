# Hướng Dẫn Sử Dụng Tool Merge File (Markdown Merger Pro)

## Giới thiệu
**Markdown Merger Pro** giúp bạn tự động ghép nối các file kết quả (`page_1.md`, `page_2.md`...) sau khi xử lý OCR thành một file Markdown duy nhất, hoàn chỉnh.

Tool sẽ:
1.  Giải nén file ZIP chứa các file Markdown.
2.  Tự động sắp xếp các trang theo đúng thứ tự (1, 2, 3...).
3.  Nối nội dung và xóa các ký tự xuống dòng thừa/gạch ngang ngắt trang không cần thiết.
4.  Xuất ra một file `KET_QUA_GOP.md` duy nhất.

---

## Cách chạy Tool

**Yêu cầu:** Máy đã cài đặt Python và thư viện `gradio`.
Nếu chưa cài, chạy lệnh sau:
```bash
pip install gradio
```

**Cách chạy:**
1.  Mở terminal tại thư mục chứa code `model_parser`.
2.  Chạy lệnh:
    ```bash
    python merge_files/tool_merge.py
    ```
3.  Trình duyệt web sẽ tự động mở giao diện tại `http://127.0.0.1:7860`.

---

## Quy trình Sử dụng

1.  **Chuẩn bị file:**
    *   Sau khi chạy `dots.ocr` xong, bạn nén toàn bộ các file `page_X.md` (hoặc thư mục chứa chúng) thành một file **.zip**.
    
2.  **Upload:**
    *   Kéo thả file `.zip` vừa nén vào ô **"Upload ZIP File"** trên giao diện web.
    
3.  **Xử lý:**
    *   Bấm nút **🚀 Start Processing**.
    *   Chờ vài giây, tool sẽ hiển thị log xử lý và số lượng trang đã ghép.

4.  **Tải về:**
    *   File kết quả `KET_QUA_GOP.md` sẽ hiện ra ở ô **"Download result file"**.
    *   Bấm vào để tải về máy.

---

## Lưu ý 💡
*   Tool tìm các file có tên chứa `page_` và đuôi `.md` (ví dụ: `yourfile_page_1.md`).
*   Tool tự động sắp xếp số thông minh (ví dụ: page_2 sẽ đứng trước page_10).
*   File kết quả cũng được lưu tự động vào thư mục `merge_files/KET_QUA/` trong project của bạn.
