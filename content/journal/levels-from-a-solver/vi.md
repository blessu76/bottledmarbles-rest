---
title: Màn chơi do bộ giải tạo ra, không phải do may rủi
summary: Xáo trộn bi ngẫu nhiên có thể tạo ra màn không thể giải. Vì vậy chúng tôi tạo sẵn mọi màn chơi và chứng minh rằng chúng đều hoàn thành được.
lang: vi
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Trò xếp phân loại có một cái bẫy: nếu xáo bi ngẫu nhiên, một số cách sắp xếp sẽ không thể giải được. Chẳng ai thích phát hiện ra điều đó ở nước đi thứ bốn mươi.

## Quyết định

Màn chơi không được tạo trong lúc bạn chơi. Một bộ giải (solver) dựng chúng trước khi ứng dụng phát hành, và ứng dụng đóng gói kết quả thành một tệp tĩnh: với mỗi màn là cách sắp xếp các chai và **số nước đi ít nhất** cần để giải. Ứng dụng chỉ đọc màn chơi qua một giao diện nhỏ, nên cách tạo màn có thể thay đổi mà không phải đụng đến các màn hình.

Chúng tôi chọn cách này vì màn đã dựng sẵn chắc chắn giải được, và vì biết số nước tối thiểu giúp ứng dụng hiển thị nó cạnh kết quả tốt nhất của bạn.

## Một màn chơi được tạo ra thế nào

- Bắt đầu từ n màu với một hạt giống ngẫu nhiên cố định: n chai đầy, cộng thêm 2 chai rỗng.
- Tìm lời giải. Bản thử nghiệm đầu tiên dùng tìm kiếm theo chiều sâu với giới hạn 60.000 trạng thái.
- Việc tìm kiếm bỏ qua những nước không thể giúp ích: chạm vào chai đã hoàn thành, rót vào các chai rỗng quá một lần, chuyển một viên bi từ chai chỉ có một viên sang chai rỗng.
- Một trạng thái được lưu dưới dạng danh sách các chai đã sắp xếp, nên hai cách bày chỉ khác thứ tự chai được tính là một.
- Sau đó tìm số nước ít nhất: tìm kiếm theo chiều rộng cho màn nhỏ, đào sâu dần (iterative deepening) cho màn lớn.
- Những màn không giải được, đã giải xong sẵn hoặc quá dễ sẽ bị loại bỏ. Phần còn lại được xếp từ dễ đến khó.

## Kiểm tra

Kế hoạch có một bài kiểm thử giải lại mọi màn được đóng gói, và phiên bản chơi được đầu tiên đặt mục tiêu ít nhất 30 màn. Trang giới thiệu hiện ghi 150.
