# variables
.data

  # v - global
  
  # v - recursion
  recursionvara: .word 0
  recursionvarb: .word 0
  
  # v - main
  mvara: .word 0
  
.text
.globl main

funcrecursion:
  move $fp $sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

  # constante
  li $a0 9

  sw $a0 recursionvarb
  # variable recursionvarb
  lw $a0 recursionvarb
  # output
  li $v0 1
  syscall

  # if statement
  lw $a0 8($sp)
  sw $a0 0($sp)
  addiu $sp $sp -4
  # constante
  li $a0 5

  lw $t1 4($sp)
  slt $a0 $t1 $a0
  addiu $sp $sp 4
  beq $a0 $zero else_0
# if true
  lw $a0 8($sp)
  # output
  li $v0 1
  syscall

  sw $fp 0($sp)
  addiu $t2 $sp -4
  # param None
  lw $a0 8($sp)
  # sumar
  sw 	$a0 	0($sp)
  addiu 	$sp 	$sp 	-4

  # constante
  li $a0 1

  # suma - guardar resultado
  lw 	$t1 	4($sp)
  add 	$a0 	$t1 	$a0
  addiu 	$sp 	$sp 	4

  # save param
  sw $a0 0($t2)
  addiu $t2 $t2 -4

  move $sp $t2
  jal funcrecursion
  j fin_1

# if false
else_0:
  j fin_1

# end if
fin_1:
  
  # end function
  lw $ra 4($sp)
  addiu $sp $sp 12
  lw $fp 0($sp)
  jr $ra
main:
  # constante
  li $a0 2

  sw $a0 mvara
  sw $fp 0($sp)
  addiu $t2 $sp -4
  # param a
  # variable mvara
  lw $a0 mvara
  # save param
  sw $a0 0($t2)
  addiu $t2 $t2 -4

  move $sp $t2
  jal funcrecursion
  # constante
  li $a0 1

  # output
  li $v0 1
  syscall

  # end call
  li $v0 10
  syscall

