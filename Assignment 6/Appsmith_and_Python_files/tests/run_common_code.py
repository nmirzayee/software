"""Run the common test suite against a code-based implementation.

Usage: python3 run_common_code.py <project_dir> <out.json>
"""
import importlib.util, json, os, sys

proj, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common_cases import CASES

spec = importlib.util.spec_from_file_location("app", os.path.join(proj, "main.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

results = []
print(f"Common test suite against {os.path.abspath(proj)}/main.py\n")
for c in CASES:
    data = []
    for course, title in c["pre"]:
        app.add_assignment(data, course, title)
    before = [d.copy() for d in data]
    try:
        msg = app.add_assignment(data, c["course"], c["title"])
        stored = True
    except ValueError as e:
        msg = str(e)
        stored = False
    ok = (stored == c["stored"] and msg == c["msg"] and len(data) == c["count"])
    if c["stored"]:
        ok = ok and (data[-1]["course"], data[-1]["title"]) == tuple(c["store_as"])
    else:
        ok = ok and data == before
    results.append(dict(id=c["id"], stored=stored, msg=msg, count=len(data),
                        last=data[-1] if data else None, passed=ok))
    print(f"{c['id']}  {'PASS' if ok else 'FAIL'}  stored={stored!s:5}  count={len(data)}  msg={msg!r}")
print(f"\n{sum(r['passed'] for r in results)}/{len(results)} passed")
json.dump(results, open(out, "w"), indent=1)
