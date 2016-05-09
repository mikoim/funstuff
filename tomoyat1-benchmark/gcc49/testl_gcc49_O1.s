	.file	"testl.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB4:
	.cfi_startproc
	movl	$-1, %eax
.L2:
#APP
# 7 "testl.c" 1
	testl %ebx, %ebx
# 0 "" 2
#NO_APP
	subl	$1, %eax
	jne	.L2
	movl	$0, %eax
	ret
	.cfi_endproc
.LFE4:
	.size	main, .-main
	.ident	"GCC: (Debian 4.9.2-10) 4.9.2"
	.section	.note.GNU-stack,"",@progbits
