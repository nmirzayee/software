"""Safe local runtime checks (DAST-style) against the CLI. Only our own process,
no network targets. Usage: python3 dast_cli.py <project_dir>"""
import random, subprocess, sys

proj = sys.argv[1]
random.seed(6)


def run(stdin, label):
    p = subprocess.run([sys.executable, "-B", "main.py"], cwd=proj, input=stdin,
                       capture_output=True, text=True, timeout=20)
    tb = "Traceback" in p.stderr
    esc = "\x1b" in p.stdout
    print(f"{label:<42} exit={p.returncode}  traceback={tb!s:5}  raw ESC echoed in output={esc}")
    return p

run("1\n" + "A" * 1_000_000 + "\nQuiz\n3\n", "1 MB course name")
run("1\nMath\n" + "\x00\x01\x02" + "\n3\n", "NUL / control bytes in title")
run("1\nMath\nLab\x1b[2J\x1b[31m FAKE\n2\n3\n", "ANSI escape in title, then View")
run("1\nMath\n{}{0}%s%n${7*7}\n2\n3\n", "format-string / template payloads")
run("1\nMath\n'; DROP TABLE x;--\n2\n3\n", "SQL-style payload (no DB)")
run("1\nMath\n", "EOF in the middle of input")
fuzz = "".join(random.choice("12 3\n\tabcXYZ!@#é\x1b") for _ in range(4000)) + "\n3\n"
run(fuzz, "random fuzz stream (4000 chars, seed 6)")
