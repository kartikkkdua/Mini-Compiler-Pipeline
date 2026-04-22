#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>

// Global Variables & Temporaries
long long t1 = 0;
char* message = NULL;
long long result = 0;
long long x = 0;
long long counter = 0;
long long t5 = 0;
long long a = 0;
long long b = 0;
long long t11 = 0;
long long d = 0;
long long y = 0;
long long t7 = 0;
long long c = 0;
long long t8 = 0;
long long t6 = 0;
long long flag = 0;
long long t10 = 0;
long long t9 = 0;
long long t3 = 0;

intptr_t param_stack[1000];
int param_sp = 0;

int main() {
    a = (long long)5;
    b = (long long)10;
    message = "Starting calculation";
    goto L1;
FUNC_multiply:;
    y = (long long)param_stack[--param_sp];
    x = (long long)param_stack[--param_sp];
    t1 = x * y;
    // RETURN t1
    // RETURN_VOID
L1:;
    t3 = a + 6;
    c = (long long)t3;
    t5 = a + 6;
    d = (long long)t5;
    param_stack[param_sp++] = (intptr_t)t3;
    param_stack[param_sp++] = (intptr_t)t5;
    // CALL multiply - Simulated by flat IR jumps
    result = (long long)t6;
    flag = (long long)1;
    counter = (long long)0;
L2:;
    t7 = counter < 5;
    t8 = flag == 1;
    t9 = t7 && t8;
    if (!t9) goto L3;
    printf("%s\n", message);
    t10 = counter + 1;
    counter = (long long)t10;
    t11 = t10 == 4;
    if (!t11) goto L5;
L4:;
    flag = (long long)0;
L5:;
    goto L2;
L3:;
    printf("%lld\n", (long long)result);
    return 0;
}