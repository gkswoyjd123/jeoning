#!/usr/bin/env python3
"""data.json -> index.html + <day>.html. 사용: python3 build.py
type: milk(우유 91) car(오빠달려붕붕 120) ganbare(간바레 151) sig(슴흔들 시그모음 500)"""
import json, html, os
D = os.path.dirname(os.path.abspath(__file__))
COL = {"milk": "#3b82f6", "car": "#ec4899", "ganbare": "#38bdf8", "sig": "#8b5cf6"}
def hms(s): return "%d:%02d:%02d" % (s // 3600, s % 3600 // 60, s % 60)
e = html.escape
CSS = """body{margin:0;padding:14px;background:#0f1115;color:#eee;font-family:'Malgun Gothic',sans-serif}
a{color:#9cf;text-decoration:none}
.hd{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px}
.hd h1{font-size:20px;margin:0}.meta{color:#aaa;font-size:14px}.cnt{background:#3b82f6;color:#fff;border-radius:12px;padding:2px 10px;font-size:13px}
.nav{margin-left:auto;display:flex;gap:6px}.nav a,.nav span{padding:6px 12px;border-radius:8px;background:#222;font-size:14px}.nav span{color:#555}
#wrap{background:#000}#wrap iframe{width:100%;height:72vh;border:0;display:block}#wrap:fullscreen{padding:0}#wrap:fullscreen iframe{height:100vh}
.bar{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
button{border:2px solid transparent;border-radius:10px;color:#fff;cursor:pointer;font-size:14px;padding:6px;display:flex;flex-direction:column;align-items:flex-start;gap:4px;background:var(--c);opacity:.85;transition:.15s}
button:hover{opacity:1}button.on{opacity:1;border-color:#fff;box-shadow:0 0 0 3px var(--c),0 0 14px var(--c);transform:translateY(-2px)}
button img{width:160px;border-radius:6px;display:block}button b{background:#fff;color:var(--c);border-radius:4px;padding:0 6px;margin-right:4px}
#fs{--c:#22c55e;justify-content:center;padding:10px 16px;align-self:stretch}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.card{background:#1a1d24;border-radius:12px;overflow:hidden;color:#eee;transition:.15s}.card:hover{transform:translateY(-3px);box-shadow:0 6px 18px #000}
.card img{width:100%;display:block;aspect-ratio:16/9;object-fit:cover;background:#000}.card div{padding:10px}.card .d{font-size:18px;font-weight:bold}"""
def page(d, prev, nxt):
    rs = d["reactions"]; v = d["vod"]
    btns = ""
    for i, r in enumerate(rs, 1):
        img = '<img src="%s" alt="">' % e(r["thumb"]) if r.get("thumb") else ""
        btns += '<button style="--c:%s" onclick="go(%d)">%s<span><b>%d</b>%s %s</span></button>' % (COL.get(r["type"], "#666"), i - 1, img, i, hms(r["sec"]), e(r["label"]))
    nav = lambda x, t: '<a href="%d.html">%s</a>' % (x, t) if x else '<span>%s</span>' % t
    first = rs[0]["sec"] if rs else 0
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{e(d['title'])}</title><style>{CSS}</style></head><body>
<div class="hd"><a href="index.html">← 목록</a><h1>{e(d['title'])}</h1><span class="meta">{e(d['date'])}</span><span class="cnt">리액션 {len(rs)}개</span>
<div class="nav">{nav(prev,'◀ 이전 일차')}{nav(nxt,'다음 일차 ▶')}</div></div>
<div id="wrap"><iframe id="v" allow="autoplay; fullscreen" allowfullscreen src="https://vod.sooplive.com/player/{v}/embed?change_second={first}&autoPlay=true&autoplay=1"></iframe></div>
<div class="bar"><button id="fs" onclick="fs()">⛶ 전체화면</button>{btns}</div>
<script>
var T={json.dumps([r['sec'] for r in rs])},B=document.querySelectorAll('.bar button:not(#fs)');
function go(i){{document.getElementById('v').src='https://vod.sooplive.com/player/{v}/embed?change_second='+T[i]+'&autoPlay=true&autoplay=1&_='+Date.now();B.forEach(function(b,j){{b.classList.toggle('on',j===i)}});setTimeout(function(){{window.focus()}},300)}}
function fs(){{var w=document.getElementById('wrap');if(document.fullscreenElement)document.exitFullscreen();else w.requestFullscreen()}}
setInterval(function(){{var f=document.getElementById('v');if(document.activeElement===f){{f.blur();window.focus()}}}},400);
document.addEventListener('keydown',function(e){{var n=parseInt(e.key);if(n>=1&&n<=T.length)go(n-1)}});
</script></body></html>"""
def main():
    days = sorted(json.load(open(os.path.join(D, "data.json"), encoding="utf-8"))["days"], key=lambda x: x["day"])
    nums = [d["day"] for d in days]; cards = ""
    for d in days:
        n = d["day"]
        prev, nxt = (n - 1 if n - 1 in nums else None), (n + 1 if n + 1 in nums else None)
        open(os.path.join(D, "%d.html" % n), "w", encoding="utf-8").write(page(d, prev, nxt))
        th = next((r["thumb"] for r in d["reactions"] if r.get("thumb")), "")
        cards += f'<a class="card" href="{n}.html">{"<img src=%s alt=>" % e(th) if th else "<img alt=>"}<div><div class="d">{n}일차</div>{e(d["title"])}<br><span class="meta">{e(d["date"])} · 리액션 {len(d["reactions"])}개</span></div></a>'
    open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>져닝 리액션 시간</title><style>{CSS}</style></head><body><div class="hd"><h1>져닝 리액션 시간</h1><span class="cnt">{len(days)}일차</span></div><div class="cards">{cards}</div></body></html>')
if __name__ == "__main__": main()
