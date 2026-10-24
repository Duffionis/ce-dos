org 100h
  mov ax,13h
  int 10h
  mov ax,0A000h
  mov es,ax
  xor di,di
  mov cx,64000
  cld
  xor dx,dx          ; riga
fill:
  mov ax,di
  xor dx,dx
  mov bx,320
  div bx             ; ax=y, dx=x
  mov al,dl          ; colore = x
  stosb
  loop fill
  ; palette: colore 1 = rosso pieno
  mov dx,3C8h
  mov al,1
  out dx,al
  inc dx
  mov al,63
  out dx,al
  xor al,al
  out dx,al
  out dx,al
  mov ax,4C00h
  int 21h
