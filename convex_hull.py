import random  # Rastgele sayı/nokta üretimi için Python'un random modülü
import time  # Süre ölçümü için time modülü (perf_counter kullanacağız)
import math  # Trigonometrik fonksiyonlar (atan2) ve matematiksel işlemler için
import matplotlib.pyplot as plt  # Grafik çizimi: noktalar ve convex hull çizgileri


def nokta_uret(n, alt=0, ust=1000, seed=None):
    """
    n adet rastgele (x, y) noktası üretir.

    Parametreler:
    - n: kaç nokta üretilecek
    - alt, ust: koordinatlar [alt, ust] aralığında
    - seed: sabit tohum verilirse her çalıştırmada aynı noktalar üretilir

    Zaman: O(n) -> n kez randint + append
    """
    if seed is not None:
        random.seed(
            seed
        )  # Aynı seed ile aynı nokta kümesini üretmek için (adil karşılaştırma)

    noktalar = []  # Üretilen noktaları tutacağımız liste
    for _ in range(n):  # n kez döner -> O(n)
        x = random.randint(alt, ust)  # x koordinatı üret
        y = random.randint(alt, ust)  # y koordinatı üret
        noktalar.append((x, y))  # (x, y) noktasını listeye ekle

    return noktalar  # Üretilen nokta listesini döndür


def orientation(p, q, r):
    """
    p, q, r noktalarının dönüş yönünü belirler (2B çapraz çarpım işareti).

    Hesap: (q - p) x (r - p)
    - > 0: sol dönüş (counter-clockwise)
    - < 0: sağ dönüş (clockwise)
    - = 0: kolinear (aynı doğru üzerinde)

    Zaman: O(1)
    """
    # Aşağıdaki ifade, 2B determinanta karşılık gelir:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def uzaklik2(a, b):
    """
    İki nokta arasındaki ÖKLİD mesafesinin karesi.
    sqrt kullanmıyoruz -> karşılaştırma için yeterli ve daha hızlı.

    Zaman: O(1)
    """
    dx = a[0] - b[0]  # x farkı
    dy = a[1] - b[1]  # y farkı
    return dx * dx + dy * dy  # mesafe^2


def noktalari_ciz(noktalar, hull_kenarlar=None, baslik="Noktalar"):
    """
    Noktaları çizer; hull_kenarlar verilirse hull kenarlarını da çizer.
    Tema: koyu arkaplan + glow efektleri

    Zaman: O(n + E) (n: nokta sayısı, E: çizilecek kenar sayısı)
    """
    xs = [p[0] for p in noktalar]  # Tüm noktaların x koordinatları -> O(n)
    ys = [p[1] for p in noktalar]  # Tüm noktaların y koordinatları -> O(n)

    fig, ax = plt.subplots(figsize=(8.8, 5.6))  # Belirli boyutta figür ve eksen oluştur

    # --- Arkaplan teması ---
    fig.patch.set_facecolor("#0f172a")  # Figure (dış alan) arkaplan rengi
    ax.set_facecolor("#111827")  # Grafik çizim alanı arkaplan rengi

    # Hafif ızgara: okuma kolaylığı için
    ax.grid(True, linestyle=":", linewidth=0.8, alpha=0.25, color="#e5e7eb")

    # Noktalar: iki katmanlı çizim
    ax.scatter(
        xs,
        ys,
        s=55,  # glow boyutu (büyük)
        c="#93c5fd",  # glow rengi
        alpha=0.10,  # glow saydamlık
        edgecolors="none",
        zorder=2,  # çizim katmanı
    )
    ax.scatter(
        xs,
        ys,
        s=18,  # ana nokta boyutu
        c="#60a5fa",  # ana nokta rengi
        alpha=0.85,  # ana nokta saydamlığı
        edgecolors="#0b1220",  # nokta kenarlık rengi
        linewidths=0.3,
        zorder=3,
    )

    # Hull çizgileri
    if hull_kenarlar is not None:
        for a, b in hull_kenarlar:  # Her kenar iki noktadan oluşur
            # Önce glow çizgisi (kalın, saydam)
            ax.plot(
                [a[0], b[0]],
                [a[1], b[1]],
                linewidth=5.5,
                alpha=0.12,
                color="#f59e0b",
                zorder=4,
            )
            # Sonra ana çizgi (daha ince, daha opak)
            ax.plot(
                [a[0], b[0]],
                [a[1], b[1]],
                linewidth=2.2,
                alpha=0.95,
                color="#fbbf24",
                zorder=5,
            )

    # Başlık ve etiketler: koyu temada okunması için açık renk
    ax.set_title(baslik, fontsize=13, color="#f9fafb", pad=12)
    ax.set_xlabel("x", color="#e5e7eb")
    ax.set_ylabel("y", color="#e5e7eb")

    # Eksen üzerindeki sayıların rengini değiştir
    ax.tick_params(colors="#e5e7eb")

    # Grafik çerçevelerini yumuşat (açık renk, düşük alfa)
    for spine in ax.spines.values():
        spine.set_alpha(0.25)
        spine.set_color("#e5e7eb")

    # Legend (açıklama kutusu) oluşturmak için Line2D kullanıyoruz
    from matplotlib.lines import Line2D  # Legend için özel öğeler

    legend_items = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            label="Noktalar",
            markerfacecolor="#60a5fa",
            markeredgecolor="#0b1220",
            markersize=8,
        ),
        Line2D([0], [0], color="#fbbf24", lw=2.2, label="Convex Hull"),
    ]

    ax.legend(
        handles=legend_items,
        loc="upper right",
        frameon=True,
        facecolor="#0b1220",
        edgecolor="#334155",
        labelcolor="#f9fafb",
    )

    plt.tight_layout()  # Kenar boşluklarını otomatik ayarla
    plt.show()  # Grafiği ekrana bas


def _collinear_endpoint_filter(p, q, noktalar):
    """
    KOLİNEAR (aynı doğru üstü) durumlarda gereksiz 'iç' segmentleri elemek için.

    Amaç:
    - Brute force kenar adayları içinde, aynı doğru üstünde birden çok nokta olabilir.
    - Hull kenarı, o doğru üzerindeki EN UÇTAKİ iki nokta arasında olmalıdır.
    - p-q o doğrultuda uç noktalar değilse bu segment içte kalır -> elenir.

    Zaman: O(n)
    """
    dx = q[0] - p[0]  # doğrultu vektörü x bileşeni
    dy = q[1] - p[1]  # doğrultu vektörü y bileşeni

    if dx == 0 and dy == 0:
        return False  # p ve q aynı nokta ise geçersiz

    # Bir noktayı doğrultuya projekte etmek için skaler değer
    def proj(t):
        return t[0] * dx + t[1] * dy  # dot((t), (dx,dy)) gibi düşün

    min_val = None  # doğrultu üzerindeki en küçük projeksiyon
    max_val = None  # doğrultu üzerindeki en büyük projeksiyon

    pproj = proj(p)  # p'nin projeksiyonu
    qproj = proj(q)  # q'nun projeksiyonu

    for r in noktalar:  # tüm noktalar içinde dolaş -> O(n)
        if orientation(p, q, r) == 0:  # r, p-q doğrusu üzerinde mi?
            v = proj(r)  # r'nin projeksiyonu
            if min_val is None or v < min_val:
                min_val = v  # minimumu güncelle
            if max_val is None or v > max_val:
                max_val = v  # maksimumu güncelle

    # p ve q, bu doğru üzerindeki uçlarda olmalı (min ve max projeksiyon)
    return (pproj == min_val and qproj == max_val) or (
        pproj == max_val and qproj == min_val
    )


def brute_force_hull_edges(noktalar):
    """
    BRUTE FORCE CONVEX HULL (kenar bulma)

    Mantık:
    - Her (p, q) çiftini aday kenar kabul et
    - Diğer tüm noktalar bu doğru parçasının aynı tarafında mı kontrol et
    - Eğer hepsi tek tarafta ise p-q bir hull kenarı olabilir

    i-j-k üçlü döngü -> teorik O(n^3)

    Not:
    - Koliner fazlalıklar için _collinear_endpoint_filter ile iç segmentleri eliyoruz.
    """
    n = len(noktalar)  # nokta sayısı
    kenarlar = []  # bulunan hull kenar adayları

    for i in range(n):  # dış döngü -> O(n)
        p = noktalar[i]  # i. nokta
        for j in range(i + 1, n):  # ikinci döngü -> O(n)
            q = noktalar[j]  # j. nokta

            sol_var = False  # doğru parçasının solunda nokta var mı?
            sag_var = False  # doğru parçasının sağında nokta var mı?

            for k in range(n):  # üçüncü döngü -> O(n)
                if k == i or k == j:
                    continue  # p ve q'nun kendisini kontrol etmeyelim
                r = noktalar[k]  # kontrol edilen üçüncü nokta
                val = orientation(p, q, r)  # r, p-q'ya göre hangi tarafta? -> O(1)

                if val > 0:
                    sol_var = True
                elif val < 0:
                    sag_var = True

                # Eğer hem sağda hem solda noktalar varsa p-q dış sınır olamaz
                if sol_var and sag_var:
                    break  # erken çıkış (worst-case yine O(n))

            # Eğer tüm noktalar tek tarafta kaldıysa aday kenar
            if not (sol_var and sag_var):
                # Koliner noktalar için uç segment filtresi -> O(n)
                if _collinear_endpoint_filter(p, q, noktalar):
                    kenarlar.append((p, q))

    return kenarlar  # bulunan kenar adaylarını döndür


def brute_force_edges_to_polygon(kenarlar):
    """
    Brute force kenar listesini, "kapalı poligon" çizilebilecek hale getirir.

    Yaklaşım:
    - Kenarlardan unique hull noktalarını çıkar
    - Ağırlık merkezi (centroid) etrafında açıya göre sırala
    - Ardışık noktaları birleştirip kapanışı ekle

    Zaman: O(h log h) (h = hull üzerindeki nokta sayısı)
    """
    if not kenarlar:
        return []  # kenar yoksa poligon yok

    noktalar = set()  # tekrarları önlemek için set
    for a, b in kenarlar:  # O(E)
        noktalar.add(a)
        noktalar.add(b)

    hull_pts = list(noktalar)  # set -> liste
    if len(hull_pts) < 2:
        return []

    # centroid hesapla (sıralama için referans)
    cx = sum(p[0] for p in hull_pts) / len(hull_pts)
    cy = sum(p[1] for p in hull_pts) / len(hull_pts)

    def angle_key(p):
        # centroid'e göre açı: noktaları saat yönünde/tersinde sıraya sokar
        return math.atan2(p[1] - cy, p[0] - cx)

    hull_pts.sort(key=angle_key)  # O(h log h) açıya göre sırala

    poly_edges = []  # kapalı poligon kenarları
    for i in range(len(hull_pts)):  # O(h)
        a = hull_pts[i]
        b = hull_pts[(i + 1) % len(hull_pts)]  # son noktadan sonra ilk noktaya bağla
        poly_edges.append((a, b))

    return poly_edges  # çizim için uygun kenar listesi


def graham_scan_hull(noktalar):
    """
    GRAHAM SCAN CONVEX HULL

    Adımlar:
    1) pivot seç (en küçük y, eşitse en küçük x) -> O(n)
    2) diğer noktaları pivot'a göre açıyla sırala -> O(n log n)
    3) aynı açıdaki noktaları düzelt -> O(n)
    4) stack ile sağ dönüşleri ele -> amortize O(n)

    Toplam: O(n log n)
    """
    n = len(noktalar)
    if n <= 1:
        return noktalar[:]  # 0 veya 1 nokta hull'un kendisidir

    pivot = min(noktalar, key=lambda p: (p[1], p[0]))  # O(n)

    digerleri = [p for p in noktalar if p != pivot]  # pivot dışındakiler -> O(n)

    def siralama_anahtari(p):
        # atan2 ile açı + mesafe^2 ile aynı açıdaki noktaları ayırt et
        return (
            math.atan2(p[1] - pivot[1], p[0] - pivot[0]),
            uzaklik2(pivot, p),
        )

    digerleri.sort(key=siralama_anahtari)  # O(n log n)

    # Aynı açıdaki noktalar için en uzaktakini tut
    temiz = []
    i = 0
    while i < len(digerleri):  # O(n)
        j = i
        while (
            j + 1 < len(digerleri)
            and orientation(pivot, digerleri[j], digerleri[j + 1]) == 0
        ):
            j += 1
        temiz.append(digerleri[j])  # aynı açıda en uzaktaki (sonda kalan) tutulur
        i = j + 1

    # hull noktalarını tutan stack
    stack = [pivot]

    for p in temiz:  # O(n)
        stack.append(p)  # yeni noktayı ekle

        # Son 3 nokta sağ dönüş/kolinear ise ortadaki hull'da olamaz
        while len(stack) >= 3 and orientation(stack[-3], stack[-2], stack[-1]) <= 0:
            del stack[-2]  # ortadakini çıkar  O(1)

    return stack  # hull noktaları sırayla


def hull_noktalardan_kenara(hull_noktalar):
    """
    Hull noktalarını, çizim için kenarlara çevirir.
    (A0->A1, A1->A2, ..., A_last->A0)

    Zaman: O(h)
    """
    if len(hull_noktalar) < 2:
        return []

    kenarlar = []
    for i in range(len(hull_noktalar)):  # O(h)
        a = hull_noktalar[i]
        b = hull_noktalar[(i + 1) % len(hull_noktalar)]
        kenarlar.append((a, b))

    return kenarlar


def _median(lst):
    """
    Liste elemanlarının medyanını alır.
    Tekrar ölçümlerde gürültüyü azaltmak için kullanıyoruz.

    Zaman: O(k log k) (k = tekrar sayısı, küçük olduğu için sorun değil)
    """
    s = sorted(lst)  # sıralama
    m = len(s) // 2  # orta indeks
    if len(s) % 2 == 1:  # tek sayıda eleman
        return s[m]
    return 0.5 * (s[m - 1] + s[m])  # çift sayıda elemanda ortalama


def performans_testi(time_limit_bf=2.0, tekrar=3, seed=42):
    """
    Performans karşılaştırması:
    - Her N için:
        Graham Scan süresi
        Brute Force süresi (2 saniyeyi aşarsa 'pratik değil' -> None)

    time_limit_bf:
    - Brute Force çok yavaşladığında bilgisayarı kilitlemesin diye sınır
    """
    N_list = [10, 500, 1000, 2000, 5000]  # test edilecek nokta sayıları

    bf_sureler = []  # brute force süreleri (None olabilir)
    gs_sureler = []  # graham scan süreleri
    bf_koptugu_N = None  # BF'nin ilk kez pratik olmadığı N

    for N in N_list:
        # Her N için aynı seed ile nokta üret -> algoritmalar aynı veri üzerinde koşar
        noktalar = nokta_uret(N, alt=0, ust=1000, seed=seed)

        # --- Graham Scan ölçümü (tekrar ile median) ---
        gs_runs = []
        for _ in range(tekrar):
            t0 = time.perf_counter()  # başlangıç zamanı
            hull = graham_scan_hull(noktalar)  # hull hesapla
            _ = hull_noktalardan_kenara(hull)  # kenara çevir (çizime benzer iş yükü)
            t1 = time.perf_counter()  # bitiş zamanı
            gs_runs.append(t1 - t0)  # bu ölçümü listeye ekle

        gs = _median(gs_runs)  # medyan süre (daha stabil)
        gs_sureler.append(gs)  # sonuç listesine ekle

        # --- Brute Force ölçümü (tekrar + time_limit) ---
        bf_runs = []
        bf_pratik = True

        for _ in range(tekrar):
            t0 = time.perf_counter()
            _ = brute_force_hull_edges(noktalar)  # BF ile kenarları bul
            t1 = time.perf_counter()

            dt = t1 - t0  # geçen süre
            if dt > time_limit_bf:
                bf_pratik = False  # pratik değil
                break  # tekrar denemeyi bırak
            bf_runs.append(dt)

        # Eğer pratik değilse None yaz
        if (not bf_pratik) or (len(bf_runs) == 0):
            if bf_koptugu_N is None:
                bf_koptugu_N = N  # BF'nin ilk koptuğu N
            bf_sureler.append(None)
        else:
            bf_sureler.append(_median(bf_runs))  # median süreyi ekle

        # Terminalde özet yazdır
        print(f"N={N:5d} | BF: {bf_sureler[-1]} | GS: {gs_sureler[-1]:.6f}")

    # --- Grafik ---
    fig, ax = plt.subplots(figsize=(9.2, 5.6))  # figür+eksen

    fig.patch.set_facecolor("#0b1020")  # dış arkaplan
    ax.set_facecolor("#0f172a")  # grafik alanı arkaplan

    ax.grid(True, linestyle="--", alpha=0.25, color="#cbd5e1")  # grid

    # Graham Scan çizgisi
    ax.plot(
        N_list,
        gs_sureler,
        marker="o",
        markersize=7,
        linewidth=2.6,
        label="Graham Scan",
        color="#22c55e",
    )

    # Brute Force: None olmayanları çizmek için filtrele
    bf_x, bf_y = [], []
    for i, s in enumerate(bf_sureler):
        if s is not None:
            bf_x.append(N_list[i])
            bf_y.append(s)

    # Brute Force çizgisi (eğer çizilecek veri varsa)
    if bf_x:
        ax.plot(
            bf_x,
            bf_y,
            marker="s",
            markersize=7,
            linewidth=2.6,
            label="Brute Force",
            color="#ef4444",
        )

    # BF pratik değil çizgisi + anotasyon
    if bf_koptugu_N is not None:
        ax.axvline(
            bf_koptugu_N, linestyle=":", linewidth=2.0, color="#fbbf24", alpha=0.95
        )
        ax.annotate(
            f"BF pratik değil\nN={bf_koptugu_N}",
            xy=(bf_koptugu_N, max(gs_sureler)),
            xytext=(bf_koptugu_N + (max(N_list) * 0.05), max(gs_sureler) * 2.2),
            arrowprops=dict(arrowstyle="->", color="#fbbf24", lw=1.5),
            color="#fde68a",
            fontsize=10,
        )

    # GS noktalarının üzerine süre yaz
    for x, y in zip(N_list, gs_sureler):
        ax.text(
            x, y, f"{y:.4f}s", fontsize=8.5, color="#bbf7d0", ha="left", va="bottom"
        )

    # BF noktalarının üzerine süre yaz (None olmayanlar)
    for x, y in zip(bf_x, bf_y):
        ax.text(
            x, y, f"{y:.3f}s", fontsize=8.5, color="#fecaca", ha="left", va="bottom"
        )

    ax.set_title("Performans Karşılaştırması", fontsize=13, color="#f8fafc", pad=12)
    ax.set_xlabel("N (nokta sayısı)", color="#e2e8f0")
    ax.set_ylabel("Çalışma süresi (saniye)", color="#e2e8f0")
    ax.tick_params(colors="#e2e8f0")  # tick renkleri

    # Çerçeve renk/şeffaflık ayarı
    for spine in ax.spines.values():
        spine.set_alpha(0.30)
        spine.set_color("#e2e8f0")

    # Legend
    leg = ax.legend(loc="upper left", frameon=True)
    leg.get_frame().set_facecolor("#0b1020")
    leg.get_frame().set_edgecolor("#334155")
    for text in leg.get_texts():
        text.set_color("#f8fafc")

    plt.tight_layout()  # düzenle
    plt.savefig("performans_grafik.png", dpi=240)  # dosyaya kaydet
    plt.show()  # göster


if __name__ == "__main__":
    # Program doğrudan çalıştırıldığında burası çalışır
    N = 100  # PDF'de istenen temel gösterim: 100 nokta
    noktalar = nokta_uret(N, alt=0, ust=1000, seed=42)  # 100 nokta üret

    # Kullanıcı menü seçimi (CLI)
    secim = input(
        "1: Sadece noktalar\n"
        "2: Brute Force Hull (poligon)\n"
        "3: Graham Scan Hull\n"
        "4: Performans Testi (grafik)\n"
        "Secim: "
    ).strip()  # baştaki/sondaki boşlukları temizle

    if secim == "1":
        # Sadece noktaları çiz
        noktalari_ciz(noktalar, baslik=f"{N} ADET NOKTA (Noktalar)")

    elif secim == "2":
        # Brute force ile hull kenarlarını bul + poligonlaştır + çiz
        t0 = time.perf_counter()  # süre ölçümü başlangıç
        kenarlar = brute_force_hull_edges(noktalar)  # BF kenarları
        poligon_kenarlar = brute_force_edges_to_polygon(kenarlar)  # poligon kenarları
        t1 = time.perf_counter()  # süre ölçümü bitiş

        print(
            f"Brute Force süre: {t1 - t0:.6f} saniye | "
            f"Aday kenar: {len(kenarlar)} | "
            f"Poligon kenar: {len(poligon_kenarlar)}"
        )

        noktalari_ciz(
            noktalar,
            hull_kenarlar=poligon_kenarlar,
            baslik=f"Brute Force Convex Hull (Poligon) (N={N})",
        )

    elif secim == "3":
        # Graham Scan ile hull bul + kenara çevir + çiz
        t0 = time.perf_counter()
        hull = graham_scan_hull(noktalar)  # hull noktaları
        kenarlar = hull_noktalardan_kenara(hull)  # kenarlar
        t1 = time.perf_counter()

        print(
            f"Graham Scan süre: {t1 - t0:.6f} saniye | "
            f"Hull nokta sayısı: {len(hull)}"
        )

        noktalari_ciz(
            noktalar, hull_kenarlar=kenarlar, baslik=f"Graham Scan Convex Hull (N={N})"
        )

    elif secim == "4":
        # Performans testi (grafik üretir)
        performans_testi(time_limit_bf=2.0, tekrar=3, seed=42)

    else:
        # Geçersiz seçim kontrolü
        print("Geçersiz seçim.")
