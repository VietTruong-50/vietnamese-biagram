# Vietnamese Bigram Language Model

Đây là bài tập xây dựng Mô hình ngôn ngữ N-gram (Bigram) cho tiếng Việt ở mức âm tiết.
Chương trình được viết bằng Python, sử dụng phương pháp là trơn Add-1 (Laplace Smoothing).

## Tính năng
1. **Tự động tải dữ liệu**: Tự động tải về tập dữ liệu 10.000 câu tin tức tiếng Việt từ Leipzig Corpora (`vie_news_2020_10K.tar.gz`).
2. **Tính xác suất câu**: Phân tích và tính toán xác suất xuất hiện của một câu cụ thể (Ví dụ: "Hôm nay trời đẹp lắm") dựa trên tập dữ liệu đã học.
3. **Sinh câu tự động**: Tự động sinh ra các câu tiếng Việt ngẫu nhiên dựa trên xác suất các bigram liên tiếp.

## Cách chạy dự án

Bạn chỉ cần môi trường có cài đặt Python 3. Không cần cài thêm thư viện phức tạp ngoài `requests` (nếu chưa có).

1. Mở Terminal / Command Prompt.
2. Chuyển đến thư mục chứa mã nguồn:
   ```bash
   cd /đường/dẫn/tới/thư/mục
   ```
3. Chạy lệnh thực thi file:
   ```bash
   python3 vietnamese_bigram_lm.py
   ```

## Nguồn dữ liệu
Tập dữ liệu được sử dụng để huấn luyện mô hình là: [Leipzig Corpora Collection - Vietnamese News 2020 10K](https://downloads.wortschatz-leipzig.de/corpora/vie_news_2020_10K.tar.gz).
Mã nguồn sẽ tự động tải file này về trong lần chạy đầu tiên.
