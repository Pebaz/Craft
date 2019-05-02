// ./tcc -Ilibtcc dynamic_compilation.c -L. -ltcc

#include <stdlib.h>
#include <stdio.h>
#include "libtcc.h"


// This error will happen since this func is declared outside of the code
// <string>:8: warning: implicit declaration of function 'add'
int add(int a, int b) { return a + b; }

char my_program[] =
"#include <stdio.h>\n"
"int fib(int n) {\n"
"    if (n <= 2) return 1;\n"
"    else return fib(n-1) + fib(n-2);\n"
"}\n"
"int foobar(int n) {\n"
"    printf(\"\t-> fib(%d) = %d\\n\", n, fib(n));\n"
"    printf(\"\t-> add(%d, %d) = %d\\n\", n, 2 * n, add(n, 2 * n));\n"
"    return 1337;\n"
"}\n";

int main(int argc, char **argv)
{
    TCCState *s;
    int (*foobar_func)(int);
    void *mem;

    s = tcc_new();
    tcc_set_output_type(s, TCC_OUTPUT_MEMORY);
    tcc_compile_string(s, my_program);
    tcc_add_symbol(s, "add", add);

    mem = malloc(tcc_relocate(s, NULL));
    tcc_relocate(s, mem);

    foobar_func = tcc_get_symbol(s, "foobar");

    tcc_delete(s);

    printf("foobar returned: %d\n", foobar_func(32));

    free(mem);
    return 0;
}