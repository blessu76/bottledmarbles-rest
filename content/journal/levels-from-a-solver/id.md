---
title: Level dibuat oleh solver, bukan keberuntungan
summary: Mengacak kelereng secara acak bisa menghasilkan susunan yang tidak mungkin diselesaikan. Jadi kami membuat setiap level lebih dulu dan membuktikan bahwa level itu bisa diselesaikan.
lang: id
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Teka-teki menyortir punya jebakan: kalau kelereng diacak begitu saja, sebagian susunan memang tidak bisa diselesaikan. Tidak ada yang senang baru menyadarinya di langkah keempat puluh.

## Keputusannya

Level tidak dibuat saat kamu bermain. Sebuah solver membuatnya sebelum aplikasi dirilis, dan aplikasi menyertakan hasilnya sebagai file statis: untuk setiap level, susunan botol dan **jumlah langkah paling sedikit** yang dibutuhkan untuk menyelesaikannya. Aplikasi hanya membaca level lewat satu antarmuka kecil, jadi cara pembuatannya bisa berubah tanpa menyentuh layar-layarnya.

Kami memilih cara ini karena level yang sudah dibuat pasti bisa diselesaikan, dan karena dengan mengetahui jumlah minimumnya, aplikasi bisa menampilkannya di samping hasil terbaikmu.

## Cara level dibuat

- Mulai dari n warna dengan seed acak yang tetap: n botol terisi penuh, ditambah 2 botol kosong.
- Cari solusi. Prototipe pertama memakai depth-first search dengan batas 60.000 status.
- Pencarian melewati langkah yang tidak mungkin membantu: menyentuh botol yang sudah selesai, menuang ke botol kosong lebih dari sekali, memindahkan satu kelereng dari botol berisi satu kelereng ke botol kosong.
- Sebuah status disimpan sebagai daftar botol yang sudah diurutkan, sehingga dua susunan yang hanya berbeda urutan botolnya dianggap sama.
- Lalu cari jumlah langkah paling sedikit: breadth-first search untuk level kecil, iterative deepening untuk level besar.
- Level yang tidak bisa diselesaikan, sudah selesai sejak awal, atau terlalu mudah dibuang. Sisanya diurutkan dari mudah ke sulit.

## Pemeriksaan

Rencana kami mencakup tes yang menyelesaikan ulang setiap level yang disertakan, dan versi pertama yang bisa dimainkan menargetkan setidaknya 30 level. Halaman utama sekarang menyebut 150.
