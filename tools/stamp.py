# 배포 직전에 index.html 의 <meta name="build"> 에 지금 시각(서울)을 적는다. 푸시 루틴에서 자동으로 부른다.
import re, datetime, zoneinfo, pathlib, collections
p=pathlib.Path(__file__).resolve().parent.parent/'index.html'
s=p.read_text(encoding='utf-8')
# 먼저 「이름이 겹친 함수」가 없는지 본다. 같은 범위에서 함수를 같은 이름으로 두 번 선언하면 오류 없이 뒤의 것이 앞의 것을 덮어쓴다.
# 2026-10-08 선 고르기를 넣다가 paintSel·inkRect 가 글자 선택 쪽 함수를 덮어써 PDF 글자 끌기 메뉴가 죽었다 — node --check 는 이것을 못 잡는다.
js=max(re.findall(r'<script>(.*?)</script>', s, flags=re.S), key=len)
seen=collections.defaultdict(list)
for i,ln in enumerate(js.splitlines(), 1):
    m=re.match(r'(?:async )?function[*]? ([A-Za-z_$][A-Za-z0-9_$]*) *[(]', ln)
    if m: seen[m.group(1)].append(i)
dup={k:v for k,v in seen.items() if len(v)>1}
assert not dup, '이름이 겹친 함수가 있습니다(뒤의 것이 앞의 것을 덮어씁니다): '+', '.join('%s — 스크립트 %s줄' % (k, '·'.join(map(str, v))) for k,v in dup.items())
now=datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Seoul')).replace(microsecond=0).isoformat()
s2,n=re.subn(r'<meta name="build" content="[^"]*">', lambda m: '<meta name="build" content="'+now+'">', s, count=1)
assert n==1, 'build meta 가 없습니다'
p.write_text(s2, encoding='utf-8'); print('build', now, '· 함수', len(seen), '개 · 이름 겹침 없음')
