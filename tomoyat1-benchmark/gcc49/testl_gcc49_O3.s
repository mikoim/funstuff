	.file	"testl.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.section	.text.startup,"ax",@progbits
.LHOTB0:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB4:
	.cfi_startproc
	movl	$-1, %eax
	.p2align 4,,10
	.p2align 3
.L2:
#APP
# 7 "testl.c" 1
	testl %ebx, %ebx
# 0 "" 2
#NO_APP
	subl	$1, %eax
	jne	.L2
	xorl	%eax, %eax
	ret
	.cfi_endproc
.LFE4:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE0:
	.section	.text.startup
.LHOTE0:
	.ident	"GCC: (Debian 4.9.2-10) 4.9.2"
	.section	.note.GNU-stack,"",@progbits
