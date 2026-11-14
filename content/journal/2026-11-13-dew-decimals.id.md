---
title: "Mengapa embun ditampilkan dengan desimal"
description: "Lumut tumbuh 0,1 per detik, tetapi penghitung embun terlihat beku. Begini cara kami memperbaiki format angkanya."
copy_review: iris 2026-11-14
---
Moss Garden adalah game idle (incremental) untuk iOS, dan penghitung embunnya dulu terlihat beku karena hanya menampilkan bilangan bulat mulai dari sepuluh ke atas. Kini kami menampilkan dua desimal di bawah 1 dan satu desimal di bawah 1.000, serta membulatkan ke bawah agar angka tidak pernah menjanjikan lebih dari yang Anda punya.

## Mengapa angkanya terlihat beku

Lumut terus bertambah 0,1 per detik, tetapi angka embun di bagian atas layar bertahan sama dalam waktu lama. Seorang penguji bilang ia tidak bisa tahu apakah angkanya benar-benar berjalan. Penyebabnya sederhana: dari sepuluh ke atas kami hanya menampilkan bilangan bulat.

## Apa yang kami ubah

Nilai di bawah 1 kini ditampilkan dengan dua desimal, dan nilai di bawah 1.000 dengan satu desimal. Nol di belakang dihilangkan, jadi Anda membaca 289, bukan 289,0.

Keputusan yang sebenarnya penting adalah pembulatan. Menampilkan 185,56 sebagai 185,6 akan membuat sesuatu yang belum bisa Anda beli tampak terjangkau. Karena itu kami **membulatkan ke bawah**: angka di layar selalu paling banyak sebesar yang benar-benar Anda miliki.

Ini perubahan kecil, tetapi dalam game tentang menunggu, melihat angka bergerak adalah bagian dari hadiahnya.

## FAQ

### Mengapa Moss Garden menampilkan embun dengan desimal?
Karena lumut tumbuh 0,1 per detik, dan bilangan bulat membuat penghitung tampak beku. Dengan desimal, Anda bisa melihat bahwa angkanya berjalan.

### Apakah angka embun dibulatkan ke atas atau ke bawah?
Ke bawah. Angka di layar selalu paling banyak sebesar jumlah yang benar-benar Anda miliki, jadi tidak ada yang tampak terjangkau sebelum waktunya.
