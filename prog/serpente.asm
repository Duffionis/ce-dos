; Serpente: gioco VGA 13h con timer (INT 8) e tastiera (INT 9) agganciati. Frecce per muoversi, Esc per uscire.
; Codice di uscita = lunghezza del serpente.
org 100h
  mov ax,3508h
  int 21h
  mov [old8],bx
  mov [old8+2],es
  mov ax,3509h
  int 21h
  mov [old9],bx
  mov [old9+2],es
  push cs
  pop ds
  mov ax,2508h
  mov dx,isr8
  int 21h
  mov ax,2509h
  mov dx,isr9
  int 21h
  mov ax,13h
  int 10h
  mov ax,0A000h
  mov es,ax

  ; stato iniziale: lunghezza 3, testa a (12,12)
  mov byte [lung],3
  mov byte [testa],2
  mov byte [coda],0
  mov byte [sx+0],10
  mov byte [sx+1],11
  mov byte [sx+2],12
  mov byte [sy+0],12
  mov byte [sy+1],12
  mov byte [sy+2],12
  mov byte [dirx],1
  mov byte [diry],0
  mov byte [mela_x],20
  mov byte [mela_y],12
  mov bl,10
  mov cx,3
  xor si,si
dis0:
  mov al,[sx+si]
  mov ah,[sy+si]
  mov bl,10
  call cella
  inc si
  loop dis0
  mov al,[mela_x]
  mov ah,[mela_y]
  mov bl,12
  call cella

principale:
  cmp byte [key],1          ; Esc
  je fine
  mov al,[key]
  cmp al,48h
  jne n1
  cmp byte [diry],1
  je n1
  mov byte [dirx],0
  mov byte [diry],-1
n1: cmp al,50h
  jne n2
  cmp byte [diry],-1
  je n2
  mov byte [dirx],0
  mov byte [diry],1
n2: cmp al,4Bh
  jne n3
  cmp byte [dirx],1
  je n3
  mov byte [dirx],-1
  mov byte [diry],0
n3: cmp al,4Dh
  jne n4
  cmp byte [dirx],-1
  je n4
  mov byte [dirx],1
  mov byte [diry],0
n4:
  cmp byte [ticks],2
  jb principale
  mov byte [ticks],0
  ; nuova testa
  xor bx,bx
  mov bl,[testa]
  mov al,[sx+bx]
  add al,[dirx]
  cmp al,40
  jb okx
  jl_wrap:
  cmp al,200
  jae xneg
  xor al,al
  jmp okx
xneg: mov al,39
okx: mov dl,al
  mov al,[sy+bx]
  add al,[diry]
  cmp al,25
  jb oky
  cmp al,200
  jae yneg
  xor al,al
  jmp oky
yneg: mov al,24
oky: mov dh,al              ; dl=x, dh=y
  ; collisione con il corpo
  xor si,si
  mov cl,[lung]
  xor ch,ch
col:
  push bx
  mov bx,si
  add bl,[coda]
  mov al,[sx+bx]
  cmp al,dl
  jne nocol
  mov al,[sy+bx]
  cmp al,dh
  jne nocol
  pop bx
  jmp fine
nocol:
  pop bx
  inc si
  loop col
  ; avanza testa
  inc byte [testa]
  mov bl,[testa]
  xor bh,bh
  mov [sx+bx],dl
  mov [sy+bx],dh
  mov al,dl
  mov ah,dh
  push ax
  mov bl,10
  call cella
  pop ax
  ; mela?
  cmp al,[mela_x]
  jne nomela
  cmp ah,[mela_y]
  jne nomela
  inc byte [lung]
  ; nuova mela (generatore congruenziale)
  mov ax,[seme]
  mov dx,25173
  mul dx
  add ax,13849
  mov [seme],ax
  mov bl,40
  xchg ah,al
  xor ah,ah
  div bl
  mov [mela_x],ah
  mov ax,[seme]
  xor al,al
  xchg al,ah
  mov bl,25
  div bl
  mov [mela_y],ah
  mov al,[mela_x]
  mov ah,[mela_y]
  mov bl,12
  call cella
  jmp principale
nomela:
  ; cancella la coda
  xor bx,bx
  mov bl,[coda]
  mov al,[sx+bx]
  mov ah,[sy+bx]
  xor bl,bl
  call cella
  inc byte [coda]
  jmp principale

fine:
  mov ax,2508h
  lds dx,[old8]
  int 21h
  mov ax,2509h
  lds dx,[old9]
  int 21h
  push cs
  pop ds
  mov ax,3
  int 10h
  mov al,[lung]
  mov ah,4Ch
  int 21h

; disegna la cella (al=x, ah=y) col colore bl
cella:
  push ax
  push bx
  push cx
  push di
  push dx
  mov [cs:colore],bl
  xor bh,bh
  mov bl,ah
  mov ah,0
  mov cl,3
  shl ax,cl                  ; x*8
  mov di,ax
  mov ax,bx
  mov bx,2560                ; 8*320
  mul bx
  add di,ax
  mov al,[cs:colore]
  mov dx,8
riga:
  mov cx,8
  rep stosb
  add di,312
  dec dx
  jnz riga
  pop dx
  pop di
  pop cx
  pop bx
  pop ax
  ret

isr8:
  push ax
  inc byte [cs:ticks]
  pop ax
  jmp far [cs:old8]
isr9:
  push ax
  in al,60h
  mov [cs:key],al
  mov al,20h
  out 20h,al
  pop ax
  iret

old8 dw 0,0
old9 dw 0,0
ticks db 0
key db 0
lung db 0
testa db 0
coda db 0
dirx db 0
diry db 0
mela_x db 0
mela_y db 0
seme dw 12345
colore db 0
sx times 256 db 0
sy times 256 db 0
