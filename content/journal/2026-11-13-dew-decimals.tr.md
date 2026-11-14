---
title: "Çiyi neden ondalıklı gösteriyoruz"
description: "Yosun saniyede 0,1 büyüyor ama çiy sayacı donmuş gibiydi. Sayı biçimini böyle düzelttik."
---
Moss Garden, iOS için bir idle (artımlı) oyundur ve çiy sayacı, ondan itibaren yalnızca tam sayı gösterdiği için donmuş gibi görünüyordu. Artık 1'in altında iki, 1.000'in altında bir ondalık basamak gösteriyoruz ve sayı sahip olduğunuzdan fazlasını vadetmesin diye aşağı yuvarlıyoruz.

## Sayı neden donmuş gibiydi

Yosun saniyede 0,1 birikiyordu ama ekranın üstündeki çiy sayısı uzun süre aynı kalıyordu. Bir test kullanıcısı, sayacın saydığını hiç anlayamadığını söyledi. Neden basitti: ondan itibaren yalnızca tam sayı gösteriyorduk.

## Ne değiştirdik

1'in altındaki değerler artık iki, 1.000'in altındakiler bir ondalık basamakla görünüyor. Sondaki sıfırlar atılır; yani 289,0 değil 289 okursunuz.

Asıl karar yuvarlamaydı. 185,56'yı 185,6 olarak göstermek, henüz alamayacağınız bir şeyi alınabilir gibi gösterirdi. Bu yüzden **aşağı yuvarlıyoruz**: ekrandaki sayı en fazla gerçekte sahip olduğunuz kadardır.

Küçük bir değişiklik ama beklemek üzerine kurulu bir oyunda sayının ilerlediğini görmek ödülün bir parçası.

## SSS

### Moss Garden çiyi neden ondalıklı gösteriyor?
Yosun saniyede 0,1 büyüdüğü için ve tam sayılar sayacı donmuş gibi gösterdiği için. Ondalıklar sayacın saydığını görmenizi sağlar.

### Çiy sayısı yukarı mı aşağı mı yuvarlanır?
Aşağı. Ekrandaki sayı en fazla gerçekte sahip olduğunuz kadardır; böylece hiçbir şey vaktinden önce alınabilir görünmez.
