.data
  alo: .word 0
  
.text
.globl main

main:
  la $a0, alo
  li $v0, 1
  syscall

  li 	$v0, 	10
  syscall

