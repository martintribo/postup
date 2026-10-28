# Fold the four "<page>-signin" pages into the signin sheet (Martin, Oct 31 2026 [M1031-draft]). exec'd by build.py after home.py.
import json, re
# The button that used to open a separate "-signin" page now calls act(dest,title,sub): signed out it opens the signin sheet in the
# page's sheet slot with a continuation (dest); signed in it goes straight to dest. Old URLs (#join-signin etc.) still work:
# FOLD_JS (prepended to the page script) rewrites the hash to the host page and opens the sheet.
FOLD={'join-signin':('postup','joined','Join Maya','Sign in so Maya knows who’s coming.'),
      'ask-signin':('postup-ask','ask','Ask Tess','Sign in so Tess knows who’s asking.'),
      'post-signin':('post','posted','Almost there','Sign in and your postup goes live.'),
      'attach-signin':('project-attach','posted','Almost there','Sign in to post up for this project.')}
def _actcall(k): h,d,t,s=FOLD[k]; return f"act('{d}','{t}','{s}')"
for _k in list(S):
    if _k.split('--')[0] in FOLD: del S[_k]; continue
    _v=S[_k]
    for _f in FOLD:
        _v=re.sub(r"(?:sheet|go)\('"+_f+r"'\)",_actcall(_f),_v)
    S[_k]=_v
_left=[k for k in S if any(f in S[k] for f in FOLD) and k!='index']
assert not _left, f'fold: old signin page ids still referenced in {_left}'
DLG=[d for d in DLG if d not in FOLD]
FOLD_JS='(function(){var A='+json.dumps({k:list(v) for k,v in FOLD.items()},ensure_ascii=False)+''';function f(){var h=location.hash.slice(1),a=A[h];if(!a)return;history.replaceState(null,"",location.pathname+location.search+"#"+a[0]);setTimeout(function(){act(a[1],a[2],a[3])},0)}addEventListener("hashchange",f);f()})();
'''
