#include <stdio.h>
#include <string.h>

char flag[80] = "csc{n0t_wh4t_1t_s33ms!}";
char pwd[20] = "l3tm31n";
int main(void){
    printf("Enter the password:\n");
    char input[20];
    scanf("%19s", &input);
    if(strcmp(input, pwd) == 0){
        printf("Welcome! Here's your flag: %s\n", flag);
    }else{
        printf("Wrong\n");
    }
    // printf(pwd);
    return 0;
}

__attribute__ ((__constructor__)) 
void __construct_gc(void) { 
    char a[20] = {0x3c, 'K', 'C', '*', 'E', '\01', 'w'};
    for(int i = 0; i<8; i++){
        pwd[i] = (pwd[i] - a[i] + 128) % 128;
    }
    char b[20] = {'w', 'H', '@', 'k', 0x18, '7', 'A', '\x15', 'k', 'I', 'C', 'l', '\x14', 'F', 0x7f, '\06', 'B', '>'};
    for(int i = 0; i<20; i++){
        flag[i + 4] = (flag[i+4] - b[i] + 128) % 128;
    }


}

int strcmp(const char *X, const char *Y)
{
    while (*X)
    {
        // if characters differ, or end of the second string is reached
        if (*X != *Y) {
            break;
        }
 
        // move to the next pair of characters
        X++;
        Y++;
    }
 
    // return the ASCII difference after converting `char*` to `unsigned char*`
    return *(const unsigned char*)X - *(const unsigned char*)Y;
}