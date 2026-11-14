---
title: Bốn viên bi mỗi chai: toàn bộ luật chơi
date: 2026-11-13
time: 22:28
summary: Luật của Bottled Marbles gói gọn trong vài dòng. Đây là luật chơi, cùng những quyết định nhỏ xung quanh.
lang: vi
copy_review: iris
---
Bottled Marbles là một trò xếp phân loại: chuyển bi giữa các chai thủy tinh cho đến khi mỗi chai chỉ còn một màu. Toàn bộ luật chơi được cố ý giữ ngắn.

## Luật chơi, như đã ghi

- Một chai chứa **4 viên bi**. Một màn có n màu thì có 4 × n viên bi.
- Có n + 2 chai: n chai bắt đầu đầy bi, và **2 chai bắt đầu trống**.
- Bạn có thể rót từ một chai không trống sang một chai chưa đầy, và chỉ rót lên chai trống hoặc lên viên bi cùng màu.
- Bạn rót cả dãy bi cùng màu ở trên cùng, trong chừng mực chai đích còn chỗ, và việc đó tính là **một nước đi**.
- Bạn thắng khi mọi chai đều trống hoặc đầy một màu duy nhất.

Số màu tăng theo màn: `min(3 + floor((level + 1) / 2), 8)`, nên các màn đầu có ba màu và các màn sau ngừng tăng ở tám màu.

## Bốn và hai

Sức chứa bốn và hai chai trống dự phòng đến thẳng từ bản mẫu đầu tiên. Hai chai trống là khoảng thở giúp việc rót có thể thực hiện được, và chúng tôi chưa cần đổi con số nào trong hai số đó.

## Những quyết định nhỏ nhưng quan trọng

- Chạm lại vào cùng một chai sẽ bỏ chọn, và chai trống không thể được chọn.
- Chạm vào chai không thể rót vào sẽ báo cho bạn biết và chuyển lựa chọn sang chai đó, thay vì lặng lẽ bỏ qua cú chạm.
- Hoàn tác không giới hạn và trừ một nước đi khỏi bộ đếm. Chơi lại đưa màn về cách sắp xếp ban đầu.

Những luật này xuất phát từ bản mẫu chơi được đầu tiên và được giữ nguyên trong ứng dụng. Kỷ lục chúng tôi lưu cho mỗi màn là số nước đi ít nhất bạn cần.
