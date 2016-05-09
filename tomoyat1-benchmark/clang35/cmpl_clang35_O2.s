	.text
	.file	"cmpl.c"
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# BB#0:
	movl	$-1, %eax
	.align	16, 0x90
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	#APP
	cmpl	%ebx, %ebx
	#NO_APP
	decl	%eax
	jne	.LBB0_1
# BB#2:
	xorl	%eax, %eax
	retq
.Ltmp0:
	.size	main, .Ltmp0-main
	.cfi_endproc


	.ident	"Debian clang version 3.5.0-10 (tags/RELEASE_350/final) (based on LLVM 3.5.0)"
	.section	".note.GNU-stack","",@progbits
