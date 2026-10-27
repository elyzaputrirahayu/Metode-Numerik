import math

def f(x, pilihan):
    """Fungsi yang akan dicari akarnya."""
    fungsi = {
        "1": lambda x: x**3 - x - 2,
        "2": lambda x: x**2 - 4,
        "3": lambda x: math.cos(x) - x,
        "4": lambda x: x**3 - 2*x - 5,
    }
    return fungsi[pilihan](x)

def regular_falsi(pilihan, a, b, toleransi, maks_iterasi):
    fa = f(a, pilihan)
    fb = f(b, pilihan)

    if not all(math.isfinite(v) for v in (fa, fb)):
        raise ValueError("Nilai fungsi pada interval tidak valid.")
    if fa == 0:
        return a, [], "Akar tepat ditemukan pada batas bawah."
    if fb == 0:
        return b, [], "Akar tepat ditemukan pada batas atas."
    if fa * fb > 0:
        raise ValueError("f(a) dan f(b) harus berlainan tanda. Pilih interval yang mengurung akar.")

    tabel = []
    xr_lama = None

    for i in range(1, maks_iterasi + 1):
        penyebut = fb - fa
        if penyebut == 0:
            raise ZeroDivisionError("Penyebut nol; metode tidak dapat dilanjutkan.")

        xr = (a * fb - b * fa) / penyebut
        fr = f(xr, pilihan)
        galat = abs(xr - xr_lama) if xr_lama is not None else None

        tabel.append({
            "iterasi": i, "a": a, "b": b, "fa": fa, "fb": fb,
            "xr": xr, "fxr": fr, "galat": galat
        })

        if fr == 0 or (galat is not None and galat < toleransi):
            return xr, tabel, "Konvergen: toleransi terpenuhi atau akar tepat ditemukan."

        if fa * fr < 0:
            b, fb = xr, fr
        else:
            a, fa = xr, fr

        xr_lama = xr

    return xr, tabel, "Batas iterasi tercapai; hasil adalah pendekatan terakhir."

def main():
    print("=" * 66)
    print("             PROGRAM METODE REGULAR FALSI")
    print("=" * 66)
    print("Pilih fungsi:")
    print("1. f(x) = x^3 - x - 2")
    print("2. f(x) = x^2 - 4")
    print("3. f(x) = cos(x) - x")
    print("4. f(x) = x^3 - 2x - 5")

    pilihan = input("Masukkan pilihan (1-4): ").strip()
    if pilihan not in {"1", "2", "3", "4"}:
        print("Pilihan tidak valid.")
        return

    try:
        a = float(input("Masukkan batas bawah a: "))
        b = float(input("Masukkan batas atas b: "))
        toleransi = float(input("Masukkan toleransi (contoh 0.0001): "))
        maks_iterasi = int(input("Masukkan maksimum iterasi (contoh 100): "))

        if not all(math.isfinite(v) for v in (a, b, toleransi)):
            raise ValueError("Input harus berupa angka yang valid.")
        if a >= b:
            raise ValueError("Batas bawah a harus lebih kecil daripada batas atas b.")
        if toleransi <= 0:
            raise ValueError("Toleransi harus lebih besar dari 0.")
        if maks_iterasi < 1:
            raise ValueError("Maksimum iterasi minimal 1.")

        akar, tabel, status = regular_falsi(pilihan, a, b, toleransi, maks_iterasi)
        print("\n" + "-" * 108)
        print(f"{'Iter':>4} {'a':>12} {'b':>12} {'f(a)':>12} {'f(b)':>12} {'xr':>12} {'f(xr)':>12} {'Galat':>12}")
        print("-" * 108)
        for row in tabel:
            galat = "-" if row["galat"] is None else f'{row["galat"]:.6g}'
            print(f'{row["iterasi"]:>4} {row["a"]:>12.6f} {row["b"]:>12.6f} '
                  f'{row["fa"]:>12.6f} {row["fb"]:>12.6f} {row["xr"]:>12.6f} '
                  f'{row["fxr"]:>12.6f} {galat:>12}')
        print("-" * 108)
        print(f"\nPerkiraan akar : {akar:.10f}")
        print(f"f(akar)        : {f(akar, pilihan):.10g}")
        print(f"Jumlah iterasi : {len(tabel)}")
        print(f"Status         : {status}")
    except (ValueError, OverflowError, ZeroDivisionError) as e:
        print(f"\nTerjadi kesalahan input/perhitungan: {e}")

if __name__ == "__main__":
    main()
