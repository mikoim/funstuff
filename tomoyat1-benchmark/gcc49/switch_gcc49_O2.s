	.file	"switch.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"%d"
.LC1:
	.string	"ONE"
.LC2:
	.string	"TWO"
.LC3:
	.string	"THREE"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB4:
	.section	.text.startup,"ax",@progbits
.LHOTB4:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB11:
	.cfi_startproc
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	xorl	%eax, %eax
	movl	$.LC0, %edi
	leaq	12(%rsp), %rsi
	call	__isoc99_scanf
	movl	12(%rsp), %eax
	cmpl	$2, %eax
	je	.L3
	cmpl	$3, %eax
	je	.L4
	subl	$1, %eax
	je	.L8
.L2:
	xorl	%eax, %eax
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 8
	ret
.L8:
	.cfi_restore_state
	movl	$.LC1, %edi
	call	puts
	jmp	.L2
.L4:
	movl	$.LC3, %edi
	call	puts
	jmp	.L2
.L3:
	movl	$.LC2, %edi
	call	puts
	jmp	.L2
	.cfi_endproc
.LFE11:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE4:
	.section	.text.startup
.LHOTE4:
	.ident	"GCC: (Debian 4.9.2-10) 4.9.2"
	.section	.note.GNU-stack,"",@progbits
