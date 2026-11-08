// public/js/vt-datos-envio.js
/* Datos de envío (Etapa 2i): el script de main sin cambios de fondo. El texto de WhatsApp, sus emojis y el bloque #VT1 los
   lee el sistema del dueño: no se cambian. Solo se pasa de style.display a hidden y de onclick a addEventListener. */
(function () {
'use strict';
const ESTADOS=["Aguascalientes","Baja California","Baja California Sur","Campeche","Chiapas","Chihuahua","CDMX","Coahuila","Colima","Durango","Estado de México","Guanajuato","Guerrero","Hidalgo","Jalisco","Michoacán","Morelos","Nayarit","Nuevo León","Oaxaca","Puebla","Querétaro","Quintana Roo","San Luis Potosí","Sinaloa","Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz","Yucatán","Zacatecas"];
const $=id=>document.getElementById(id);
$("estado").innerHTML='<option value="">Elige el estado</option>'+ESTADOS.map(e=>`<option>${e}</option>`).join('');
const b64e=o=>btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
let P={};
try{const d=new URLSearchParams(location.search).get('d');if(d)P=JSON.parse(decodeURIComponent(escape(atob(d.replace(/-/g,'+').replace(/_/g,'/')))));}catch(e){P={};}
if(P.n){$("hola").textContent='Hola '+P.n.split(' ')[0]+', ¿a dónde te lo enviamos?';$("recibe").value=P.n;}
if(P.p){$("order").hidden=false;$("oProd").textContent=P.p;$("oFolio").textContent=P.f?'Pedido '+P.f:'';$("oTot").textContent=P.t||'';}
if(P.s&&ESTADOS.includes(P.s))$("estado").value=P.s;
if(P.c)$("municipio").value=P.c;
if(P.z)$("cp").value=P.z;
const WA=(P.w&&/^\d{10}$/.test(P.w))?P.w:'8333268008';
const dg=s=>(s||'').replace(/\D/g,'');
const v=id=>$(id).value.trim();
function marca(id,ok){$(id).classList.toggle('bad',!ok);return ok;}
function enviar(){
  let ok=true;
  ['calle','colonia','municipio','ref'].forEach(id=>ok=marca(id,v(id).length>=2)&&ok);
  ok=marca('estado',!!v('estado'))&&ok;
  ok=marca('cp',dg(v('cp')).length===5)&&ok;
  ok=marca('recibe',v('recibe').split(/\s+/).length>=2)&&ok;
  ok=marca('tel',dg(v('tel')).slice(-10).length===10)&&ok;
  const fx=$("quiere").checked;
  if(fx){
    ok=marca('rfc',/^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$/.test(v('rfc').toUpperCase()))&&ok;
    ok=marca('fcp',dg(v('fcp')).length===5)&&ok;
    ok=marca('razon',v('razon').length>=3)&&ok;
    ok=marca('regimen',!!v('regimen'))&&ok;ok=marca('uso',!!v('uso'))&&ok;
    ok=marca('correo',/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v('correo')))&&ok;
  }
  $("err").hidden=ok;
  if(!ok){const b=document.querySelector('.bad');if(b){b.scrollIntoView({behavior:'smooth',block:'center'});b.focus();}return;}
  const e={calle:v('calle'),colonia:v('colonia'),municipio:v('municipio'),estado:v('estado'),cp:dg(v('cp')),ref:v('ref'),recibe:v('recibe'),tel:dg(v('tel')).slice(-10)};
  const x=fx?{rfc:v('rfc').toUpperCase(),cp:dg(v('fcp')),razon:v('razon'),regimen:v('regimen'),uso:v('uso'),correo:v('correo')}:null;
  let t=`Hola, aquí están mis datos de envío${P.f?' para el pedido '+P.f:''}:\n\n`;
  t+=`📍 *Dirección de entrega*\nCalle y número: ${e.calle}\nColonia: ${e.colonia}\nMunicipio: ${e.municipio}\nEstado: ${e.estado}\nCódigo Postal: ${e.cp}\nReferencias: ${e.ref}\n\n`;
  t+=`📦 *Recibe*\nNombre: ${e.recibe}\nTeléfono: ${e.tel}\n\n`;
  t+=x?`🧾 *Factura*\nRFC: ${x.rfc}\nRazón social: ${x.razon}\nRégimen: ${x.regimen}\nC.P. fiscal: ${x.cp}\nUso de CFDI: ${x.uso}\nCorreo: ${x.correo}\n\n`:`🧾 Factura: no\n\n`;
  t+=`#VT1:${b64e({f:P.f||'',e,x})}`;
  const url=`https://wa.me/52${WA}?text=${encodeURIComponent(t)}`;
  $("again").href=url;$("form").hidden=true;$("done").hidden=false;window.scrollTo(0,0);
  location.href=url;
}
$("enviar").addEventListener('click',enviar);
$("quiere").addEventListener('change',function(){$("fact").hidden=!this.checked;});
})();
