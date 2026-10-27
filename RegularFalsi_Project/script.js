document.addEventListener('DOMContentLoaded',()=>{
 const form=document.getElementById('calc'),reset=document.getElementById('reset'),csv=document.getElementById('csv');
 if(form)form.addEventListener('submit',e=>{
  const a=Number(document.getElementById('a').value),b=Number(document.getElementById('b').value),t=Number(document.getElementById('tol').value),m=Number(document.getElementById('max').value);
  if(![a,b,t,m].every(Number.isFinite)){e.preventDefault();alert('Isi semua input dengan angka yang valid.');}
  else if(a>=b){e.preventDefault();alert('Batas bawah a harus lebih kecil dari b.');}
  else if(t<=0||!Number.isInteger(m)||m<1||m>1000){e.preventDefault();alert('Toleransi harus positif dan iterasi antara 1–1000.');}
 });
 if(reset&&form)reset.addEventListener('click',()=>setTimeout(()=>{document.getElementById('a').value='1';document.getElementById('b').value='2';document.getElementById('tol').value='0.0001';document.getElementById('max').value='100';document.getElementById('fungsi').value='p1';},0));
 if(csv)csv.addEventListener('click',()=>{
  const table=document.getElementById('table');if(!table)return;
  const content=Array.from(table.querySelectorAll('tr')).map(r=>Array.from(r.querySelectorAll('th,td')).map(c=>'"'+c.innerText.replaceAll('"','""')+'"').join(',')).join('\r\n');
  const url=URL.createObjectURL(new Blob(['\uFEFF'+content],{type:'text/csv;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='hasil-regula-falsi.csv';a.click();URL.revokeObjectURL(url);
 });
});
