# Deterministic phase-consistency checks [M1047-draft]. Called from validate.py.
# Failures are reported through validate.err (file:line). Exceptions live in model/phases.toml.
import os, re, copy
import model as M

# Screens that implement the named rules (all must be unavailable when the rule holds).
RULE_SCREENS = {
    'no-share': ['share'],
    'no-inbox': ['inbox'],
    'no-chat': ['chat'],
    'no-leave': ['leave'],
    'no-projects': ['projects', 'project', 'project-new', 'project-update', 'project-attach', 'invite-project'],
    'no-ask-to-join': ['ask', 'postup-ask', 'requested'],
    'no-size-limit': ['postup-full'],
}

def _exc(check, item, ph):
    for x in M.PEXCEPT:
        if x.get('check') != check: continue
        if x.get('item') != item: continue
        if not M.in_phase(x, ph): continue
        if not re.search(M.TAG, x.get('reason') or ''):
            continue
        return x
    return None

def _need_reason(err, path, needle, x):
    if x and not re.search(M.TAG, x.get('reason') or ''):
        err(path, needle, f'phase exception for {x.get("item")}: reason needs a source tag')

def run(sc, fl, ev, gl, err, US, WAYS, GS):
    """Register every new phase check. err(path, needle, msg) as in validate.py."""
    if not M.PIDS:
        err(M.PHASES_FILE or 'model/phases.toml', '[[phases]]', 'phases.toml must list at least one phase')
        return
    _check_ids(sc, fl, ev, WAYS, GS, err)
    _check_legacy_phase_key(sc, fl, ev, WAYS, GS, err)
    _check_monotonic(sc, fl, ev, WAYS, GS, err)
    _check_targets(sc, ev, err)
    _check_flow_screens(sc, fl, err)
    _check_delta(sc, fl, ev, WAYS, GS, err)
    _check_rules(sc, ev, err)
    _check_way_path(fl, WAYS, US, err)
    _check_deliverable_goals(sc, fl, US, WAYS, GS, err)

def _known(v, path, needle, err, ctx):
    if v is None: return True
    try:
        M.pid(v)
        return True
    except ValueError:
        err(path, needle, f'{ctx}: unknown phase id {v!r} (ids are {M.PIDS})')
        return False

def _bounds_ok(item):
    for v in (item.get('since'), item.get('until')):
        if v is None: continue
        try: M.pid(v)
        except ValueError:
            return False
    return True

def _iter_items(sc, fl, ev, WAYS, GS):
    for s in sc.values():
        yield 'screen', s['id'], s, s['_file'], 'since =' if s.get('since') else 'id ='
        for i,l in enumerate(s.get('links') or []):
            yield 'link', f"{s['id']}:{l['id']}", l, s['_file'], f'id = "{l["id"]}"'
    for f in fl.values():
        yield 'flow', f['id'], f, f['_file'], 'since =' if f.get('since') else 'id ='
    for e in ev.get('events') or []:
        yield 'event', e['id'], e, ev['_file'], f'id = "{e["id"]}"'
    for w in WAYS.values():
        yield 'way', w['id'], w, w.get('_file') or 'model/ways.toml', f'id = "{w["id"]}"'
    for g in GS.values():
        yield 'goal', g['id'], g, g.get('_file') if isinstance(g.get('_file'), str) else 'model/goals.toml', f'id = "{g["id"]}"'

def _check_ids(sc, fl, ev, WAYS, GS, err):
    for kind, iid, item, path, needle in _iter_items(sc, fl, ev, WAYS, GS):
        _known(item.get('since'), path, needle, err, f'{kind} {iid} since')
        _known(item.get('until'), path, needle, err, f'{kind} {iid} until')
        if item.get('since') and item.get('until') and _bounds_ok(item):
            if M.pindex(item['since']) > M.pindex(item['until']):
                err(path, needle, f'{kind} {iid}: since {item["since"]!r} is after until {item["until"]!r}')

def _check_legacy_phase_key(sc, fl, ev, WAYS, GS, err):
    for kind, iid, item, path, needle in _iter_items(sc, fl, ev, WAYS, GS):
        if 'phase' in item and kind != 'link':
            err(path, 'phase =', f'{kind} {iid}: use since=/until= phase ids, not phase = {item["phase"]!r}')

def _check_monotonic(sc, fl, ev, WAYS, GS, err):
    """Available in an earlier phase but not a later one requires until= or a later hide. [M1047-draft]"""
    hide_later = {ph['id']: {h if isinstance(h, str) else h.get('of') for h in (ph.get('hide') or [])} for ph in M.PHASES}
    for kind, iid, item, path, needle in _iter_items(sc, fl, ev, WAYS, GS):
        if kind == 'link':
            # a link disappearing later is OK if until is set (or owner screen ends)
            av = [p for p in M.PIDS if M.in_phase(item, p)]
            if not av: continue
            missing = [p for p in M.PIDS if M.pindex(p) > M.pindex(av[0]) and p not in av]
            if missing and not item.get('until'):
                err(path, needle, f'link {iid} is available in {av[0]} but not {missing[0]} without until= (monotonic unless explicit until/hide/replace)')
            continue
        av = [p for p in M.PIDS if M.in_phase(item, p)]
        if not av: continue
        for p in M.PIDS:
            if M.pindex(p) <= M.pindex(av[0]): continue
            if M.in_phase(item, p): continue
            # disappeared: must have until or be hidden in this or an earlier-later phase
            hidden = any(iid in hide_later[q] for q in M.PIDS if M.pindex(q) <= M.pindex(p) and M.pindex(q) > M.pindex(av[0]))
            if not item.get('until') and not hidden:
                err(path, needle, f'{kind} {iid} is available in {av[0]} but not {p} without until= or a hide in phases.toml')

def _check_targets(sc, ev, err):
    """Links and events available in a phase may only target screens available in it."""
    for sid,s in sc.items():
        for l in s.get('links') or []:
            to=l.get('to')
            if not to or to not in sc: continue
            for ph in M.PIDS:
                if not M.in_phase(s, ph) or not M.in_phase(l, ph): continue
                if not M.in_phase(sc[to], ph):
                    err(s['_file'], f'id = "{l["id"]}"', f'link {sid}:{l["id"]} is available in {ph} but targets {to}, which is not')
    for e in ev.get('events') or []:
        to=e.get('to')
        if not to or to not in sc: continue
        for ph in M.PIDS:
            if not M.in_phase(e, ph): continue
            if not M.in_phase(sc[to], ph):
                err(ev['_file'], f'id = "{e["id"]}"', f'event {e["id"]} is available in {ph} but targets {to}, which is not')

def _check_flow_screens(sc, fl, err):
    """A flow walked in its walk phase may only step on screens available in that phase."""
    for fid,f in fl.items():
        ph=M.flow_phase(f)
        try:
            steps=M.flow_states(sc,f)
        except Exception:
            continue
        for i,(_,scs) in enumerate(steps):
            for s in scs:
                if s in sc and not M.in_phase(sc[s], ph):
                    err(f['_file'], '[[steps]]', f'flow {fid} walked in {ph} step {i+1} uses {s}, not available in that phase',)

def _check_delta(sc, fl, ev, WAYS, GS, err):
    """Items whose since is a later phase must be listed in that phase's add."""
    listed={}
    for ph in M.PHASES:
        add=set()
        for a in ph.get('add') or []:
            add.add(a if isinstance(a,str) else a.get('id') or a.get('of'))
        listed[ph['id']]=add
    first=M.PIDS[0]
    seen_ids=set()
    for kind, iid, item, path, needle in _iter_items(sc, fl, ev, WAYS, GS):
        if kind == 'link': continue
        if kind == 'flow' and item.get('parent'): continue
        s=item.get('since')
        if not s or not _bounds_ok(item): continue
        if M.pid(s)==first: continue
        if iid in listed.get(M.pid(s), ()): continue
        # allow if already reported (screen and flow sharing an id, etc.)
        key=(M.pid(s), iid)
        if key in seen_ids: continue
        seen_ids.add(key)
        err(M.PHASES_FILE, 'add =', f'{kind} {iid} has since={s} but is not in that phase\'s add list in phases.toml')

def _check_rules(sc, ev, err):
    evs={e['id']:e for e in ev.get('events') or []}
    for ph in M.PIDS:
        for rule in M.phase_rules(ph):
            if rule in RULE_SCREENS:
                for sid in RULE_SCREENS[rule]:
                    if sid in sc and M.in_phase(sc[sid], ph):
                        err(sc[sid]['_file'], 'since =' if sc[sid].get('since') else 'id =',
                            f'rule {rule} holds in {ph} but screen {sid} is still available')
            if rule == 'no-building-mode':
                if M.dmode('none', ph) != 'live':
                    err(M.PHASES_FILE, 'rules', f'rule no-building-mode holds in {ph} but Building mode is the default tab')
                if 'home' in sc:
                    for l in sc['home'].get('links') or []:
                        if l.get('id')=='building' and M.in_phase(l, ph):
                            err(sc['home']['_file'], 'id = "building"', f'rule no-building-mode holds in {ph} but home:building is available')
            if rule == 'no-size-limit' and 'postup-fills' in evs and M.in_phase(evs['postup-fills'], ph):
                err(ev['_file'], 'id = "postup-fills"', f'rule no-size-limit holds in {ph} but event postup-fills is available')
            if rule == 'no-share' and 'share' in sc:
                for sid,s in sc.items():
                    if not M.in_phase(s, ph): continue
                    for l in s.get('links') or []:
                        if l.get('to')=='share' and M.in_phase(l, ph):
                            err(s['_file'], f'id = "{l["id"]}"', f'rule no-share holds in {ph} but {sid}:{l["id"]} still opens share')
            if rule not in RULE_SCREENS and rule not in ('no-building-mode','no-size-limit','no-share'):
                err(M.PHASES_FILE, 'rules', f'unknown named rule {rule!r} on phase {ph}')

def _check_way_path(fl, WAYS, US, err):
    """A way available in a phase should have a modeled path also available in that phase, unless excepted."""
    # Map way id -> flows/outcomes that use it
    used={}
    for f in fl.values():
        if f.get('parent'): continue
        if f.get('way'):
            used.setdefault(f['way'], []).append(f)
        for o in f.get('outcomes') or []:
            if o.get('way'):
                # expanded child id
                cid=f'{f["id"]}--{o["id"]}'
                used.setdefault(o['way'], []).append(fl.get(cid) or {**o, 'id':cid, '_file':f['_file']})
    for wid,w in WAYS.items():
        for ph in M.PIDS:
            if not M.in_phase(w, ph): continue
            paths=used.get(wid) or []
            has=any(M.in_phase(p, ph) for p in paths)
            if has: continue
            x=_exc('way-path-in-phase', wid, ph)
            if x:
                _need_reason(err, M.PHASES_FILE, 'reason =', x)
                continue
            err(w.get('_file') or 'model/ways.toml', f'id = "{wid}"',
                f'way {wid} is available in {ph} but no flow or outcome for it is; add a path or a source-tagged [[exceptions]] check="way-path-in-phase"')

def _check_deliverable_goals(sc, fl, US, WAYS, GS, err):
    """Each phase's deliverable goals are reachable (same logic as goal_reachability)."""
    import goal_reachability as GR
    cfg=GR.default_config()
    cfg['phases']=list(M.PIDS)
    cfg['skips']=[]
    spread=GR.build_spread(sc, fl, US, WAYS, GS, cfg)
    # explicit failures
    for case in spread['cases']:
        ph=case['phase']
        if case['goal'] not in M.phase_goals(ph):
            continue
        if not M.in_phase(WAYS[case['way']], ph):
            continue
        result=GR.check_case(sc, fl, US, WAYS, GS, case)
        if result['status']=='failed':
            err(M.PHASES_FILE, 'deliverable',
                f'deliverable goal {case["goal"]} fails for {case["id"]}: {result.get("detail") or result.get("skip_reason")}')
    # a listed deliverable goal must have at least one passing case in that phase
    for ph in M.PIDS:
        for gid in M.phase_goals(ph):
            cases=[c for c in spread['cases'] if c['phase']==ph and c['goal']==gid and M.in_phase(WAYS[c['way']], ph)]
            passed=0
            for c in cases:
                if GR.check_case(sc, fl, US, WAYS, GS, c)['status']=='passed':
                    passed+=1
            if passed==0:
                err(M.PHASES_FILE, 'deliverable',
                    f'deliverable goal {gid} has no reachable passing case in {ph}')
