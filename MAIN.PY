"""Aplikasi Study Log sederhana
- Menyimpan catatan belajar ke dalam list `catatan` (list of dict)
- Fungsi: tambah_catatan(), tampilkan_catatan(), dan menu CLI sederhana
"""

catatan = []  # list untuk menyimpan catatan. Setiap catatan adalah dict sederhana

# Target harian (menit). None berarti belum diatur
target_harian = None


def tambah_catatan():
    """Minta input mapel, topik, dan durasi (menit), lalu simpan ke list `catatan`."""
    mapel = input("Masukkan mata pelajaran: ").strip()
    topik = input("Masukkan topik: ").strip()

    # Validasi agar durasi berupa integer > 0
    while True:
        durasi_str = input("Masukkan durasi belajar (menit): ").strip()
        try:
            durasi = int(durasi_str)
            if durasi <= 0:
                print("Durasi harus lebih dari 0. Coba lagi.")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat untuk durasi (mis. 45).")

    catatan.append({
        "mapel": mapel,
        "topik": topik,
        "durasi_menit": durasi,
    })

    print(f"✅ Catatan ditambahkan: {mapel} — {topik} ({durasi} menit)")


def total_waktu():
    """Menghitung total durasi belajar (menit) dari semua catatan.

    Mengembalikan jumlah durasi dalam satuan menit (int).
    """
    return sum(c.get('durasi_menit', 0) for c in catatan)


def set_target_harian():
    """Mengatur target harian (menit). Masukkan angka bulat > 0."""
    while True:
        s = input("Masukkan target harian (menit), atau kosong untuk batal: ").strip()
        if s == "":
            print("Batal. Target tidak diubah.")
            return
        try:
            t = int(s)
            if t <= 0:
                print("Target harus lebih dari 0. Coba lagi.")
                continue
            global target_harian
            target_harian = t
            print(f"✅ Target harian diset: {t} menit")
            return
        except ValueError:
            print("Masukkan angka bulat untuk target (mis. 60).")


def lihat_target_harian():
    """Menampilkan target harian bila sudah diatur."""
    if target_harian is None:
        print("Target harian belum diatur.")
    else:
        print(f"Target harian: {target_harian} menit")


def lihat_catatan():
    """Menampilkan semua catatan dalam tabel monospace yang rapi dan menarik."""
    if not catatan:
        print("Belum ada catatan.")
        if target_harian is not None:
            print(f"Target harian: {target_harian} menit")
        return

    # header dan lebar kolom
    headers = ["No", "Mata Pelajaran", "Topik", "Durasi (menit)"]
    no_w = max(len(headers[0]), len(str(len(catatan))))
    mapel_w = max(len(headers[1]), max((len(c['mapel']) for c in catatan), default=0))
    topik_w = max(len(headers[2]), max((len(c['topik']) for c in catatan), default=0))
    dur_w = max(len(headers[3]), max((len(str(c['durasi_menit'])) for c in catatan), default=0))

    # garis kotak (menggunakan karakter box-drawing unicode)
    top = '┌' + '─'*(no_w+2) + '┬' + '─'*(mapel_w+2) + '┬' + '─'*(topik_w+2) + '┬' + '─'*(dur_w+2) + '┐'
    mid = '├' + '─'*(no_w+2) + '┼' + '─'*(mapel_w+2) + '┼' + '─'*(topik_w+2) + '┼' + '─'*(dur_w+2) + '┤'
    bottom = '└' + '─'*(no_w+2) + '┴' + '─'*(mapel_w+2) + '┴' + '─'*(topik_w+2) + '┴' + '─'*(dur_w+2) + '┘'

    # cetak header tabel
    print("\nDaftar catatan:")
    print(top)
    print(f"│ {'No'.ljust(no_w)} │ {'Mata Pelajaran'.ljust(mapel_w)} │ {'Topik'.ljust(topik_w)} │ {'Durasi (menit)'.rjust(dur_w)} │")
    print(mid)

    # isi tabel
    for i, c in enumerate(catatan, start=1):
        print(f"│ {str(i).ljust(no_w)} │ {c['mapel'].ljust(mapel_w)} │ {c['topik'].ljust(topik_w)} │ {str(c['durasi_menit']).rjust(dur_w)} │")

    # footer
    print(bottom)

    # ringkasan
    total = total_waktu()
    print(f"Total durasi: {total} menit")

    # progress terhadap target
    if target_harian is not None:
        remaining = max(0, target_harian - total)
        percent = min(100, int((total / target_harian) * 100)) if target_harian > 0 else 0
        status = "tercapai" if total >= target_harian else "belum tercapai"
        # tampilkan progress dalam bar sederhana (20 char)
        bar_len = 20
        filled = int(bar_len * percent / 100)
        bar = '█' * filled + '-' * (bar_len - filled)
        print(f"Target harian: {target_harian} menit — {percent}% ({status})")
        print(f"Progress: |{bar}| Sisa: {remaining} menit")

    # Tampilkan progress terhadap target jika terpasang
    if target_harian is not None:
        remaining = target_harian - total
        status = "tercapai" if total >= target_harian else "belum tercapai"
        percent = min(100, int((total / target_harian) * 100)) if target_harian > 0 else 0
        print(f"Target harian: {target_harian} menit — {percent}% ({status}). Sisa: {max(0, remaining)} menit")



def tampilkan_catatan():
    """Alias untuk melihat catatan — tetap kompatibel dengan versi lama."""
    lihat_catatan()


def main():
    """Menu sederhana untuk menambah dan melihat catatan serta mengatur target harian."""
    while True:
        print("\nMenu:")
        print("1. Tambah catatan")
        print("2. Tampilkan catatan")
        print("3. Keluar")
        print("4. Set target harian")
        print("5. Lihat target harian")
        pilihan = input("Pilih (1/2/3/4/5): ").strip()

        if pilihan == "1":
            tambah_catatan()
        elif pilihan == "2":
            tampilkan_catatan()
        elif pilihan == "3":
            print("Sampai jumpa!")
            break
        elif pilihan == "4":
            set_target_harian()
        elif pilihan == "5":
            lihat_target_harian()
        else:
            print("Pilihan tidak valid. Coba lagi.")


if __name__ == "__main__":
    main()
