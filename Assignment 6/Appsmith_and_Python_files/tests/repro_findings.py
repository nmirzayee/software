"""Reproduce candidate findings from the agentic code review (Task 5).
Usage: python3 repro_findings.py <project_dir>
"""
import importlib.util, os, subprocess, sys, unicodedata

proj = sys.argv[1]
spec = importlib.util.spec_from_file_location("app", os.path.join(proj, "main.py"))
app = importlib.util.module_from_spec(spec); spec.loader.exec_module(app)


def add(data, c, t):
    try:
        return "STORED: " + app.add_assignment(data, c, t)
    except ValueError as e:
        return "REJECTED: " + str(e)


print("F1  EOF on input (Ctrl+D / closed stdin) while adding an assignment")
p = subprocess.run([sys.executable, "-B", "main.py"], cwd=proj, input="1\nSoftware Engineering\n",
                   capture_output=True, text=True)
print("    exit code:", p.returncode, "| last stderr line:",
      (p.stderr.strip().splitlines() or ["<none>"])[-1])

print("F2  Terminal control / ANSI escape sequences accepted and echoed back")
data = []
evil = "Lab\x1b[2J\x1b[31m FAKE: grade=A"
print("   ", add(data, "Software Engineering", evil), "| stored repr:", repr(data[-1]["title"]) if data else None)
print("   ", add(data, "Math\nERROR: injected line", "Quiz"))

print("F3  Unicode canonical equivalence (NFC 'é' vs NFD 'e'+U+0301)")
data = []
nfc = unicodedata.normalize("NFC", "Café Project")
nfd = unicodedata.normalize("NFD", "Café Project")
print("   ", add(data, "Français", nfc))
print("   ", add(data, "Français", nfd), "| stored:", len(data), "records that look identical")
long_nfd = unicodedata.normalize("NFD", "é" * 30)
print("    30 visible 'é' typed decomposed ->", add([], long_nfd, "Essay"),
      "(len =", len(long_nfd), ")")

print("F4  Boundary values 30/80 not covered by unit tests")
src = open(os.path.join(proj, "test_main.py")).read()
print("    tests mention '* 30' or '* 80':", ("* 30" in src) or ("* 80" in src))

print("F5  Unbounded list growth (no maximum number of assignments)")
data = []
for i in range(20000):
    app.add_assignment(data, "Course", f"Task {i}")
print("    20000 assignments accepted; duplicate check is O(n) per add")

print("F6  Claimed 'SQL/command injection' risk")
print("    main.py uses sqlite/subprocess/eval/exec/os.system:",
      any(k in open(os.path.join(proj, "main.py")).read()
          for k in ("sqlite", "subprocess", "eval(", "exec(", "os.system")))
