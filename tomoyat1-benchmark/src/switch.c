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
