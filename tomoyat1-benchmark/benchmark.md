
```c:if.c
#include <stdio.h>

int main(int argc, const char * argv[]) {
    int num;
    
    scanf("%d", &num);
    
    if (num == 1)
        printf("ONE\n");

    else if (num == 2)
        printf("TWO\n");
    
    else if (num == 3)
        printf("THREE\n");
    
    return 0;
}

```


```c:switch.c
#include <stdio.h>

int main(int argc, const char * argv[]) {
    int num;
    
    scanf("%d", &num);
    
    switch (num) {
        case 1:
            printf("ONE\n");
            break;
            
        case 2:
            printf("TWO\n");
            break;
        
        case 3:
            printf("THREE\n");
            break;
    }
    
    return 0;
}

```

```c:testl.c
#include <inttypes.h>

int main(int argc, const char * argv[]) {
	uint32_t i;

    for (i = 0; i < UINT32_MAX; i++) {
        asm volatile("testl %ebx, %ebx");
    }
    
    return 0;
}

```

```c:cmpl.c
#include <inttypes.h>

int main(int argc, const char * argv[]) {
	uint32_t i;

    for (i = 0; i < UINT32_MAX; i++) {
        asm volatile("cmpl %ebx, %ebx");
    }
    
    return 0;
}

```