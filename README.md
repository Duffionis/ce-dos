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

## Interruzioni hardware (come un vero gioco)
Un "BIOS" minimo sta a F000:0000: ogni vettore parte puntato a uno stub. Il timer (INT 8, ~18,2 Hz dall'orologio vero,
conta anche in 0040:006C) e la tastiera (INT 9, porta 60h con scancode di pressione e rilascio) sono consegnati ai
programmi che li agganciano, come su un PC. `prog/serpente.com` (gioco VGA, sorgente `serpente.asm`) li usa:

    ./ce esegui src/finestra.ce -l SDL2 prog/serpente.com      # frecce per muoversi, Esc esce, F12 chiude la finestra

Per le prove automatiche: `--det` (il tempo conta le istruzioni), `--copione "tick:scancode,..."`, `--passi N`, `--ppm file`.
Dal 386 c'e' solo `0F 80..8F` (salti condizionali near).

## Interattivo
    ./cedos programma.com --vivo        # terminale: schermo 80x25 che si aggiorna, tastiera in tempo reale (Ctrl-] esce)
    ./ce esegui src/finestra.ce -l SDL2 prog/grafica.com    # finestra SDL2 per la grafica 13h (sul tuo PC, non in un Codespace)

## Non fatto ancora
directory e memoria DOS (INT 21h 48h-4Ah), testo nella finestra SDL (serve un font), 286/386, suono.

Nessun BIOS, ROM o chiave e' incluso. Le prove di conformita' si scaricano da SingleStepTests.
