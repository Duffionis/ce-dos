org 100h
  mov ah,0Ah
  mov dx,buf
  int 21h
  mov bx,buf+2
  xor ch,ch
  mov cl,[buf+1]
  mov si,bx
r: lodsb
  cmp al,'a'
  jb s
  cmp al,'z'
  ja s
  sub al,32
s: mov dl,al
  mov ah,2
  int 21h
  loop r
  mov dl,10
  int 21h
  int 20h
buf db 40,0
  times 41 db 0
