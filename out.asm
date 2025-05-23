# variables
.data

  # v - global
  vary: .word 0
  
  # v - test
  testvary: .word 0
  
  # v - main
  mvarx: .word 0
  
.text
.globl main

functest:
  move $fp $sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

  # constante
  li $a0 1

  sw $a0 testvary
  lw $a0 testvary
  # output
  li $v0 1
  syscall

  
  # end function
  lw $ra 4($sp)
  addiu $sp $sp 8
  lw $fp 0($sp)
  jr $ra

main:
  # constante
  li $a0 2

  sw $a0 vary
  # constante
  li $a0 3

  sw $a0 mvarx
  lw $a0 vary
  # output
  li $v0 1
  syscall

  lw $a0 mvarx
  # output
  li $v0 1
  syscall

  sw $fp 0($sp)
  addiu $t2 $sp -4
  move $sp $t2
  jal functest
  lw $a0 vary
  # output
  li $v0 1
  syscall

  # end call
  li $v0 10
  syscall

