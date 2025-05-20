# variables
.data

  # v - global
  
  # v - main
  vara: .word 0
  varb: .word 0
  varc: .word 0
  
.text
.globl main

main:
  # input
  li $v0 5
  syscall
  move $a0 $v0

  sw $a0 vara
  # input
  li $v0 5
  syscall
  move $a0 $v0

  sw $a0 varb
  lw $a0 vara
  # output
  li $v0 1
  syscall

  lw $a0 varb
  # output
  li $v0 1
  syscall

  lw $a0 vara
  # sumar
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  lw $a0 varb
  # suma - guardar resultado
  lw 	$t1 	4 	($sp)
  add 	$a0 	$t1 	$a0
  addiu 	$sp 	$sp 	4

  sw $a0 varc
  lw $a0 varc
  # output
  li $v0 1
  syscall

  lw $a0 vara
  # sumar
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  lw $a0 varb
  # suma - guardar resultado
  lw 	$t1 	4 	($sp)
  add 	$a0 	$t1 	$a0
  addiu 	$sp 	$sp 	4

  # sumar
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  # constante
  li $a0 7

  # suma - guardar resultado
  lw 	$t1 	4 	($sp)
  add 	$a0 	$t1 	$a0
  addiu 	$sp 	$sp 	4

  sw $a0 varc
  lw $a0 varc
  # output
  li $v0 1
  syscall

  # end call
  li 	$v0 	10
  syscall

