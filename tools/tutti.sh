#!/bin/bash
# scarica (una volta) e prova i file di opcode di SingleStepTests/8088. Senza argomenti: tutti.
# Argomenti: opcode in esadecimale (es. 27 80 F6)
cd "$(dirname "$0")/.."
mkdir -p t
[ -f t/meta.json ] || curl -sSL -o t/meta.json https://raw.githubusercontent.com/SingleStepTests/8088/main/v2/metadata.json
elenco=$(python3 -I - "$@" <<'PY'
import json, sys
m = json.load(open('t/meta.json'))['opcodes']
ops = sys.argv[1:] or ['%02X' % i for i in range(256)]
for op in ops:
    e = m.get(op)
    if e is None:
        continue
    if 'reg' in e:
        for n, x in sorted(e['reg'].items()):
            if x.get('status') != 'undocumented':
                print('%s.%s %d' % (op, n, x.get('flags-mask', 65535)))
    elif e.get('status') in ('normal', 'alias', None):
        print('%s %d' % (op, e.get('flags-mask', 65535)))
PY
)
echo "$elenco" | while read nome mask; do
  [ -z "$nome" ] && continue
  [ -f t/$nome.json.gz ] || curl -sSfL -o t/$nome.json.gz https://raw.githubusercontent.com/SingleStepTests/8088/main/v2/$nome.json.gz || { echo "$nome: non scaricabile"; continue; }
  python3 -I tools/converti.py t/$nome.json.gz t/$nome.bin $mask
  echo -n "$nome: "; ./prova86 t/$nome.bin | tail -4 | tr '\n' ' '; echo
  rm -f t/$nome.bin
done
