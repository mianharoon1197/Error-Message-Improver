section .data
x db 0
y db 0
z db 0
section .text
; declare x
mov %r0, int
mov x, %r0
; declare y
mov %r1, int
mov y, %r1
; declare z
mov %r2, int
mov abc, %r2
mov %r3, float
mov pi, %r3

; Function add
add:
mov %r4, int
mov eax, %r4
ret
ret
mov %r5, int
mov %r6, int
push %r5 ; arg0
push %r6 ; arg1
call add
add esp, 8
mov %r7, int
push %r7 ; arg0
call add
add esp, 4
L0:
mov %r8, int
cmp int, %r8
cmp int, 0
je L1
mov %r9, int
mov %r10, int
mov x, %r10
jmp L0
L1:
mov %r11, int
cmp int, %r11
cmp int, 0
je L2
mov %r12, int
mov %r13, int
mov x, %r13
jmp L3
L2:
mov %r14, int
mov %r15, int
mov x, %r15
L3: