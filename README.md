# convex_hull
Kaba Kuvvet ve Graham Scan algoritmaları ile Convex Hull probleminin teorik ve deneysel analizi
# Convex Hull Problemi — Brute Force ve Graham Scan Analizi

Bu proje, Algoritma Analizi ve Tasarım dersi kapsamında geliştirilmiş olup **Convex Hull (Kapalı Çevrim)** probleminin iki farklı algoritmik yöntemle çözümünü ve performans karşılaştırmasını içermektedir.

Projede:

- **Brute Force (Kaba Kuvvet)**
- **Graham Scan**

algoritmaları teorik ve deneysel olarak analiz edilmiştir.

---

## 📌 Convex Hull Problemi Nedir?

Convex Hull problemi, düzlem üzerindeki bir nokta kümesini çevreleyen en küçük dış sınırın (kapalı çevrim) bulunması problemidir.

Bu sınır, noktaların oluşturduğu geometrik yapının dış kabuğunu temsil eder.

---

## 🧠 Kullanılan Algoritmalar

### 1. Kaba Kuvvet (Brute Force)

Brute Force yaklaşımında tüm nokta çiftleri `(p, q)` seçilir ve bu iki noktadan geçen doğrunun diğer tüm noktaları aynı tarafta bırakıp bırakmadığı kontrol edilir.

Eğer tüm noktalar doğrunun tek tarafında kalıyorsa, bu kenar Convex Hull’a ait kabul edilir.

#### Kullanılan Yöntemler

- Orientation (sağ/sol dönüş) testi
- Üç iç içe döngü ile tüm kombinasyonların denenmesi

#### Zaman Karmaşıklığı

\[
O(N^3)
\]

Bu nedenle nokta sayısı arttıkça çalışma süresi çok hızlı yükselir ve büyük veri kümelerinde verimsiz hale gelir.

---

### 2. Graham Scan Algoritması

Graham Scan algoritması daha verimli bir Convex Hull yöntemidir.

#### Çalışma Mantığı

1. En küçük `y` koordinatına sahip nokta pivot seçilir.
2. Diğer noktalar pivot noktasına göre açıya göre sıralanır.
3. Stack (yığın) yapısı kullanılarak sağ dönüş yapan noktalar elenir.
4. Dış sınır noktaları elde edilir.

#### Zaman Karmaşıklığı

En maliyetli adım sıralama olduğundan:

\[
O(N \log N)
\]

Bu algoritma büyük veri kümelerinde bile hızlı ve pratik sonuçlar üretir.

---

## 📊 Performans Karşılaştırması

Projede her iki algoritma farklı büyüklüklerde rastgele nokta kümeleri üzerinde test edilmiştir.

### Gözlemler

- Brute Force algoritmasının çalışma süresi nokta sayısı arttıkça çok hızlı artmaktadır.
- Graham Scan algoritmasının çalışma süresi daha kontrollü ve düşük seviyede kalmaktadır.

Bu sonuçlar teorik karmaşıklık analizleriyle birebir uyumludur.

---

## 📂 Proje İçeriği

Projede aşağıdaki işlemler gerçekleştirilmiştir:

- Rastgele nokta üretimi
- Brute Force Convex Hull çözümü
- Graham Scan Convex Hull çözümü
- Performans testi ve süre ölçümü
- Grafiksel karşılaştırma

---

## 🛠️ Kullanılan Teknolojiler

Python
Matplotlib (grafik çizimi)
Math kütüphanesi (atan2)
Stack veri yapısı

---

## 📈 Çıktılar

Program çalıştırıldığında:

Convex Hull görselleştirmeleri
Brute Force ve Graham Scan süre karşılaştırmaları
Performans grafikleri
üretilmektedir.

---

## 📌 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
