---
title: "Vì sao chúng tôi giữ hai bản sao của dữ liệu lưu"
description: "Mất khu vườn đã chăm bao lâu là điều tệ nhất, nên dữ liệu lưu được tách thành tệp chính và bản dự phòng."
---
Moss Garden, một game idle trên iOS, bảo vệ khu vườn của bạn bằng hai lớp an toàn: checksum phát hiện dữ liệu lưu bị hỏng và một bản dự phòng riêng để khôi phục, kèm thông báo. Việc chỉnh lùi đồng hồ thiết bị để nhận thưởng cũng bị phát hiện, và khoảng thời gian đó không được tính.

## Hai lớp an toàn cho dữ liệu lưu

Trong một game idle, điều đáng buồn nhất là mất đi khu vườn bạn đã chăm sóc. Vì vậy việc lưu có hai lớp an toàn.

Lớp thứ nhất là checksum: một giá trị kiểm tra được ghi cùng dữ liệu lưu, và nếu khi tải lên mà không khớp thì tệp bị coi là hỏng. Lớp thứ hai là bản dự phòng: tệp chính và bản dự phòng được giữ riêng, nên nếu tệp chính hỏng, chúng tôi khôi phục từ bản dự phòng và báo cho bạn biết. Chúng tôi cũng chú ý đến thứ tự, để tệp chính bị hỏng không bao giờ ghi đè lên bản dự phòng còn tốt.

## Chỉnh lùi đồng hồ

Chúng tôi cũng phải chặn mẹo chỉnh lùi đồng hồ thiết bị để nhận thưởng. Khi phát hiện đồng hồ bị lùi, khoảng thời gian đó không được tính, và ứng dụng sẽ báo cho bạn.

## Giữ cho dữ liệu lưu cũ vẫn dùng được

Khi thêm tính năng, chúng tôi giữ nguyên định dạng dữ liệu lưu và chỉ thêm trường mới, nên dữ liệu lưu cũ vẫn mở được trên các phiên bản mới hơn.

## Câu hỏi thường gặp

### Điều gì xảy ra nếu tệp lưu của Moss Garden bị hỏng?
Checksum phát hiện sự không khớp, game khôi phục từ bản dự phòng riêng và cho bạn biết điều đó.

### Tôi có thể nhận thưởng bằng cách đổi đồng hồ thiết bị không?
Không. Khi phát hiện đồng hồ bị lùi, khoảng thời gian đó không được tính, và ứng dụng sẽ báo cho bạn.
