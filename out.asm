# variables
.data

  # v - global
  
  # v - main
  a: .word 0
  
.text
.globl main

main:
  lw $a0 a
  # output
  li $v0 1
  syscall

  # end call
  li 	$v0 	10
  syscall

