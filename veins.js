(()=>{const c=document.getElementById('veins'),x=c.getContext('2d');let w,h,d=Math.min(devicePixelRatio||1,2);
const red=matchMedia('(prefers-reduced-motion: reduce)').matches;
function rs(){w=innerWidth;h=innerHeight;c.width=w*d;c.height=h*d;x.setTransform(d,0,0,d,0,0)}rs();addEventListener('resize',rs);
function bolt(x0,y0,a,len,depth,pts){let px=x0,py=y0;const s=[[px,py]];const n=8+Math.random()*10|0;
for(let i=0;i<n;i++){a+=(Math.random()-.5)*.9;px+=Math.cos(a)*len/n;py+=Math.sin(a)*len/n;s.push([px,py]);
if(depth<2&&Math.random()<.18)bolt(px,py,a+(Math.random()-.5)*1.5,len*.45,depth+1,pts)}pts.push({s,wd:2.2-depth*.7})}
let vs=[];function spawn(){const p=[],e=Math.random()*4|0,X=e==1?w:e==3?0:Math.random()*w,Y=e==0?0:e==2?h:Math.random()*h;
bolt(X,Y,Math.atan2(h/2-Y,w/2-X)+(Math.random()-.5),Math.max(w,h)*(.3+Math.random()*.4),0,p);vs.push({p,life:1,dec:.008+Math.random()*.02})}
function draw(){x.clearRect(0,0,w,h);x.lineCap='round';
for(const v of vs){const f=v.life*(.6+Math.random()*.4);for(const b of v.p){x.beginPath();b.s.forEach(([a,c],i)=>i?x.lineTo(a,c):x.moveTo(a,c));
x.strokeStyle=`rgba(46,168,255,${.18*f})`;x.lineWidth=b.wd*4;x.stroke();x.strokeStyle=`rgba(170,225,255,${.55*f})`;x.lineWidth=b.wd*.6;x.stroke()}v.life-=v.dec}
vs=vs.filter(v=>v.life>0)}
for(let i=0;i<5;i++)spawn();if(red){draw();return}
let last=0;function loop(t){if(!document.hidden&&t-last>40){last=t;if(vs.length<(w<700?4:7)&&Math.random()<.06)spawn();draw()}requestAnimationFrame(loop)}requestAnimationFrame(loop)})();
