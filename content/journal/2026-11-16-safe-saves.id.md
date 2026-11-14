---
title: "Mengapa kami menyimpan dua salinan data simpanan"
description: "Kehilangan taman yang sudah dirawat itu yang terburuk, jadi data simpanan dibagi menjadi berkas utama dan cadangan."
copy_review: iris 2026-11-14
---
Moss Garden, game idle untuk iOS, melindungi taman Anda dengan dua pengaman: checksum yang mendeteksi data simpanan yang rusak, dan cadangan terpisah untuk memulihkannya, lengkap dengan pemberitahuan. Memundurkan jam perangkat untuk mengambil hadiah juga terdeteksi, dan rentang waktu itu tidak dihitung.

## Dua pengaman untuk data simpanan

Dalam game idle, hal yang paling menyedihkan adalah kehilangan taman yang sudah Anda rawat. Karena itu penyimpanan punya dua pengaman.

Yang pertama adalah checksum: nilai pemeriksa ditulis bersama data simpanan, dan jika tidak cocok saat dimuat, berkas dianggap rusak. Yang kedua adalah cadangan: berkas utama dan cadangan disimpan terpisah, jadi jika berkas utama rusak, kami memulihkannya dari cadangan dan memberi tahu Anda. Kami juga berhati-hati soal urutannya, agar berkas utama yang rusak tidak pernah menimpa cadangan yang sehat.

## Jam yang dimundurkan

Kami juga harus menghentikan trik memundurkan jam perangkat untuk mengambil hadiah. Saat pemunduran jam terdeteksi, rentang waktu itu tidak dihitung, dan aplikasi memberi tahu Anda.

## Menjaga data simpanan lama tetap berfungsi

Saat menambah fitur, kami mempertahankan format data simpanan dan hanya menambahkan kolom baru, sehingga data simpanan lama tetap bisa dibuka di versi yang lebih baru.

## FAQ

### Apa yang terjadi jika berkas simpanan Moss Garden rusak?
Checksum mendeteksi ketidakcocokan, lalu game memulihkan dari cadangan terpisah dan memberi tahu Anda bahwa hal itu terjadi.

### Bisakah saya mendapat hadiah dengan mengubah jam perangkat?
Tidak. Saat pemunduran jam terdeteksi, rentang waktu itu tidak dihitung, dan aplikasi memberi tahu Anda.
