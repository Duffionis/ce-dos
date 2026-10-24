#!/usr/bin/env python3
"""Converte un file di SingleStepTests/8088 (json) in un binario di parole u32 little-endian.
Per ogni prova: 14 registri iniziali, n, (indirizzo,valore)*n, 14 registri finali, m, (indirizzo,valore)*m, maschera.
Uso: converti.py ingresso.json[.gz] uscita.bin [maschera_flag]"""
import gzip, json, struct, sys

NOMI = ["ax", "bx", "cx", "dx", "cs", "ss", "ds", "es", "sp", "bp", "si", "di", "ip", "flags"]

def main():
    src, dst = sys.argv[1], sys.argv[2]
    maschera = int(sys.argv[3]) if len(sys.argv) > 3 else 65535
    aperto = gzip.open if src.endswith(".gz") else open
    with aperto(src, "rt") as f:
        prove = json.load(f)
    out = [len(prove), maschera]
    for p in prove:
        i, e = p["initial"], p["final"]
        ri = [i["regs"][n] for n in NOMI]
        rf = [e["regs"].get(n, i["regs"][n]) for n in NOMI]
        out += ri + [len(i["ram"])] + [x for a in i["ram"] for x in a]
        out += rf + [len(e["ram"])] + [x for a in e["ram"] for x in a]
    with open(dst, "wb") as f:
        f.write(struct.pack("<%dI" % len(out), *out))

main()
