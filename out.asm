# variables
.data

  # v - global
  vary: .word 0
  
  # v - main
  main_varx: .word 0
  
.text
.globl main

main:
  # constante
  li $a0 2

  sw $a0 vary
  # constante
  li $a0 3

  sw $a0 main_varx
  lw $a0 vary
  # output
  li $v0 1
  syscall

  lw $a0 main_varx
  # output
  li $v0 1
  syscall

  # end call
  li $v0 10
  syscall

