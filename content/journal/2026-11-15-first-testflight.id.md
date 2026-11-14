---
title: "Begini build TestFlight pertama naik"
description: "Setelah MVP selesai, build internal pertama naik, tetapi skrip deploy sempat menghentikan kami satu kali."
---
MVP pertama Moss Garden, game idle untuk iOS, naik ke TestFlight sebagai 1.0.0 (1) untuk pengujian internal setelah skrip deploy menghentikan percobaan pertama. Pemrosesan memakan waktu sekitar tiga menit, dan build ini tidak diajukan untuk ditinjau maupun dibuka untuk penguji eksternal.

## Isi MVP

MVP pertama terbentuk dengan delapan tanaman, penghitungan offline, musim, buku koleksi, penyimpanan, dan pengaturan. Kami lalu mengunggahnya ke TestFlight sebagai 1.0.0 (1) untuk pengujian internal. Pemrosesan memakan waktu sekitar tiga menit, dan kami tidak mengajukannya untuk ditinjau maupun membukanya untuk penguji eksternal.

## Percobaan pertama gagal

Saat skrip deploy menjalankan green gate, sebuah variabel lingkungan yang artinya "jangan naikkan nomor build" ikut bocor ke dalam tes dan merusaknya, sehingga skrip berhenti di situ. Berkat penghentian itu, tidak ada build buruk yang terunggah. Kami memperbaikinya agar proses anak tidak lagi mewarisi lingkungan luar, lalu mengunggah ulang.

Deploy memang bisa merepotkan, tetapi aturan kami tetap: kalau tes belum hijau, tidak ada yang dirilis.

## FAQ

### Apa saja isi build TestFlight pertama Moss Garden?
Delapan tanaman, penghitungan offline, musim, buku koleksi, penyimpanan, dan pengaturan, diunggah sebagai 1.0.0 (1) untuk pengujian internal.

### Apakah Moss Garden sudah diajukan untuk tinjauan App Store?
Belum. Build ini hanya diunggah untuk pengujian internal, dan kami tidak mengajukannya untuk ditinjau.
