<?php
function f($x,$jenis){
 switch($jenis){
  case 'p1': return $x*$x*$x-$x-2;
  case 'p2': return $x*$x-4;
  case 'p3': return cos($x)-$x;
  case 'p4': return exp($x)-3*$x;
  case 'p5': return $x*$x-$x-2;
  default: throw new Exception('Fungsi tidak valid.');
 }
}
function fmt($n){return rtrim(rtrim(number_format($n,8,'.',''),'0'),'.');}
$jenis=$_POST['fungsi']??'p1'; $aS=$_POST['a']??'1'; $bS=$_POST['b']??'2'; $tolS=$_POST['tol']??'0.0001'; $maxS=$_POST['max']??'100'; $rows=[];$akar=null;$error='';$status='';
if($_SERVER['REQUEST_METHOD']==='POST'){
 try{
  if(!in_array($jenis,['p1','p2','p3','p4','p5'],true)) throw new Exception('Pilih fungsi yang tersedia.');
  foreach([$aS,$bS,$tolS,$maxS] as $v) if(!is_numeric($v)) throw new Exception('Semua input harus berupa angka.');
  $a=(float)$aS;$b=(float)$bS;$tol=(float)$tolS;$max=(int)$maxS;
  if($a >= $b) throw new Exception('Batas bawah a harus lebih kecil dari b.');
  if($tol<=0) throw new Exception('Toleransi harus lebih besar dari 0.');
  if($max<1||$max>1000) throw new Exception('Maksimal iterasi harus 1–1000.');
  $fa=f($a,$jenis);$fb=f($b,$jenis);
  if($fa==0){$akar=$a;$status='Akar tepat ditemukan pada batas bawah.';}
  elseif($fb==0){$akar=$b;$status='Akar tepat ditemukan pada batas atas.';}
  elseif($fa*$fb>0) throw new Exception('f(a) dan f(b) harus berlainan tanda. Coba interval lain.');
  else{
   $prev=null;$konvergen=false;
   for($i=1;$i<=$max;$i++){
    if(abs($fb-$fa)<1e-15) throw new Exception('Penyebut terlalu dekat dengan nol.');
    $xr=($a*$fb-$b*$fa)/($fb-$fa);$fr=f($xr,$jenis);
    if(!is_finite($xr)||!is_finite($fr)) throw new Exception('Hasil perhitungan tidak valid.');
    $err=$prev===null?null:abs($xr-$prev);
    $rows[]=[$i,$a,$b,$fa,$fb,$xr,$fr,$err];
    if(abs($fr)<=$tol||($err!==null&&$err<=$tol)){$konvergen=true;$akar=$xr;break;}
    if($fa*$fr<0){$b=$xr;$fb=$fr;}else{$a=$xr;$fa=$fr;}
    $prev=$xr;$akar=$xr;
   }
   $status=$konvergen?'Konvergen: toleransi tercapai.':'Batas iterasi tercapai; hasil adalah pendekatan terakhir.';
  }
 }catch(Throwable $e){$error=$e->getMessage();}
}
$names=['p1'=>'x³ − x − 2','p2'=>'x² − 4','p3'=>'cos(x) − x (radian)','p4'=>'eˣ − 3x','p5'=>'x² − x − 2'];
function h($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
?>
<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Regular Falsi | Metode Numerik</title><link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head><body>
<div class="wrap"><header><div class="logo">RF</div><div><small>METODE NUMERIK</small><h1>Regular Falsi</h1></div><span class="tag">ROOT FINDER</span></header>
<section class="hero"><div><small>NUMERICAL ANALYSIS</small><h2>Temukan akar fungsi<br><em>dengan pendekatan numerik.</em></h2><p>Atur interval, toleransi, dan iterasi. Sistem menampilkan hasil serta tabel proses perhitungan.</p></div><div class="formula"><small>RUMUS REGULAR FALSI</small><strong>xᵣ = (a·f(b) − b·f(a)) / (f(b) − f(a))</strong><p>Syarat: f(a) dan f(b) berlainan tanda.</p></div></section>
<main><form method="post" id="calc"><section class="card"><div class="heading"><b>01</b><div><h3>Parameter perhitungan</h3><p>Masukkan data awal metode.</p></div></div>
<label for="fungsi">Pilih fungsi f(x)</label><select id="fungsi" name="fungsi"><?php foreach($names as $key=>$name):?><option value="<?=h($key)?>" <?=$jenis===$key?'selected':''?>>f(x) = <?=h($name)?></option><?php endforeach;?></select>
<div class="grid"><div><label for="a">Batas bawah (a)</label><input id="a" name="a" type="number" step="any" value="<?=h($aS)?>" required></div><div><label for="b">Batas atas (b)</label><input id="b" name="b" type="number" step="any" value="<?=h($bS)?>" required></div></div>
<div class="grid"><div><label for="tol">Toleransi</label><input id="tol" name="tol" type="number" min="0.0000000001" step="any" value="<?=h($tolS)?>" required></div><div><label for="max">Maks. iterasi</label><input id="max" name="max" type="number" min="1" max="1000" value="<?=h($maxS)?>" required></div></div>
<div class="hint">ⓘ Contoh: x³ − x − 2 dengan interval [1, 2].</div><button class="primary" type="submit">Hitung akar <span>↗</span></button><button class="secondary" id="reset" type="reset">Reset input</button></section></form>
<section class="card"><div class="heading"><b>02</b><div><h3>Hasil perhitungan</h3><p>Ringkasan pendekatan akar.</p></div></div>
<?php if($error):?><div class="error"><b>Perhitungan gagal</b><p><?=h($error)?></p></div><div class="empty"><strong>Periksa input kembali</strong><p>Pastikan interval mengurung akar.</p></div>
<?php elseif($akar!==null):?><div class="root"><small>PENDEKATAN AKAR</small><strong><?=h(fmt($akar))?></strong><span>f(x) = <?=h($names[$jenis])?></span></div><div class="status"><?=h($status)?></div><div class="stats"><div><small>Jumlah iterasi</small><b><?=count($rows)?></b></div><div><small>Toleransi</small><b><?=h($tolS)?></b></div></div>
<?php else:?><div class="empty"><div class="symbol">∑</div><strong>Hasil akan tampil di sini</strong><p>Isi parameter lalu tekan tombol Hitung akar.</p><span>f(a) × f(b) &lt; 0</span></div><?php endif;?></section></main>
<?php if($rows):?><section class="card table-card"><div class="heading"><b>03</b><div><h3>Tabel iterasi</h3><p>Rincian setiap langkah perhitungan.</p></div><button type="button" class="download" id="csv">Unduh CSV ↓</button></div><div class="scroll"><table id="table"><thead><tr><th>Iterasi</th><th>a</th><th>b</th><th>f(a)</th><th>f(b)</th><th>xᵣ</th><th>f(xᵣ)</th><th>Galat</th></tr></thead><tbody><?php foreach($rows as $r):?><tr><?php foreach($r as $j=>$v):?><td><?=$j===7&&$v===null?'—':h(is_float($v)?fmt($v):$v)?></td><?php endforeach;?></tr><?php endforeach;?></tbody></table></div><p class="note">Galat absolut = |xᵣ sekarang − xᵣ sebelumnya|.</p></section><?php endif;?>
<section class="info"><b>i</b><p><strong>Cara kerja:</strong> Regular Falsi memperkirakan akar dengan garis yang menghubungkan titik (a, f(a)) dan (b, f(b)). Interval diperbarui sampai toleransi tercapai atau batas iterasi terpenuhi.</p></section><footer>REGULAR FALSI · TUGAS METODE NUMERIK</footer></div></body></html>
