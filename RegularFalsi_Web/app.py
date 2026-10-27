from flask import Flask, request, render_template_string
import math
import csv
import io

app = Flask(__name__)

FUNCTIONS = {
    "1": {"label": "f(x) = x³ − x − 2", "fn": lambda x: x**3 - x - 2},
    "2": {"label": "f(x) = x² − 4", "fn": lambda x: x**2 - 4},
    "3": {"label": "f(x) = cos(x) − x", "fn": lambda x: math.cos(x) - x},
    "4": {"label": "f(x) = x³ − 2x − 5", "fn": lambda x: x**3 - 2*x - 5},
}

PAGE = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Regular Falsi | Metode Numerik</title>
<style>
:root{--navy:#651b3d;--navy2:#8b2d52;--gold:#e8a0b8;--ink:#382331;--muted:#8c7180;--paper:#fff5f8;--line:#f0dce4;--white:#fff;--red:#a12d57;--green:#7b294d}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,Segoe UI,Arial,sans-serif}
header{background:linear-gradient(125deg,var(--navy),var(--navy2));color:white;padding:34px 20px 68px;border-bottom:5px solid var(--gold)}
.wrap{max-width:1120px;margin:auto;padding:0 18px}.eyebrow{text-transform:uppercase;letter-spacing:3px;font-size:11px;color:var(--gold);font-weight:800}
h1{font-size:clamp(28px,5vw,42px);margin:12px 0 8px;letter-spacing:-1px}.sub{color:#f4dfe8;max-width:650px;line-height:1.65;margin:0}
main{margin-top:-38px;padding-bottom:44px}.layout{display:grid;grid-template-columns:340px minmax(0,1fr);gap:20px;align-items:start}
.card{background:var(--white);border:1px solid var(--line);border-radius:18px;box-shadow:0 12px 32px #651b3d0c;padding:22px}
h2{font-size:17px;margin:0 0 18px;color:var(--navy)}label{display:block;font-size:12px;font-weight:800;color:#755564;margin:14px 0 7px}
select,input{width:100%;border:1px solid #ead6df;border-radius:10px;padding:12px 13px;font:inherit;background:#fff;color:var(--ink);outline:none}
select:focus,input:focus{border-color:var(--gold);box-shadow:0 0 0 3px #e8a0b82b}
button,.download{display:inline-flex;justify-content:center;align-items:center;background:var(--navy);color:white;border:0;border-radius:10px;padding:12px 15px;font-weight:800;cursor:pointer;text-decoration:none}
button:hover,.download:hover{background:var(--navy2)}.primary{width:100%;margin-top:20px;border-bottom:3px solid var(--gold)}
.note{font-size:12px;color:var(--muted);line-height:1.6;margin-top:14px}
.formula{background:#fff2f6;border:1px solid #f1d5e0;padding:14px;border-radius:12px;font-family:Georgia,serif;text-align:center;font-size:17px;margin:14px 0}
.error{background:#fff0f5;border:1px solid #f0cbd9;color:var(--red);padding:13px;border-radius:11px;margin-bottom:14px}
.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:16px}
.metric{background:#fff9fb;border:1px solid var(--line);border-radius:12px;padding:13px;min-width:0}.metric span{display:block;color:var(--muted);font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.5px}.metric strong{display:block;color:var(--navy);font-size:18px;overflow-wrap:anywhere;margin-top:7px}
.status{font-size:13px;color:var(--green);background:#fceaf1;padding:10px 12px;border-radius:9px;margin-bottom:14px}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:12px}table{border-collapse:collapse;width:100%;min-width:720px;font-size:12px}th{background:var(--navy);color:white;text-align:right;padding:12px 10px;white-space:nowrap}td{text-align:right;padding:10px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums;white-space:nowrap}td:first-child,th:first-child{text-align:center}tbody tr:nth-child(even){background:#fff8fb}tbody tr:last-child td{border-bottom:0}.table-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin:20px 0 10px}.table-head h2{margin:0}.small{font-size:12px;color:var(--muted)}footer{text-align:center;padding:22px;color:var(--muted);font-size:12px}
@media(max-width:850px){.layout{grid-template-columns:1fr}.metrics{grid-template-columns:1fr}.metric strong{font-size:16px}header{padding-bottom:60px}}
</style>
</head>
<body>
<header><div class="wrap"><div class="eyebrow">Metode Numerik · Python</div><h1>Regular Falsi</h1><p class="sub">Kalkulator pencarian akar persamaan menggunakan metode posisi palsu, lengkap dengan tabel iterasi dan estimasi galat.</p></div></header>
<main class="wrap"><div class="layout">
<section class="card">
<h2>Parameter Perhitungan</h2>
<form method="post">
<label for="fungsi">Fungsi f(x)</label>
<select id="fungsi" name="fungsi">
{% for key,item in functions.items() %}<option value="{{key}}" {% if selected == key %}selected{% endif %}>{{item.label}}</option>{% endfor %}
</select>
<label for="a">Batas bawah (a)</label><input id="a" name="a" type="number" step="any" value="{{a}}" required>
<label for="b">Batas atas (b)</label><input id="b" name="b" type="number" step="any" value="{{b}}" required>
<label for="tol">Toleransi galat</label><input id="tol" name="tol" type="number" step="any" min="0.000000000001" value="{{tol}}" required>
<label for="maks">Maksimum iterasi</label><input id="maks" name="maks" type="number" min="1" max="10000" step="1" value="{{maks}}" required>
<button class="primary" type="submit">Hitung Akar →</button>
</form>
<div class="formula">xᵣ = (a·f(b) − b·f(a)) / (f(b) − f(a))</div>
<p class="note">Syarat interval: f(a) dan f(b) harus berlainan tanda, kecuali salah satu batas sudah merupakan akar. Fungsi cos(x) menggunakan radian.</p>
</section>
<section class="card">
{% if error %}<div class="error"><strong>Perhitungan belum dapat dilakukan</strong><br>{{error}}</div>{% endif %}
{% if result %}
<h2>Hasil Perhitungan</h2>
<div class="metrics">
<div class="metric"><span>Perkiraan akar</span><strong>{{ "%.10f"|format(result.root) }}</strong></div>
<div class="metric"><span>Nilai f(akar)</span><strong>{{ "%.4e"|format(result.froot) }}</strong></div>
<div class="metric"><span>Jumlah iterasi</span><strong>{{result.rows|length}}</strong></div>
</div>
<div class="status">{{result.status}}</div>
<div class="table-head"><h2>Tabel Iterasi</h2><a class="download" href="/download?fungsi={{selected}}&a={{a}}&b={{b}}&tol={{tol}}&maks={{maks}}">Ekspor CSV ↓</a></div>
<div class="table-wrap"><table><thead><tr><th>Iterasi</th><th>a</th><th>b</th><th>f(a)</th><th>f(b)</th><th>xᵣ</th><th>f(xᵣ)</th><th>Galat</th></tr></thead>
<tbody>{% for row in result.rows %}<tr><td>{{row.i}}</td><td>{{"%.7f"|format(row.a)}}</td><td>{{"%.7f"|format(row.b)}}</td><td>{{"%.7f"|format(row.fa)}}</td><td>{{"%.7f"|format(row.fb)}}</td><td>{{"%.7f"|format(row.xr)}}</td><td>{{"%.7f"|format(row.fxr)}}</td><td>{% if row.err is none %}—{% else %}{{"%.4e"|format(row.err)}}{% endif %}</td></tr>{% endfor %}</tbody></table></div>
{% else %}
<h2>Ringkasan Metode</h2><p class="note">Masukkan interval yang mengurung akar, lalu klik <strong>Hitung Akar</strong>. Hasil, status konvergensi, dan tabel setiap iterasi akan muncul di sini.</p>
<div class="formula">f(a) · f(b) &lt; 0</div>
<p class="note">Program memperbarui salah satu batas interval berdasarkan tanda f(xᵣ), lalu menghitung perkiraan akar berikutnya hingga toleransi terpenuhi atau batas iterasi tercapai.</p>
{% endif %}
</section></div></main><footer>Regular Falsi · Aplikasi pembelajaran Metode Numerik</footer>
</body></html>"""

def calculate(key, a, b, tol, max_iter):
    fn = FUNCTIONS[key]["fn"]
    fa, fb = fn(a), fn(b)
    if not all(math.isfinite(v) for v in (fa, fb)):
        raise ValueError("Nilai fungsi pada interval tidak valid.")
    if fa == 0:
        return {"root": a, "froot": fa, "rows": [], "status": "Akar tepat ditemukan pada batas bawah."}
    if fb == 0:
        return {"root": b, "froot": fb, "rows": [], "status": "Akar tepat ditemukan pada batas atas."}
    if fa * fb > 0:
        raise ValueError("f(a) dan f(b) harus berlainan tanda. Coba interval lain.")
    rows, previous = [], None
    for i in range(1, max_iter + 1):
        denominator = fb - fa
        if denominator == 0:
            raise ValueError("Penyebut nol; perhitungan tidak dapat dilanjutkan.")
        xr = (a * fb - b * fa) / denominator
        fxr = fn(xr)
        if not all(math.isfinite(v) for v in (xr, fxr)):
            raise ValueError("Perhitungan menghasilkan angka yang tidak valid. Coba interval lain.")
        err = None if previous is None else abs(xr - previous)
        rows.append({"i": i, "a": a, "b": b, "fa": fa, "fb": fb, "xr": xr, "fxr": fxr, "err": err})
        if fxr == 0 or (err is not None and err < tol):
            return {"root": xr, "froot": fxr, "rows": rows, "status": "Konvergen: toleransi terpenuhi atau akar tepat ditemukan."}
        if fa * fxr < 0:
            b, fb = xr, fxr
        else:
            a, fa = xr, fxr
        previous = xr
    return {"root": rows[-1]["xr"], "froot": rows[-1]["fxr"], "rows": rows, "status": "Batas iterasi tercapai; hasil adalah pendekatan terakhir."}

def read_params(source):
    key = source.get("fungsi", "1")
    if key not in FUNCTIONS:
        raise ValueError("Pilihan fungsi tidak valid.")
    a, b = float(source.get("a", "1")), float(source.get("b", "2"))
    tol, max_iter = float(source.get("tol", "0.0001")), int(source.get("maks", "100"))
    if not all(math.isfinite(v) for v in (a, b, tol)):
        raise ValueError("Semua input numerik harus berupa angka yang valid.")
    if a >= b:
        raise ValueError("Batas bawah a harus lebih kecil daripada batas atas b.")
    if tol <= 0:
        raise ValueError("Toleransi harus lebih besar dari 0.")
    if not 1 <= max_iter <= 10000:
        raise ValueError("Maksimum iterasi harus antara 1 dan 10000.")
    return key, a, b, tol, max_iter

@app.route("/", methods=["GET", "POST"])
def index():
    selected, a, b, tol, maks = "1", "1", "2", "0.0001", "100"
    result, error = None, None
    if request.method == "POST":
        selected, a, b, tol, maks = (request.form.get("fungsi", "1"), request.form.get("a", "1"),
                                    request.form.get("b", "2"), request.form.get("tol", "0.0001"),
                                    request.form.get("maks", "100"))
        try:
            key, av, bv, tv, mv = read_params(request.form)
            result = calculate(key, av, bv, tv, mv)
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            error = str(exc)
    return render_template_string(PAGE, functions=FUNCTIONS, selected=selected, a=a, b=b, tol=tol, maks=maks, result=result, error=error)

@app.route("/download")
def download():
    try:
        key, a, b, tol, maks = read_params(request.args)
        result = calculate(key, a, b, tol, maks)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Iterasi", "a", "b", "f(a)", "f(b)", "xr", "f(xr)", "Galat"])
        for row in result["rows"]:
            writer.writerow([row["i"], row["a"], row["b"], row["fa"], row["fb"], row["xr"], row["fxr"], row["err"]])
        from flask import Response
        return Response(output.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment; filename=regular_falsi_iterasi.csv"})
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        return f"Parameter tidak valid: {exc}", 400

if __name__ == "__main__":
    app.run(debug=False)
