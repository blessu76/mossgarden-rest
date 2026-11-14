---
title: "İlk TestFlight sürümü nasıl yüklendi"
description: "MVP bittikten sonra ilk dahili sürüm yüklendi, ancak dağıtım betiği yolda bizi bir kez durdurdu."
copy_review: iris 2026-11-14
---
iOS için bir idle oyun olan Moss Garden'ın ilk MVP'si, dağıtım betiği ilk denemeyi durdurduktan sonra dahili test için 1.0.0 (1) olarak TestFlight'a yüklendi. İşlenmesi yaklaşık üç dakika sürdü; sürüm incelemeye gönderilmedi ve harici test kullanıcılarına açılmadı.

## MVP'de neler vardı

İlk MVP sekiz bitki, çevrimdışı hesaplama, mevsimler, koleksiyon defteri, kaydetme ve ayarlarla ortaya çıktı. Ardından dahili test için 1.0.0 (1) olarak TestFlight'a yükledik. İşlenmesi yaklaşık üç dakika sürdü; incelemeye göndermedik ve harici test kullanıcılarına açmadık.

## İlk deneme başarısız oldu

Dağıtım betiği green gate'i çalıştırırken "yapı numarasını artırma" anlamına gelen bir ortam değişkeni testlere sızıp onları bozdu ve betik tam orada durdu. Bu duruş sayesinde hatalı bir sürüm yüklenmedi. Alt süreçlerin dıştaki ortamı miras almaması için düzeltmeyi yaptık, sonra yeniden yükledik.

Dağıtım zahmetli olabilir ama kuralımız değişmedi: testler yeşil değilse hiçbir şey yayına çıkmaz.

## SSS

### Moss Garden'ın ilk TestFlight sürümünde neler vardı?
Sekiz bitki, çevrimdışı hesaplama, mevsimler, koleksiyon defteri, kaydetme ve ayarlar; dahili test için 1.0.0 (1) olarak yüklendi.

### Moss Garden App Store incelemesine gönderildi mi?
Hayır. Bu sürüm yalnızca dahili test için yüklendi ve incelemeye göndermedik.
