---
title: "Bản build TestFlight đầu tiên đã lên như thế nào"
description: "Sau khi xong MVP, bản build nội bộ đầu tiên đã lên, nhưng script triển khai từng chặn chúng tôi một lần."
copy_review: iris 2026-11-14
---
MVP đầu tiên của Moss Garden, một game idle trên iOS, đã lên TestFlight với phiên bản 1.0.0 (1) để thử nghiệm nội bộ sau khi script triển khai chặn lần thử đầu tiên. Quá trình xử lý mất khoảng ba phút, và bản build này không được gửi duyệt cũng như không mở cho người thử nghiệm bên ngoài.

## MVP có những gì

MVP đầu tiên gồm tám loại cây, tính toán khi ngoại tuyến, các mùa, sổ sưu tầm, lưu trữ và phần cài đặt. Sau đó chúng tôi tải nó lên TestFlight với phiên bản 1.0.0 (1) để thử nghiệm nội bộ. Quá trình xử lý mất khoảng ba phút, và chúng tôi không gửi duyệt cũng không mở cho người thử nghiệm bên ngoài.

## Lần thử đầu tiên thất bại

Khi script triển khai chạy green gate, một biến môi trường có nghĩa là "đừng tăng số build" đã lọt vào phần kiểm thử và làm hỏng chúng, nên script dừng ngay tại đó. Nhờ lần dừng ấy, không có bản build lỗi nào được tải lên. Chúng tôi sửa để các tiến trình con không còn thừa hưởng môi trường bên ngoài, rồi tải lên lại.

Triển khai có thể rất phiền, nhưng chúng tôi giữ một quy tắc: nếu kiểm thử chưa xanh thì không phát hành gì cả.

## Câu hỏi thường gặp

### Bản build TestFlight đầu tiên của Moss Garden có những gì?
Tám loại cây, tính toán khi ngoại tuyến, các mùa, sổ sưu tầm, lưu trữ và cài đặt, được tải lên với phiên bản 1.0.0 (1) để thử nghiệm nội bộ.

### Moss Garden đã được gửi duyệt trên App Store chưa?
Chưa. Bản build này chỉ được tải lên để thử nghiệm nội bộ, và chúng tôi chưa gửi duyệt.
