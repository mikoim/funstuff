	.file	"if.c"
	.section	.rodata
.LC0:
	.string	"%d"
.LC1:
	.string	"ONE"
.LC2:
	.string	"TWO"
.LC3:
	.string	"THREE"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	movq	%rsi, -32(%rbp)
	leaq	-4(%rbp), %rax
	movq	%rax, %rsi
	movl	$.LC0, %edi
	movl	$0, %eax
	call	__isoc99_scanf
	movl	-4(%rbp), %eax
	cmpl	$1, %eax
	jne	.L2
	movl	$.LC1, %edi
	call	puts
	jmp	.L3
.L2:
	movl	-4(%rbp), %eax
	cmpl	$2, %eax
	jne	.L4
	movl	$.LC2, %edi
	call	puts
	jmp	.L3
.L4:
	movl	-4(%rbp), %eax
	cmpl	$3, %eax
	jne	.L3
	movl	$.LC3, %edi
	call	puts
.L3:
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Debian 4.9.2-10) 4.9.2"
	.section	.note.GNU-stack,"",@progbits
