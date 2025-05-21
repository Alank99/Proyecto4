# variables
.data

  # v - global
  
  # v - recursion
  vara: .word 0
  
  # v - main
  
.text
.globl main

funcrecursion:
  move $fp $sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

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
  addiu $t1 $sp -4
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
  sw $a0 0($t1)
  addiu $t1 $t1 -4

  move $sp $t1
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
  sw $fp 0($sp)
  addiu $t1 $sp -4
  # param None
  # constante
  li $a0 0

  # save param
  sw $a0 0($t1)
  addiu $t1 $t1 -4

  move $sp $t1
  jal funcrecursion
  # end call
  li $v0 10
  syscall

