---
title: Renk olmadan da ayırt edilen misketler
summary: On misket rengi, on sembol, küçük ekranlarda birkaç yerleşim testi ve dokunulamayan bir düğme.
lang: tr
copy_review: iris
date: 2026-11-17
time: 17:00
---
Renklere göre ayırma yapılan bir oyunun bariz bir sorunu var: bazı oyuncular renkleri birbirinden ayıramıyor. Teal Glass tasarımını getiren uygulamanın 6. sürümü, bu sorunu ve birkaç küçük meseleyi ele alıyor.

## Misketlerin üzerindeki semboller

On misket rengi var ve her rengin ayrıca kendine ait bir **sembolü** var. Ana sinyal renk, yedek sinyal sembol; bu yüzden iki ton birbirine benzese de bir seviye çözülebilir kalıyor.

## Küçük ekranları test etmek

Widget testleri ekranları 320 ve 375 px genişlikte, koyu ve açık modda, metin %200'e büyütülmüş hâlde çizer ve herhangi bir taşma olursa başarısız olur. Bu matrisi çalıştırmak ucuzdur ve aksi hâlde ancak birinin küçük telefonunda ortaya çıkacak türden hataları yakalar.

Henüz yapmadığımız şey: bu testler, widget testleri ile yaklaşık 393 px genişliğindeki bir simülatörden alınan ekran görüntülerinden oluşuyor. Gerçek bir telefonda 320 veya 375 px ile kontrol hâlâ açık ve bunu notlarımızda da belirtiyoruz.

## Kaydırma görünümünün altındaki düğme

Ana ekranı yaparken ayarlar düğmesinin dokunmalara yanıt vermediğini fark ettik. Sebep katmanlamaydı: düğme yığında kaydırma görünümünün altında kalıyordu ve kaydırma görünümü bütün dokunuşları yakalıyordu. Yığının sırasını değiştirmek sorunu çözdü. Düzeltme, yeniden tasarımla aynı sürümde yapıldı.

## Sırada ne var

Altı şişe mantarı ve beş şişe kaplaması tasarlandı, ancak şimdilik yalnızca varsayılan görünüm yayında. Yapı bunlara yer açacak şekilde büyüyebilir. Yeni dökme animasyonları ve dokunsal geri bildirim de henüz yok; mevcut davranış aynı kalıyor.
