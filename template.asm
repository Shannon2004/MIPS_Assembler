#run in linux terminal by java -jar Mars4_5.jar nc filename.asm(take inputs from console)

#system calls by MARS simulator:
#http://courses.missouristate.edu/kenvollmar/mars/help/syscallhelp.html
.data
	next_line: .asciiz "\n"
	inp_statement: .asciiz "Enter No. of integers to be taken as input: "
	inp_int_statement: .asciiz "Enter starting address of inputs(in decimal format): "
	out_int_statement: .asciiz "Enter starting address of outputs (in decimal format): "
	enter_int: .asciiz "Enter the integer: "	
.text
#input: N= how many numbers to sort should be entered from terminal. 
#It is stored in $t1
jal print_inp_statement	
jal input_int 
move $t1,$t4			

#input: X=The Starting address of input numbers (each 32bits) should be entered from
# terminal in decimal format. It is stored in $t2
jal print_inp_int_statement
jal input_int
move $t2,$t4

#input:Y= The Starting address of output numbers(each 32bits) should be entered
# from terminal in decimal. It is stored in $t3
jal print_out_int_statement
jal input_int
move $t3,$t4 

#input: The numbers to be sorted are now entered from terminal.
# They are stored in memory array whose starting address is given by $t2
move $t8,$t2
move $s7,$zero	#i = 0
loop1:  beq $s7,$t1,loop1end
	jal print_enter_int
	jal input_int
	sw $t4,0($t2)
	addi $t2,$t2,4
      	addi $s7,$s7,1
        j loop1      
loop1end: move $t2,$t8       
#############################################################
#Do not change any code above this line
#Occupied registers $t1,$t2,$t3. Don't use them in your sort function.
#############################################################
#function: should be written by students(sorting function)
#The below function adds 10 to the numbers. You have to replace this with
#your code
#implementing a simple bubble sort algorithm to sort the numbers in increasing order
add $t4,$t1,$0 #stores 'n'(number of inputs) value
addi $t4,$t4,-1 #stores n-1
addi $t7,$0,0 #the contorl variable i for the outer loop
beq $t4,$0,skiploop#if number of elements is 1,then no need to enter the loop at all
outerfor:#this loop acts as the outer for loop
	beq $t7,$t4,done #the terminating condition(when i=n-1)
	add $t5,$t2,$0 #starting address of input values
	add $t6,$t3,$0 #starting address of output values
	addi $t8,$0,0 #the control variable j for the inner loop
	sub $s0,$t4,$t7 #the terminating value for the inner loop (n-1-i)
	innerloop: #acts like the inner for loop
		beq $t8,$s0,innerloopdone #if j=n-1-i,then we must break out of the inner loop as the inner loop runs n-i-1 times
		lw $s1,0($t5) #s1 stores one element
		lw $s2,4($t5)
		slt $t9,$s2,$s1
		 bne $t9,0,swap#s2 stores the element adjacent to s1
		#blt $s2,$s1,swap #if s2<s1,then it means that we have to swap them.
		return_from_swap:
		addi $t5,$t5,4 #increments address contained in t5 by 4 inorder to compare the next pair of adjacent elements
		addi $t8,$t8,1 #increments j by 1
		j innerloop	#again calls the innerloop and keeps executing as long as j<n-i-1
	swap: #swaps two values
		sw $s2,0($t5) #puts s2's value in the memory space that contained s1
		sw $s1,4($t5) #puts s1's value in the memory space that contained s2
		j return_from_swap #after the swap is done,we need to continue our inner loop iteration. Hence we goto return from swap
	innerloopdone: #this block is executed once the innerloop is run completely for a particular value of i
		addi $t7,$t7,1 #this increments i by 1
		add $s3,$s0,$0 #$s0 contains 'n-1-i'and I'm copying it into $s3
		sll $s3,$s3,2	#doing shift left logical by 2 so that s3 becomes s3*4(eg: if s3 was 2, s3<<2=8 (note:memory is byte addressable)
		add $t6,$t6,$s3 #$t6 contains base address of output . So since largest element goes to the end at each iteration of the innerloop,and since we are trying to store in increasing order, we are making t6=t6+s3
		lw $s6,0($t5)#loading the number at memory[t5] to s6(since $t5 will be the address of the element that is the largest after each iteration)
		sw $s6,0($t6)#writing the loaded number into t6.
		sub $t6,$t6,$s3 #regaining the original value of t6 by subtracting s3 from it.
		j outerfor #calling the outer forloop again
done:#this block is executed once the outer for loop is done executing	
	lw $s6,-4($t5)#(Note:$t5-4 contains the lightest element and hence,we are writing this to $s6
	sw $s6,0($t6)#Storing the element in memory[$t6] which is nothing but the starting address of the output.
	j stop
skiploop:#this will just store whatever is in address $t2 to address $t3
	lw $s6,0($t2)
	sw $s6,0($t3)
stop:	#signifies the end of the program	
#Now,the numbers entered have been completely sorted in ascending order	
#endfunction
#############################################################
#You need not change any code below this line

#print sorted numbers
move $s7,$zero	#i = 0
loop: beq $s7,$t1,end
      lw $t4,0($t3)
      jal print_int
      jal print_line
      addi $t3,$t3,4
      addi $s7,$s7,1
      j loop 
#end
end:  li $v0,10
      syscall
#input from command line(takes input and stores it in $t6)
input_int: li $v0,5
	   syscall
	   move $t4,$v0
	   jr $ra
#print integer(prints the value of $t6 )
print_int: li $v0,1	
	   move $a0,$t4
	   syscall
	   jr $ra
#print nextline
print_line:li $v0,4
	   la $a0,next_line
	   syscall
	   jr $ra

#print number of inputs statement
print_inp_statement: li $v0,4
		la $a0,inp_statement
		syscall 
		jr $ra
#print input address statement
print_inp_int_statement: li $v0,4
		la $a0,inp_int_statement
		syscall 
		jr $ra
#print output address statement
print_out_int_statement: li $v0,4
		la $a0,out_int_statement
		syscall 
		jr $ra
#print enter integer statement
print_enter_int: li $v0,4
		la $a0,enter_int
		syscall 
		jr $ra
