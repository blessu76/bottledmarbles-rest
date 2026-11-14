---
title: Şişe başına dört misket: kuralların tamamı
date: 2026-11-13
time: 22:28
summary: Bottled Marbles'ın kuralları birkaç satıra sığar. İşte kurallar ve çevresindeki küçük kararlar.
lang: tr
copy_review: iris
---
Bottled Marbles bir ayırma bulmacasıdır: Cam şişeler arasında misketleri taşıyarak her şişede tek bir renk kalmasını sağlarsınız. Kuralların tamamı bilerek kısa tutuldu.

## Yazıya geçirilmiş kurallar

- Bir şişe **4 misket** alır. n renkli bir seviyede 4 × n misket vardır.
- n + 2 şişe vardır: n tanesi dolu başlar, **2 tanesi boş başlar**.
- Boş olmayan bir şişeden dolu olmayan bir şişeye dökebilirsiniz; yalnızca boş bir şişeye ya da aynı renkteki bir misketin üzerine dökebilirsiniz.
- En üstteki aynı renkli misket dizisinin tamamını, hedef şişede yer olduğu kadar dökersiniz ve bu **bir hamle** sayılır.
- Her şişe ya boş ya da tek renkle dolu olduğunda kazanırsınız.

Renk sayısı seviyeyle birlikte artar: `min(3 + floor((level + 1) / 2), 8)`. Yani ilk seviyelerde üç renk vardır, sonraki seviyelerde artış sekizde durur.

## Dört ve iki

Dörtlük kapasite ve iki yedek şişe doğrudan ilk prototipten geliyor. İki boş şişe, dökmeyi mümkün kılan nefes alanıdır ve bu sayıların hiçbirini değiştirmemiz gerekmedi.

## Önemli küçük kararlar

- Aynı şişeye tekrar dokunmak seçimi kaldırır ve boş bir şişe seçilemez.
- Dökemeyeceğiniz bir şişeye dokunmak bunu söyler ve dokunuşu sessizce yok saymak yerine seçiminizi o şişeye taşır.
- Geri alma sınırsızdır ve hamle sayacından bir hamle düşer. Yeniden başlat, seviyeyi ilk dizilimine döndürür.

Bu kurallar ilk oynanabilir prototipten geldi ve uygulamada değiştirilmeden korundu. Her seviye için tuttuğumuz rekor, ihtiyaç duyduğunuz en az hamle sayısıdır.
