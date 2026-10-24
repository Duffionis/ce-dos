org 100h
  mov ah,9
  mov dx,chiedi
  int 21h
  xor ah,ah
  int 16h
  mov [ris],al
  mov ah,9
  mov dx,dato
  int 21h
  mov ah,4Ch
  xor al,al
  int 21h
chiedi db 'Premi un tasto: $'
dato db 'Hai premuto '
ris db '?',13,10,'$'
