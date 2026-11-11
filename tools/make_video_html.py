"""Генерирует video/video.html — анимация ролика с функцией seek(t)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

parts = symbol(ring=CREAM, jar=CREAM, lid=GREEN, label=DARK, label_leaf=GREEN).split("\n")
ring = parts[0].replace("<path ", '<path id="ring" pathLength="1" stroke-dasharray="1" ')
leaf = f'<g id="leaf" style="transform-origin:120px 29px">{parts[1]}{parts[2]}</g>'
jar = f'<g id="jar" style="transform-origin:100px 150px">{"".join(parts[3:])}</g>'
SYM = f'<svg viewBox="0 0 200 200" width="420" height="420" style="overflow:visible">{ring}{leaf}{jar}</svg>'
d1, w1 = text_path("ЗЕЛЁНЫЙ", 0, 120, 140, "InterDisplay-Black.otf", 0.02)
d2, w2 = text_path("КРУГ", 0, 255, 140, "InterDisplay-Black.otf", 0.02)
WM = (f'<svg viewBox="0 0 {w1+10:.0f} 280" width="{(w1+10)*0.9:.0f}" height="252">'
      f'<path id="wm1" d="{d1}" fill="{CREAM}"/><path id="wm2" d="{d2}" fill="{CREAM}"/></svg>')
SYM_S = symbol(ring=DARK, jar=DARK)

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1920px;height:1080px;overflow:hidden;font-family:Inter;background:{DARK}}}
.sc{{position:absolute;inset:0;overflow:hidden}}
.disp{{font-family:"Inter Display";font-weight:900;letter-spacing:-.02em;line-height:1}}
#s1{{background:{DARK}}}
#s2{{background:{CREAM}}}
#s3{{background:#CFEBD3}}
#s4{{background:{CREAM}}}
#s5{{background:{DARK} url(assets/pattern_dark_preview.svg) center/1300px}}
.abs{{position:absolute}}
.pill{{display:inline-block;background:{PUMPKIN};color:{INK};border-radius:999px;padding:22px 44px;font:800 44px "Inter Display"}}
.bub{{position:absolute;background:#fff;border-radius:40px;padding:30px 44px;font:800 54px "Inter Display";color:{DARK};box-shadow:0 20px 50px rgba(20,39,28,.15);letter-spacing:-.01em}}
.step{{position:absolute;width:300px;text-align:center}}
.step .ic{{width:190px;height:190px;border-radius:50%;background:#fff;margin:0 auto 18px;display:grid;place-items:center;box-shadow:0 14px 30px rgba(20,39,28,.12)}}
.step .ic img{{width:120px}}
.step b{{font:900 40px "Inter Display";color:{DARK}}}
</style></head><body>
<div id="s1" class="sc">
  <div id="logo" class="abs" style="left:300px;top:330px;display:flex;align-items:center;gap:60px">{SYM}<div id="wmw">{WM}<div id="tag" style="font:600 40px Inter;color:#CFE0D3;margin-top:10px">продукты в многоразовой таре</div></div></div>
</div>
<div id="s2" class="sc">
  <div id="t2" class="abs disp" style="left:140px;top:150px;font-size:130px;color:{DARK}"><span id="w1">Продукты</span> <span id="w2" style="color:{GREEN}">в стекле.</span><br><span id="w3" style="font-size:90px">Без пластика.</span></div>
  <img id="i1" class="abs" src="assets/ill_jars.svg" style="left:1000px;top:480px;width:520px">
  <img id="i2" class="abs" src="assets/ill_milk.svg" style="left:1430px;top:250px;width:420px">
  <img id="i3" class="abs" src="assets/ill_bag.svg" style="left:120px;top:560px;width:460px">
  <img id="i4" class="abs" src="assets/ill_courier.svg" style="left:560px;top:600px;width:440px">
</div>
<div id="s3" class="sc">
  <div id="disc" class="abs" style="left:250px;top:140px;width:820px;height:820px;border-radius:50%;background:#B2DDB8"></div>
  <div id="ring3" class="abs" style="left:220px;top:110px;width:880px;height:880px;border-radius:50%;border:28px solid {DARK};clip-path:polygon(0 0,60% 0,60% 30%,100% 30%,100% 100%,0 100%)"></div>
  <img id="m3" class="abs" src="assets/000.png" style="left:230px;top:80px;width:860px">
  <div id="b1" class="bub" style="left:1120px;top:260px">Привет! Я&nbsp;Кругляш</div>
  <div id="b2" class="bub" style="left:1120px;top:470px;font-size:44px;background:{DARK};color:{CREAM}">Слежу, чтобы каждая<br>банка вернулась по&nbsp;кругу</div>
  <img id="st1" class="abs" src="assets/sticker_nyam.png" style="left:1250px;top:690px;width:300px">
  <img id="st2" class="abs" src="assets/sticker_lyublyu.png" style="left:1540px;top:640px;width:300px">
</div>
<div id="s4" class="sc">
  <div id="t4" class="abs disp" style="left:0;right:0;top:80px;text-align:center;font-size:100px;color:{DARK}">Тара едет по кругу</div>
  <svg class="abs" style="left:660px;top:250px" width="600" height="600" viewBox="0 0 600 600"><circle id="c4" cx="300" cy="300" r="250" fill="none" stroke="{GREEN}" stroke-width="22" stroke-linecap="round" pathLength="1" stroke-dasharray="1" transform="rotate(-90 300 300)"/>
  <g id="trav"><g transform="translate(-28,-34)"><rect x="0" y="12" width="56" height="58" rx="16" fill="#C6EBCF" stroke="{DARK}" stroke-width="6"/><rect x="4" y="0" width="48" height="16" rx="5" fill="{PUMPKIN}" stroke="{DARK}" stroke-width="5"/></g></g>
  <g transform="translate(200,200)">{SYM_S}</g></svg>
  <div id="p1" class="step" style="left:810px;top:205px"><div class="ic"><img src="assets/icon_order.svg"></div><b>Заказ</b></div>
  <div id="p2" class="step" style="left:1060px;top:455px"><div class="ic"><img src="assets/icon_deliver.svg"></div><b>Доставка</b></div>
  <div id="p3" class="step" style="left:810px;top:705px"><div class="ic"><img src="assets/icon_return.svg"></div><b>Возврат</b></div>
  <div id="p4" class="step" style="left:560px;top:455px"><div class="ic"><img src="assets/icon_wash.svg"></div><b>Мойка</b></div>
</div>
<div id="s5" class="sc">
  <div class="abs" style="inset:0;background:radial-gradient(circle at 50% 45%,rgba(31,81,54,.95) 30%,rgba(31,81,54,.6))"></div>
  <img id="l5" class="abs" src="assets/logo_horizontal_dark.svg" style="left:50%;top:250px;width:1100px;margin-left:-550px">
  <div id="u5" class="abs disp" style="left:0;right:0;top:640px;text-align:center;font-size:72px;color:{CREAM}">zelkrug.ru</div>
  <div id="c5" class="abs" style="left:0;right:0;top:770px;text-align:center"><span class="pill">−10% на первый заказ</span></div>
  <img id="m5" class="abs" src="assets/sticker_privet.png" style="left:1500px;top:600px;width:360px">
</div>
<script>
const $=id=>document.getElementById(id);
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const p=(t,a,d)=>cl((t-a)/d);
const eo=x=>1-Math.pow(1-x,3);
const back=x=>{{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const bounce=x=>{{const n=7.5625,d=2.75;if(x<1/d)return n*x*x;if(x<2/d)return n*(x-=1.5/d)*x+.75;if(x<2.5/d)return n*(x-=2.25/d)*x+.9375;return n*(x-=2.625/d)*x+.984375}};
const pop=(el,k,dy=60)=>{{el.style.opacity=cl(k*3);el.style.transform=`translateY(${{(1-back(k))*dy}}px) scale(${{.6+.4*back(k)}})`}};
const S=[0,4,9,14.5,20,24];
function wipe(id,t,start){{const k=eo(p(t,start,.7));$(id).style.clipPath=`circle(${{k*130}}% at 50% 50%)`;$(id).style.display=t>=start?'block':'none'}}
window.seek=function(t){{
  // сцена 1 — сборка логотипа
  $('ring').style.strokeDashoffset=1-eo(p(t,.2,1.3));
  const lk=p(t,1.2,.6);$('leaf').style.transform=`scale(${{back(lk)}}) rotate(${{(1-lk)*-40}}deg)`;$('leaf').style.opacity=lk>0?1:0;
  const jk=p(t,1.5,.9);$('jar').style.transform=`translateY(${{(1-bounce(jk))*-260}}px)`;$('jar').style.opacity=jk>0?1:0;
  const wk=eo(p(t,2.1,.7));$('wmw').style.opacity=wk;$('wmw').style.transform=`translateX(${{(1-wk)*80}}px)`;
  $('tag').style.opacity=p(t,2.7,.5);
  const zoom=1+0.04*p(t,0,4);$('logo').style.transform=`scale(${{zoom}})`;
  // сцена 2
  wipe('s2',t,S[1]);
  [['w1',4.4],['w2',4.75],['w3',5.2]].forEach(([id,a])=>{{const k=p(t,a,.5);$(id).style.opacity=k;$(id).style.display='inline-block';$(id).style.transform=`translateY(${{(1-eo(k))*60}}px)`}});
  [['i1',5.5],['i2',5.8],['i3',6.1],['i4',6.4]].forEach(([id,a],i)=>{{const k=p(t,a,.6);pop($(id),k,120);if(k>=1)$(id).style.transform=`translateY(${{Math.sin((t-a)*2.2+i)*10}}px)`}});
  // сцена 3
  wipe('s3',t,S[2]);
  const f=Math.floor(Math.max(0,t-S[2])*12)%24;$('m3').src=`assets/${{String(f).padStart(3,'0')}}.png`;
  $('ring3').style.transform=`rotate(${{(t-S[2])*25}}deg)`;
  pop($('b1'),p(t,9.9,.5),40);pop($('b2'),p(t,11.2,.5),40);
  [['st1',12.3],['st2',12.7]].forEach(([id,a],i)=>{{const k=p(t,a,.5);pop($(id),k,80);if(k>=1)$(id).style.transform=`rotate(${{Math.sin((t-a)*3+i)*6}}deg)`}});
  // сцена 4
  wipe('s4',t,S[3]);
  const t4=p(t,15,.6);$('t4').style.opacity=t4;$('t4').style.transform=`translateY(${{(1-eo(t4))*-40}}px)`;
  const ck=p(t,15.3,3.8);$('c4').style.strokeDashoffset=1-ck;
  const a=(-90+360*eo(ck))*Math.PI/180;$('trav').setAttribute('transform',`translate(${{300+250*Math.cos(a)}},${{300+250*Math.sin(a)}})`);$('trav').style.opacity=ck>0?1:0;
  [['p1',15.4],['p2',16.3],['p3',17.2],['p4',18.1]].forEach(([id,a])=>pop($(id),p(t,a,.5),60));
  // сцена 5
  wipe('s5',t,S[4]);
  const l5=p(t,20.4,.7);$('l5').style.opacity=l5;$('l5').style.transform=`scale(${{.8+.2*back(l5)}})`;
  pop($('u5'),p(t,21,.5),40);pop($('c5'),p(t,21.4,.5),40);
  const m5=p(t,21.8,.6);pop($('m5'),m5,100);if(m5>=1)$('m5').style.transform=`rotate(${{Math.sin((t-21.8)*4)*7}}deg)`;
}};
seek(0);
</script></body></html>"""
open(sys.argv[1], "w").write(html)
print("ok")
