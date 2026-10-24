#!/usr/bin/env python3
"""Prove di ce-dos: programmi .COM veri + (se c'e' rete) conformita' 8086 su alcuni opcode."""
import os, subprocess, sys
RADICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CE = os.path.join(RADICE, "ce")
ok = ko = 0
def esito(nome, bene, extra=""):
    global ok, ko
    if bene: ok += 1; print("ok      ", nome)
    else: ko += 1; print("FALLITO ", nome, extra)
def comp(src, out):
    return subprocess.run([CE, "compila", os.path.join("src", src), "-o", out], cwd=RADICE, capture_output=True, text=True)
r = comp("principale.ce", "cedos"); esito("compilazione emulatore", r.returncode == 0, r.stderr[:400])
if r.returncode: sys.exit(1)
r = subprocess.run(["./cedos", "prog/ciao.com"], cwd=RADICE, capture_output=True, text=True)
esito("ciao.com", r.stdout == "Ciao dal DOS in Ce++!\n54321" and r.returncode == 7, repr(r.stdout))
r = subprocess.run(["./cedos", "prog/eco.com"], cwd=RADICE, input="hello dos\n", capture_output=True, text=True)
esito("eco.com (tastiera)", r.stdout == "HELLO DOS\n", repr(r.stdout))
if "--conformita" in sys.argv or os.environ.get("CE_CONFORMITA"):
    r = comp("prova86.ce", "prova86"); esito("compilazione prova86", r.returncode == 0, r.stderr[:400])
    r = subprocess.run(["tools/tutti.sh"] + [x for x in sys.argv[1:] if not x.startswith("--")] , cwd=RADICE, capture_output=True, text=True)
    for riga in r.stdout.splitlines():
        if ": " in riga and "non scaricabile" not in riga:
            n, e = riga.split(": ", 1)
            a, _, b = e.strip().partition("/")
            esito("8086 " + n, a.isdigit() and a == b, e[:100])
print(f"\n{ok} riusciti, {ko} falliti"); sys.exit(1 if ko else 0)
