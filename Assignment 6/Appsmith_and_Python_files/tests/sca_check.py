"""SCA: inventory every import and confirm whether it is stdlib or third-party."""
import ast, sys, pathlib
for f in sys.argv[1:]:
    tree = ast.parse(pathlib.Path(f).read_text())
    mods = sorted({(n.names[0].name if isinstance(n, ast.Import) else n.module).split(".")[0]
                   for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)) and
                   (isinstance(n, ast.Import) or n.module)})
    for m in mods:
        kind = "stdlib" if m in sys.stdlib_module_names else ("local" if pathlib.Path(f).with_name(m + ".py").exists() else "THIRD-PARTY")
        print(f"{f:<22} {m:<14} {kind}")
print("\nrequirements files present:", [p.name for p in pathlib.Path('code').glob('*requirements*')] or "none")
print("Python runtime:", sys.version.split()[0])
