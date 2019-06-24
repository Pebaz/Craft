#include <stdio.h>

int main(int argc, char** argv)
{
	printf("HERE\n");
	goto error;
	printf("Won't see this\n");
	error:
	printf("Error!\n");
}
