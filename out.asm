# variables
.data

  # v - global
  
  # v - main
  mvary: .word 0
  mvara: .space 20
  
.text
.globl main

main:
  # constante
  li $a0 20

  la $t0 mvara
  # constante
  li $a0 1

  mul $t1 $a0 4
  add $t0 $t0 $t1
  sw $a1 0($t0)  # escribe en array
  la $t0 mvara
  # constante
  li $a0 1

  move $t1 $a0  # index
  mul $t1 $t1 4
  add $t0 $t0 $t1
  lw $a0 0($t0)
  sw $a0 mvary
  # variable mvary
  lw $a0 mvary
  # output
  li $v0 1
  syscall

  # end call
  li $v0 10
  syscall

