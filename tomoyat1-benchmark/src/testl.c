#include <inttypes.h>

int main(int argc, const char * argv[]) {
	uint64_t i;
    
    for (i = 0; i < 42949672950; i++) {
        asm volatile("testl %ebx, %ebx");
    }
    
    return 0;
}
