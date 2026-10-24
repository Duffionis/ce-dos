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
r = subprocess.run(["./cedos", "prog/serpente.com", "--det", "--passi", "3000000", "--copione", "6:80,7:208", "--ppm", "/tmp/ce_dos_s.ppm"], cwd=RADICE, capture_output=True, text=True)
d = open("/tmp/ce_dos_s.ppm", "rb").read(); h = len(b"P6\n320 200\n255\n")
cella = lambda x, y: tuple(d[h + ((y * 8 + 4) * 320 + x * 8 + 4) * 3: h + ((y * 8 + 4) * 320 + x * 8 + 4) * 3 + 3])
verdi = [(x, y) for y in range(25) for x in range(40) if cella(x, y)[1] > 200 and cella(x, y)[0] < 100]
esito("serpente.com (INT 8 timer + INT 9 tastiera)", cella(20, 12)[0] > 200 and len(verdi) == 3 and len({x for x, y in verdi}) == 1, str(verdi))
r = subprocess.run(["./cedos", "prog/grafica.com", "--ppm", "/tmp/ce_dos_g.ppm"], cwd=RADICE, capture_output=True, text=True)
d = open("/tmp/ce_dos_g.ppm", "rb").read(); h = len(b"P6\n320 200\n255\n")
px = lambda x, y: tuple(d[h + (y * 320 + x) * 3: h + (y * 320 + x) * 3 + 3])
esito("grafica.com (VGA 13h + palette)", px(1, 0) == (255, 0, 0) and px(2, 5) == (0, 170, 0) and len(d) == h + 192000, str(px(1, 0)))
# tastiera viva: terminale vero (pty), il programma aspetta un tasto
try:
    import pty, select, time
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(RADICE); os.execv("./cedos", ["cedos", "prog/tasto.com", "--vivo"])
    def svuota(t):
        out, fine = b"", time.time() + t
        while time.time() < fine:
            p, _, _ = select.select([fd], [], [], 0.05)
            if p:
                try: out += os.read(fd, 65536)
                except OSError: break
        return out
    a = svuota(1.0); os.write(fd, b"k"); b = svuota(1.0)
    st = os.waitpid(pid, os.WNOHANG)
    if st[0] == 0: os.kill(pid, 9)
    esito("tasto.com (--vivo, tastiera)", b"Premi un tasto" in a and b"Hai premuto k" in b and st[0] != 0 and os.WEXITSTATUS(st[1]) == 0)
except ImportError:
    print("saltato  tastiera viva (manca pty)")
import shutil
if shutil.which("pkg-config") and subprocess.run(["pkg-config", "--exists", "sdl2"]).returncode == 0:
    r = subprocess.run([CE, "esegui", "src/finestra.ce", "-l", "SDL2", "prog/grafica.com", "20"], cwd=RADICE,
                       capture_output=True, text=True, env=dict(os.environ, SDL_VIDEODRIVER="dummy"))
    esito("finestra SDL2 (driver finto)", r.returncode == 0, r.stderr[:300])
else:
    print("saltato  finestra SDL2 (manca libsdl2-dev)")
if "--conformita" in sys.argv or os.environ.get("CE_CONFORMITA"):
    r = comp("prova86.ce", "prova86"); esito("compilazione prova86", r.returncode == 0, r.stderr[:400])
    r = subprocess.run(["tools/tutti.sh"] + [x for x in sys.argv[1:] if not x.startswith("--")] , cwd=RADICE, capture_output=True, text=True)
    for riga in r.stdout.splitlines():
        if ": " in riga and "non scaricabile" not in riga:
            n, e = riga.split(": ", 1)
            a, _, b = e.strip().partition("/")
            esito("8086 " + n, a.isdigit() and a == b, e[:100])
print(f"\n{ok} riusciti, {ko} falliti"); sys.exit(1 if ko else 0)
