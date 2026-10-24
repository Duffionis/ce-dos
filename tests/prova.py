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
r = subprocess.run(["./cedos", "prog/exe.exe"], cwd=RADICE, capture_output=True, text=True)
esito("exe.exe (rilocazione MZ)", r.stdout == "EXE rilocato ok\n" and r.returncode == 5, repr(r.stdout))
r = subprocess.run(["./cedos", "prog/file.com"], cwd=RADICE, capture_output=True, text=True)
esito("file.com (crea, scrive, legge, cancella)", r.stdout == "DOS!!" and r.returncode == 0, repr(r.stdout))
r = subprocess.run(["./cedos", "prog/testo.com", "--schermo"], cwd=RADICE, capture_output=True, text=True)
righe = r.stdout.split("\n")
esito("testo.com (schermo 80x25)", len(righe) > 10 and righe[10] == " " * 20 + "Schermo 80x25 in Ce++", repr(righe[10:11]))
r = subprocess.run(["./cedos", "prog/grafica.com", "--ppm", "/tmp/ce_dos_g.ppm"], cwd=RADICE, capture_output=True, text=True)
d = open("/tmp/ce_dos_g.ppm", "rb").read(); h = len(b"P6\n320 200\n255\n")
px = lambda x, y: tuple(d[h + (y * 320 + x) * 3: h + (y * 320 + x) * 3 + 3])
esito("grafica.com (VGA 13h + palette)", px(1, 0) == (255, 0, 0) and px(2, 5) == (0, 170, 0) and len(d) == h + 192000, str(px(1, 0)))
if "--conformita" in sys.argv or os.environ.get("CE_CONFORMITA"):
    r = comp("prova86.ce", "prova86"); esito("compilazione prova86", r.returncode == 0, r.stderr[:400])
    r = subprocess.run(["tools/tutti.sh"] + [x for x in sys.argv[1:] if not x.startswith("--")] , cwd=RADICE, capture_output=True, text=True)
    for riga in r.stdout.splitlines():
        if ": " in riga and "non scaricabile" not in riga:
            n, e = riga.split(": ", 1)
            a, _, b = e.strip().partition("/")
            esito("8086 " + n, a.isdigit() and a == b, e[:100])
print(f"\n{ok} riusciti, {ko} falliti"); sys.exit(1 if ko else 0)
