	.file	"if.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
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
.LFB11:
	.cfi_startproc
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	leaq	12(%rsp), %rsi
	movl	$.LC0, %edi
	movl	$0, %eax
	call	__isoc99_scanf
	movl	12(%rsp), %eax
	cmpl	$1, %eax
	jne	.L2
	movl	$.LC1, %edi
	call	puts
	jmp	.L3
.L2:
	cmpl	$2, %eax
	jne	.L4
	movl	$.LC2, %edi
	call	puts
	jmp	.L3
.L4:
	cmpl	$3, %eax
	jne	.L3
	movl	$.LC3, %edi
	call	puts
.L3:
	movl	$0, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE11:
	.size	main, .-main
	.ident	"GCC: (Debian 4.9.2-10) 4.9.2"
	.section	.note.GNU-stack,"",@progbits
