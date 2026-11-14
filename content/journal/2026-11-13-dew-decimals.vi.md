---
title: "Vì sao hiển thị sương với số thập phân"
description: "Rêu lớn thêm 0,1 mỗi giây, vậy mà bộ đếm sương trông như đứng yên. Đây là cách chúng tôi sửa định dạng số."
copy_review: iris 2026-11-14
---
Moss Garden là một game idle (tăng dần) trên iOS, và bộ đếm sương từng trông như đứng yên vì chỉ hiển thị số nguyên từ mười trở lên. Giờ chúng tôi hiển thị hai chữ số thập phân khi dưới 1 và một chữ số thập phân khi dưới 1.000, đồng thời làm tròn xuống để con số không bao giờ hứa hẹn nhiều hơn những gì bạn đang có.

## Vì sao con số trông như đứng yên

Rêu tích lũy thêm 0,1 mỗi giây, nhưng con số sương ở đầu màn hình cứ giữ nguyên rất lâu. Một người thử nghiệm nói họ không thể biết nó có đang đếm hay không. Nguyên nhân rất đơn giản: từ mười trở lên chúng tôi chỉ hiển thị số nguyên.

## Chúng tôi đã đổi gì

Giá trị dưới 1 giờ hiển thị hai chữ số thập phân, còn dưới 1.000 thì một chữ số. Các số 0 ở cuối được bỏ đi, nên bạn đọc là 289 chứ không phải 289,0.

Quyết định thực sự quan trọng là cách làm tròn. Hiển thị 185,56 thành 185,6 sẽ khiến thứ bạn chưa mua nổi trông như đã đủ tiền. Vì vậy chúng tôi **làm tròn xuống**: con số trên màn hình luôn nhiều nhất bằng những gì bạn thật sự có.

Đó là một thay đổi rất nhỏ, nhưng trong một trò chơi về sự chờ đợi, nhìn con số chuyển động cũng là một phần của phần thưởng.

## Câu hỏi thường gặp

### Vì sao Moss Garden hiển thị sương với số thập phân?
Vì rêu lớn thêm 0,1 mỗi giây, và số nguyên khiến bộ đếm trông như đứng yên. Số thập phân giúp bạn thấy nó đang đếm.

### Con số sương được làm tròn lên hay xuống?
Xuống. Con số trên màn hình luôn nhiều nhất bằng lượng bạn thật sự có, nên không có gì trông như mua được trước khi đủ.
