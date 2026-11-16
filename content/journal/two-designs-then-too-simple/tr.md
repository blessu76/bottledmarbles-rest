---
title: İki tasarım önerisi ve bir "fazla sade"
summary: Uygulama için iki eksiksiz tasarım önerisini karşılaştırdık, ikisinden de fikirler aldık, sonra tek bir geri bildirimle sonucu çöpe attık.
lang: tr
copy_review: iris
date: 2026-11-16
time: 12:15
---
Uygulamayı cilalamadan önce iki eksiksiz tasarım yönünü yazıya döküp yan yana koyduk.

## İki öneri

- **Cam ve mürekkep:** tek bir vurgu rengine sahip mürekkep renkli bir arka plan; böylece arayüz geri çekilir, yıldız misketler olur. Renk körlüğü için bir sembol modu, başparmağın erişebileceği bir alt sayfa ve bir hareket hikâyesi getiriyordu: kaldır, taşı, bırak.
- **Temiz, premium bulmaca:** mavimsi beyaz ve lacivert, üst üste katmanlı kartlarla. Gücü, doğrudan üzerine inşa edilebilecek kesin sayılar, dört ekran durumu, yanlış dökümde titreme ve bir uygulama sırasıydı.

Notlarımız zayıf noktalar konusunda dürüsttü. Birincisinde anlamsal renkler ve hata geri bildirimi yoktu, dört sütunlu seviye kutucukları da 320 px'te sıkışıktı. İkincisi sıradan duruyordu ve metin boyutlarından biri küçük ekranlarda en az 12 sp kuralımızı çiğniyordu. İkisinde de renk kontrastı ve renk körlüğü simülasyonu doğrulanmadı.

Görünüm için birinciye, teknik özellikler ve durumlar için ikinciye yöneldik.

## Sonra geri bildirim

Geri bildirim kısaydı: **fazla sade**. Biz de süs eklemek yerine baştan başladık.

## Sürüm 2: Teal Glass

- Uygulamanın zaten sahip olduğu petrol yeşili ve altını koru, daha da ileri taşı.
- Koyu: derin petrol yeşili mürekkep, vurgu olarak altın. Açık: sıcak kâğıt, vurgu olarak derin petrol yeşili.
- Cam şişeler ve misketler, düz daireler gibi değil nesneler gibi okunsun diye geçişler ve filtrelerle çizildi.
- İki önerinin en iyi yanlarını içine aldı: tek vurgulu mürekkep, sembollü on misket rengi, alt sayfalar, anlamsal renkler, seviye durumları, ilerleme çubuğu, yanlış dökümde titreme ve 320 px kuralları.

Öneri sayfası konsepti, koyu ve açık temada sekiz ekranı, varlık dökümlerini, hareketi ve bir erişilebilirlik kontrolünü kapsıyor.
