#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    unsigned int i = 0;
    unsigned int j = 0;
    unsigned int uiLimit = 0;
    unsigned int uiPrime = 0;
    
    char cBuf[64];
    char* cpTable;
    
    printf("Maximum number:");
    fgets(cBuf, sizeof(cBuf)/sizeof(cBuf[0]), stdin);
    sscanf(cBuf, "%u", &uiLimit);
    
    cpTable = calloc(uiLimit, sizeof(char));
    
    for (i = 1; i < uiLimit; i++) {
        if (cpTable[i] == 1) {
            continue;
        }
        
        uiPrime++;
        
        for (j = i + i + 1; j < uiLimit; j = j + i + 1) {
            cpTable[j] = 1;
        }
    }
    
    for (i = 1; i < uiLimit; i++) {
        if (cpTable[i] == 0) {
            printf("%u\n", i + 1);
        }
    }
    
    free(cpTable);
    
    printf("The number of primes under %u = [%u]\n", uiLimit, uiPrime);
    
    return 0;
}
