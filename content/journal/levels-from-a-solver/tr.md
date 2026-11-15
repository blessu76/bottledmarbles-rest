---
title: Seviyeleri şans değil, bir çözücü üretir
summary: Misketleri rastgele karıştırmak çözülemeyen düzenler doğurabilir. Bu yüzden her seviyeyi önceden üretiyor ve bitirilebildiğini kanıtlıyoruz.
lang: tr
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Ayırma bulmacalarının bir tuzağı vardır: misketleri rastgele karıştırırsanız bazı dizilimler hiçbir şekilde çözülemez. Bunu kırkıncı hamlede fark etmekten kimse hoşlanmaz.

## Karar

Seviyeler siz oynarken üretilmez. Bir çözücü onları uygulama yayımlanmadan önce hazırlar ve uygulama sonucu sabit bir dosya olarak içinde taşır: her seviye için şişelerin dizilimi ve onu çözmek için gereken **en az hamle sayısı**. Uygulama seviyeleri yalnızca küçük bir arayüz üzerinden okur; bu yüzden seviyelerin üretilme biçimi ekranlara dokunmadan değiştirilebilir.

Bunu seçtik çünkü önceden hazırlanmış bir seviyenin çözülebileceği garantidir ve en az hamle sayısını bilmek, uygulamanın bunu en iyi sonucunuzun yanında göstermesini sağlar.

## Bir seviye nasıl üretilir

- n renk ve sabit bir rastgele tohumla başlanır: n dolu şişe ve 2 boş şişe.
- Bir çözüm aranır. İlk prototip, 60.000 durumluk bir sınırı olan derinlik öncelikli arama kullandı.
- Arama, işe yaramayacak hamleleri atlar: zaten tamamlanmış bir şişeye dokunmak, boş şişelere birden fazla kez dökmek, tek misketli bir şişedeki misketi boş bir şişeye taşımak.
- Bir durum, şişelerin sıralanmış listesi olarak saklanır; böylece yalnızca şişe sırası farklı olan iki dizilim aynı sayılır.
- Sonra en az hamle sayısı bulunur: küçük seviyeler için genişlik öncelikli arama, büyükler için yinelemeli derinleşme.
- Çözülemeyen, baştan çözülmüş ya da fazla kolay olan seviyeler atılır. Kalanlar kolaydan zora sıralanır.

## Doğrulama

Plan, pakete dahil her seviyeyi yeniden çözen bir test içeriyor ve ilk oynanabilir sürüm en az 30 seviyeyi hedefliyordu. Tanıtım sayfası şu anda 150 diyor.
