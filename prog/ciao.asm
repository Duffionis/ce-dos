org 100h
  mov ah,9
  mov dx,msg
  int 21h
  mov cx,5
l: mov dl,'0'
  add dl,cl
  mov ah,2
  int 21h
  loop l
  mov ah,4Ch
  mov al,7
  int 21h
msg db 'Ciao dal DOS in Ce++!',13,10,'$'
