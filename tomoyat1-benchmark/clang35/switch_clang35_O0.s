	.text
	.file	"switch.c"
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
	subq	$64, %rsp
	movl	$0, -4(%rbp)
	movl	%edi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	$.L.str, %edi
                                        # kill: RDI<def> EDI<kill>
	xorl	%eax, %eax
	movb	%al, %cl
	leaq	-20(%rbp), %rsi
	movb	%cl, %al
	callq	__isoc99_scanf
	movl	-20(%rbp), %edx
	movl	%edx, %r8d
	subl	$3, %r8d
	movl	%eax, -24(%rbp)         # 4-byte Spill
	movl	%edx, -28(%rbp)         # 4-byte Spill
	movl	%r8d, -32(%rbp)         # 4-byte Spill
	je	.LBB0_3
	jmp	.LBB0_5
.LBB0_5:
	movl	-28(%rbp), %eax         # 4-byte Reload
	subl	$2, %eax
	movl	%eax, -36(%rbp)         # 4-byte Spill
	je	.LBB0_2
	jmp	.LBB0_6
.LBB0_6:
	movl	-28(%rbp), %eax         # 4-byte Reload
	subl	$1, %eax
	movl	%eax, -40(%rbp)         # 4-byte Spill
	jne	.LBB0_4
	jmp	.LBB0_1
.LBB0_1:
	movabsq	$.L.str1, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -44(%rbp)         # 4-byte Spill
	jmp	.LBB0_4
.LBB0_2:
	movabsq	$.L.str2, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -48(%rbp)         # 4-byte Spill
	jmp	.LBB0_4
.LBB0_3:
	movabsq	$.L.str3, %rdi
	movb	$0, %al
	callq	printf
	movl	%eax, -52(%rbp)         # 4-byte Spill
.LBB0_4:
	movl	$0, %eax
	addq	$64, %rsp
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
