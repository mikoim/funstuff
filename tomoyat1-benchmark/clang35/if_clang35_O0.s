	.text
	.file	"if.c"
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:
	pushq	%rbp
.Ltmp0:
	.cfi_def_cfa_offset 16
.Ltmp1:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
.Ltmp2:
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movabsq	$.L.str, %rax
	leaq	-20(%rbp), %rcx
	movl	$0, -4(%rbp)
	movl	%edi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	%rax, %rdi
	movq	%rcx, %rsi
	movb	$0, %al
	callq	__isoc99_scanf
	cmpl	$1, -20(%rbp)
	movl	%eax, -24(%rbp)         # 4-byte Spill
	jne	.LBB0_2
# BB#1:
	movabsq	$.L.str1, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -28(%rbp)         # 4-byte Spill
	jmp	.LBB0_8
.LBB0_2:
	cmpl	$2, -20(%rbp)
	jne	.LBB0_4
# BB#3:
	movabsq	$.L.str2, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -32(%rbp)         # 4-byte Spill
	jmp	.LBB0_7
.LBB0_4:
	cmpl	$3, -20(%rbp)
	jne	.LBB0_6
# BB#5:
	movabsq	$.L.str3, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -36(%rbp)         # 4-byte Spill
.LBB0_6:
	jmp	.LBB0_7
.LBB0_7:
	jmp	.LBB0_8
.LBB0_8:
	movl	$0, %eax
	addq	$48, %rsp
	popq	%rbp
	retq
.Ltmp3:
	.size	main, .Ltmp3-main
	.cfi_endproc

	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d"
	.size	.L.str, 3

	.type	.L.str1,@object         # @.str1
.L.str1:
	.asciz	"ONE\n"
	.size	.L.str1, 5

	.type	.L.str2,@object         # @.str2
.L.str2:
	.asciz	"TWO\n"
	.size	.L.str2, 5

	.type	.L.str3,@object         # @.str3
.L.str3:
	.asciz	"THREE\n"
	.size	.L.str3, 7


	.ident	"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"
	.section	".note.GNU-stack","",@progbits
