# variables
.data

  # v - global
  
  # v - test
  
  # v - main
  mvary: .word 0
  
.text
.globl main

functest:
  move $fp $sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

  addiu $sp $sp -40
  # constante
  li $a0 4

  #Escritura arreglo testvarc
  # indice
  # constante
  li $a0 1

  move $t1 $a0
  mul $t1 $t1 4
  addiu $t0 $fp -40
  add $t2 $t0 $t1
  sw $a0 0($t2)
  # indice
  # constante
  li $a0 1

  move $t1 $a0
  mul $t1 $t1 4
  addiu $t0 $fp -40
  add $t2 $t0 $t1
  lw $a0 0($t2)
  # output
  li $v0 1
  syscall

  
  # end function
  lw $ra 4($sp)
  addiu $sp $sp 48
  lw $fp 0($sp)
  jr $ra
main:
  addiu $sp $sp -40
  # constante
  li $a0 10

  #Escritura arreglo mvara
  # indice
  # constante
  li $a0 1

  move $t1 $a0
  mul $t1 $t1 4
  addiu $t0 $fp -40
  add $t2 $t0 $t1
  sw $a0 0($t2)
  # indice
  # constante
  li $a0 1

  move $t1 $a0
  mul $t1 $t1 4
  addiu $t0 $fp -40
  add $t2 $t0 $t1
  lw $a0 0($t2)
  # variable mvary
  sw $a0 mvary
  lw $a0 mvary
  # output
  li $v0 1
  syscall

  sw $fp 0($sp)
  addiu $t2 $sp -4
  move $sp $t2
  jal functest
  # end call
  li $v0 10
  syscall

