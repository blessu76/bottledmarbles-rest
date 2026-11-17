---
title: Những viên bi phân biệt được mà không cần màu
summary: Mười màu bi, mười ký hiệu, vài bài kiểm tra bố cục trên màn hình nhỏ, và một nút bấm không chạm được.
lang: vi
copy_review: iris
date: 2026-11-17
time: 17:00
---
Một trò chơi xếp theo màu có một vấn đề hiển nhiên: có người chơi không phân biệt được các màu. Bản dựng 6 của ứng dụng, mang theo thiết kế Teal Glass, xử lý vấn đề này cùng vài việc nhỏ hơn.

## Ký hiệu trên viên bi

Có mười màu bi, và mỗi màu còn có một **ký hiệu** riêng. Màu là tín hiệu chính, ký hiệu là tín hiệu dự phòng, nên màn chơi vẫn giải được khi hai sắc màu trông giống nhau.

## Kiểm tra màn hình nhỏ

Các bài kiểm tra widget vẽ màn hình ở chiều rộng 320 và 375 px, chế độ tối và sáng, với chữ phóng to 200%, và sẽ báo lỗi nếu có bất kỳ chỗ nào bị tràn. Bộ kiểm tra này chạy rất rẻ và bắt được loại lỗi mà nếu không thì chỉ lộ ra trên chiếc điện thoại nhỏ của ai đó.

Điều chúng tôi chưa làm: các bài kiểm tra này là kiểm tra widget cộng với ảnh chụp từ trình giả lập rộng khoảng 393 px. Việc kiểm tra trên điện thoại thật ở 320 hoặc 375 px vẫn còn đó, và chúng tôi cũng đã ghi như vậy trong ghi chú.

## Nút nằm dưới khung cuộn

Khi dựng màn hình chính, chúng tôi phát hiện nút cài đặt không phản hồi khi chạm. Nguyên nhân là do thứ tự các lớp: nút nằm trong stack bên dưới khung cuộn, nên khung cuộn nhận hết mọi lần chạm. Đổi lại thứ tự trong stack là xong. Lỗi này được sửa ngay trong bản dựng có thiết kế lại.

## Sắp tới

Sáu loại nút chai và năm kiểu vỏ chai đã được thiết kế, nhưng hiện mới có giao diện mặc định được phát hành. Cấu trúc có thể mở rộng để đón nhận chúng. Hiệu ứng rót mới và phản hồi rung cũng chưa có; hành vi hiện tại vẫn giữ nguyên.
