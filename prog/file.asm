org 100h
  mov ah,3Ch
  xor cx,cx
  mov dx,nome
  int 21h
  jc err
  mov bx,ax
  mov ah,40h
  mov cx,5
  mov dx,dati
  int 21h
  mov ah,3Eh
  int 21h
  mov ax,3D00h
  mov dx,nome
  int 21h
  jc err
  mov bx,ax
  mov ah,3Fh
  mov cx,5
  mov dx,buf
  int 21h
  mov cx,ax
  mov si,buf
p: lodsb
  mov dl,al
  mov ah,2
  int 21h
  loop p
  mov ah,3Eh
  int 21h
  mov ah,41h
  mov dx,nome
  int 21h
  mov ax,4C00h
  int 21h
err: mov ax,4C01h
  int 21h
nome db '/tmp/cedos_prova.txt',0
dati db 'DOS!!'
buf times 8 db 0
