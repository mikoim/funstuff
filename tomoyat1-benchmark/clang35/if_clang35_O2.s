	.text
	.file	"if.c"
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:
	pushq	%rax
.Ltmp0:
	.cfi_def_cfa_offset 16
	leaq	4(%rsp), %rsi
	movl	$.L.str, %edi
	xorl	%eax, %eax
	callq	__isoc99_scanf
	movl	4(%rsp), %eax
	cmpl	$3, %eax
	je	.LBB0_5
# BB#1:
	cmpl	$2, %eax
	jne	.LBB0_2
# BB#4:
	movl	$.Lstr4, %edi
	jmp	.LBB0_6
.LBB0_5:
	movl	$.Lstr, %edi
	jmp	.LBB0_6
.LBB0_2:
	cmpl	$1, %eax
	jne	.LBB0_7
# BB#3:
	movl	$.Lstr5, %edi
.LBB0_6:
	callq	puts
.LBB0_7:
	xorl	%eax, %eax
	popq	%rdx
	retq
.Ltmp1:
	.size	main, .Ltmp1-main
	.cfi_endproc

	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d"
	.size	.L.str, 3

	.type	.Lstr,@object           # @str
.Lstr:
	.asciz	"THREE"
	.size	.Lstr, 6

	.type	.Lstr4,@object          # @str4
.Lstr4:
	.asciz	"TWO"
	.size	.Lstr4, 4

	.type	.Lstr5,@object          # @str5
.Lstr5:
	.asciz	"ONE"
	.size	.Lstr5, 4


	.ident	"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"
	.section	".note.GNU-stack","",@progbits
