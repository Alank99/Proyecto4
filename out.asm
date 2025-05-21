# variables
.data

  # v - global
  
  # v - test
  vara: .word 0
  
  # v - main
  
.text
.globl main

functest:
  move	 $fp 	$sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

  lw $a0 vara
  # output
  li $v0 1
  syscall

  
  # end function
  lw $ra 4($sp)
  addiu $sp $sp 12
  lw $fp 0($sp)
  jr $ra
main:
  sw $fp 0($sp)
  addiu 	$sp 	$sp 	-4
  # param None
  # constante
  li $a0 1

  # save param
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  jal functest
  sw $fp 0($sp)
  addiu 	$sp 	$sp 	-4
  # param None
  # constante
  li $a0 2

  # save param
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  jal functest
  sw $fp 0($sp)
  addiu 	$sp 	$sp 	-4
  # param None
  # constante
  li $a0 3

  # save param
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  jal functest
  sw $fp 0($sp)
  addiu 	$sp 	$sp 	-4
  # param None
  # constante
  li $a0 4

  # save param
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  jal functest
  # end call
  li $v0 10
  syscall

