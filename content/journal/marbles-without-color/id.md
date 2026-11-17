---
title: Kelereng yang bisa dibedakan tanpa warna
summary: Sepuluh warna kelereng, sepuluh simbol, beberapa uji tata letak di layar kecil, dan satu tombol yang tidak bisa diketuk.
lang: id
copy_review: iris
date: 2026-11-17
time: 17:00
---
Gim yang mengurutkan berdasarkan warna punya masalah yang jelas: sebagian pemain tidak bisa membedakan warna. Build 6 aplikasi ini, yang membawa desain Teal Glass, menangani masalah itu dan beberapa hal kecil lainnya.

## Simbol pada kelereng

Ada sepuluh warna kelereng, dan setiap warna juga punya **simbol**-nya sendiri. Warna adalah petunjuk utama, simbol adalah cadangannya, sehingga level tetap bisa diselesaikan ketika dua warna tampak mirip.

## Menguji layar kecil

Uji widget menggambar layar pada lebar 320 dan 375 px, dalam mode gelap dan terang, dengan teks diperbesar hingga 200%, dan dinyatakan gagal jika ada konten yang meluap. Rangkaian uji ini murah dijalankan dan menangkap jenis bug yang kalau tidak, baru muncul di ponsel kecil milik seseorang.

Yang belum kami lakukan: pengujian ini berupa uji widget ditambah tangkapan layar dari simulator selebar sekitar 393 px. Pengecekan di ponsel sungguhan pada lebar 320 atau 375 px masih tertunda, dan hal itu kami tulis di catatan kami.

## Tombol di bawah scroll view

Saat membuat layar beranda, kami menemukan bahwa tombol pengaturan tidak merespons ketukan. Penyebabnya ada pada susunan lapisan: tombol itu berada di dalam stack di bawah scroll view, sehingga scroll view menangkap semua sentuhan. Mengubah urutan stack memperbaikinya. Perbaikan ini masuk di build yang sama dengan desain ulangnya.

## Yang akan datang

Enam sumbat botol dan lima kulit botol sudah dirancang, tetapi sejauh ini baru tampilan bawaan yang dirilis. Strukturnya bisa berkembang untuk menampung semuanya. Animasi menuang yang baru dan haptik juga belum ada; perilaku yang sekarang tetap sama.
