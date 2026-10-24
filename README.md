# ce-dos

Un emulatore 8086 + servizi DOS "alla DOSBox", scritto in **Ce++** (il linguaggio italiano per sistemi: https://github.com/Duffionis/Ce-).

- `src/cpu86.ce`: la CPU 8086 completa (tutti gli opcode, flag, stringhe, BCD, mul/div).
- `src/dos.ce`: le interruzioni DOS/BIOS servite dall'ospite (INT 21h testo/tastiera/uscita/file 3Ch-42h, INT 10h teletype, INT 16h, INT 1Ah, INT 20h) e i caricatori `.COM` e `.EXE` (rilocazione MZ).
- `src/prova86.ce` + `tools/`: verifica contro i test di riferimento **SingleStepTests/8088** (scaricati, non inclusi).

## Uso
    ./ce compila src/principale.ce -o cedos
    ./cedos prog/ciao.com
    echo "ciao" | ./cedos prog/eco.com

I programmi di prova si ricompilano con `nasm -f bin prog/ciao.asm -o prog/ciao.com`.

## Conformita' (tutti gli opcode)
    python3 tests/prova.py --conformita        # scarica ~300 file di test e li esegue

Stato: tutti gli opcode documentati passano 10.000/10.000 prove, tranne
DIV/IDIV (F6/F7 /6 /7): gli esiti normali sono giusti, ma sull'errore di divisione i
flag "indefiniti" spinti sullo stack non imitano il chip. Cicli e coda di prefetch non sono emulati.

## Schermo
    ./cedos prog/testo.com --schermo        # schermo testo 80x25 (B800:0000), stampato alla fine
    ./cedos prog/grafica.com --ppm out.ppm  # VGA modo 13h (A000:0000) + palette DAC, salvato come immagine
La palette predefinita e' un'approssimazione di quella VGA (i primi 16 colori sono quelli veri).

## Non fatto ancora
directory e memoria DOS (INT 21h 48h-4Ah), finestra in tempo reale (SDL), 286/386, suono.

Nessun BIOS, ROM o chiave e' incluso. Le prove di conformita' si scaricano da SingleStepTests.
