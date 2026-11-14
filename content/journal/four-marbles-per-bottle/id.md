---
title: Empat kelereng per botol: seluruh aturannya
date: 2026-11-13
time: 22:28
summary: Aturan Bottled Marbles muat dalam beberapa baris. Inilah aturannya, beserta keputusan-keputusan kecil di sekitarnya.
lang: id
copy_review: iris
---
Bottled Marbles adalah teka-teki menyortir: pindahkan kelereng di antara botol kaca sampai setiap botol hanya berisi satu warna. Seluruh aturannya sengaja dibuat singkat.

## Aturan, seperti yang tertulis

- Satu botol memuat **4 kelereng**. Level dengan n warna memiliki 4 × n kelereng.
- Ada n + 2 botol: n botol dimulai dalam keadaan terisi, dan **2 botol dimulai kosong**.
- Kamu bisa menuang dari botol yang tidak kosong ke botol yang tidak penuh, dan hanya ke botol kosong atau ke atas kelereng berwarna sama.
- Kamu menuang seluruh deretan kelereng sewarna di bagian atas, sejauh botol tujuan masih punya ruang, dan itu dihitung sebagai **satu langkah**.
- Kamu menang ketika setiap botol kosong atau penuh dengan satu warna.

Jumlah warna bertambah seiring level: `min(3 + floor((level + 1) / 2), 8)`, jadi level awal punya tiga warna dan level berikutnya berhenti bertambah di delapan.

## Empat dan dua

Kapasitas empat dan dua botol cadangan berasal langsung dari prototipe pertama. Dua botol kosong itu adalah ruang bernapas yang membuat menuang bisa dilakukan, dan kami belum perlu mengubah kedua angka tersebut.

## Keputusan kecil yang penting

- Mengetuk botol yang sama lagi akan membatalkan pilihan, dan botol kosong tidak bisa dipilih.
- Mengetuk botol yang tidak bisa dituangi akan memberi tahu hal itu dan memindahkan pilihanmu ke sana, alih-alih mengabaikan ketukan secara diam-diam.
- Urungkan tidak terbatas dan mengurangi satu langkah dari penghitung. Ulangi mengembalikan level ke susunan pertamanya.

Aturan-aturan ini berasal dari prototipe pertama yang bisa dimainkan dan dipertahankan tanpa perubahan di aplikasi. Rekor yang kami simpan untuk setiap level adalah jumlah langkah paling sedikit yang kamu butuhkan.
