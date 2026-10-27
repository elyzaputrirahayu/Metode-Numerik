TUGAS METODE NUMERIK — REGULAR FALSI

Isi:
- index.php: aplikasi web, kalkulasi PHP, tabel iterasi
- style.css: tampilan elegan navy, putih, aksen gold
- script.js: validasi input dan unduh tabel CSV
- RegularFalsi.java: implementasi algoritma Regular Falsi di terminal

MENJALANKAN WEB:
1. Ekstrak ZIP.
2. Pastikan PHP terpasang (misalnya melalui Laragon).
3. Buka terminal di folder yang berisi index.php.
4. Jalankan: php -S localhost:8000
5. Buka http://localhost:8000

MENJALANKAN JAVA:
1. Pastikan JDK terpasang.
2. Buka terminal di folder proyek.
3. Jalankan: javac RegularFalsi.java
4. Jalankan: java RegularFalsi

CONTOH UJI:
Fungsi x^3 - x - 2; a=1; b=2; toleransi=0.0001; iterasi=100.
Akar pendekatan sekitar 1.5214.

Catatan: fungsi dipilih melalui dropdown/menu agar input fungsi tidak dieksekusi sebagai kode.
Versi web memakai PHP untuk kalkulasi, CSS untuk desain, dan JavaScript untuk validasi/ekspor.
Versi Java merupakan implementasi algoritma terpisah untuk dijalankan di terminal.
