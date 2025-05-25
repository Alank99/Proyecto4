# variables
.data

  # v - global
  
  # v - test
  testvary: .word 0
  testvara: .space 20
  
  # v - main
  mvary: .word 0
  mvara: .space 20
  mvarx: .word 0
  
.text
.globl main

functest:
  move $fp $sp
  sw $ra 0($sp)
  addiu	 $sp 	$sp 	-4
  # start function

  # conseguimos el indice 
  # constante
  li $a0 1

  # buscamos el lugar en el array
  mul $t0 $a0 4
  # guardamos el valor en la variable
  # constante
  li $a0 450

  sw $a0 testvara($t0)
  # fin variable array testvara
  # conseguimos el indice 
  # constante
  li $a0 0

  # buscamos el lugar en el array
  mul $t0 $a0 4
  # guardamos el valor en la variable
  # constante
  li $a0 350

  sw $a0 testvara($t0)
  # fin variable array testvara
  # constante
  li $a0 1

  mul $t0, $a0, 4
  lw $a0, testvara($t0)
  sw $a0 testvary
  # constante
  li $a0 1

  mul $t0, $a0, 4
  lw $a0, testvara($t0)
  # output
  li $v0 1
  syscall

  # constante
  li $a0 0

  mul $t0, $a0, 4
  lw $a0, testvara($t0)
  # output
  li $v0 1
  syscall

  # constante
  li $a0 2

  sw $a0 testvary
  # variable testvary
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
  li $a0 1

  sw $a0 mvarx
  # conseguimos el indice 
  # constante
  li $a0 1

  # buscamos el lugar en el array
  mul $t0 $a0 4
  # guardamos el valor en la variable
  # constante
  li $a0 20

  sw $a0 mvara($t0)
  # fin variable array mvara
  # conseguimos el indice 
  # constante
  li $a0 0

  # buscamos el lugar en el array
  mul $t0 $a0 4
  # guardamos el valor en la variable
  # constante
  li $a0 30

  sw $a0 mvara($t0)
  # fin variable array mvara
  # variable mvarx
  lw $a0 mvarx
  mul $t0, $a0, 4
  lw $a0, mvara($t0)
  sw $a0 mvary
  # constante
  li $a0 1

  mul $t0, $a0, 4
  lw $a0, mvara($t0)
  # output
  li $v0 1
  syscall

  # constante
  li $a0 0

  mul $t0, $a0, 4
  lw $a0, mvara($t0)
  # output
  li $v0 1
  syscall

  # constante
  li $a0 2

  sw $a0 mvary
  # variable mvary
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

