; piccolo .EXE: relocazione di un segmento dati
bits 16
hdr: db 'MZ'
 dw (fine-hdr) % 512, (fine-hdr + 511) / 512, 1, 2, 0, 0xFFFF, 0, 0x100, 0, 0, 0, 0x1C, 0
reloc: dw 0x0001, 0x0000      ; offset 1 nel segmento 0: il "mov ax, seg dati"
times 32-($-hdr) db 0
codice:
  mov ax,(dati-codice)/16 ; <- rilocato: diventa il segmento dei dati
  mov ds,ax
  mov ah,9
  mov dx,msg-dati
  int 21h
  mov ax,4C05h
  int 21h
align 16, db 0
dati:
msg db 'EXE rilocato ok',13,10,'$'
fine:
