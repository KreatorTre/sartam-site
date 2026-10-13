document.addEventListener('click',e=>{const s=e.target.closest('.spoiler');if(s)s.classList.toggle('open')});
document.addEventListener('keydown',e=>{const s=e.target.closest&&e.target.closest('.spoiler');if(s&&(e.key==='Enter'||e.key===' ')){e.preventDefault();s.classList.toggle('open')}});
function initQuiz(QS){const el=document.getElementById('quiz'),sc=document.getElementById('score');let r=0,n=0;
function up(){sc.textContent=`Score: ${r} / ${n}  (of ${QS.length})`}
function build(){r=n=0;up();el.innerHTML='';QS.forEach((q,i)=>{const d=document.createElement('div');d.className='q';
d.innerHTML=`<strong>${i+1}. </strong><span></span><div><button class="btn rv">Reveal answer</button></div><div class="a"><p></p><button class="btn ok">I got it ✓</button><button class="btn ghost no">Missed it ✗</button></div>`;
d.querySelector('span').textContent=q.q;d.querySelector('.a p').innerHTML=q.a.replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
d.querySelector('.rv').onclick=ev=>{d.classList.add('shown');ev.target.remove()};
d.querySelectorAll('.ok,.no').forEach(b=>b.onclick=()=>{const ok=b.classList.contains('ok');n++;if(ok)r++;d.classList.add(ok?'right':'wrong');d.querySelectorAll('.ok,.no').forEach(x=>x.remove());up()});el.appendChild(d)})}
document.getElementById('reset').onclick=build;build()}
