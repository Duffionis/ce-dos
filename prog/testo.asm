org 100h
  mov ax,3
  int 10h
  mov dx,2
  mov ah,2
  xor bh,bh
  mov dx,0A14h        ; riga 10, colonna 20
  int 10h
  mov ah,9
  mov dx,msg
  int 21h
  mov ah,4Ch
  int 21h
msg db 'Schermo 80x25 in Ce++$'
