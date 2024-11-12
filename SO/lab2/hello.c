#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main()
{
    const char *message = "Helloworld\n";
    
    write(STDOUT_FILENO, message, strlen(message));

    return 0;
}

