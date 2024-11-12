#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char** argv)
{
	struct stat sb;
	const int bufsz = 1024 * 64;
	
	int dest = open(argv[2], O_WRONLY);
	int src;
	if (stat(argv[1], &sb)) 
	{
	  perror(argv[1]);
	}
		
	src = open(argv[1], O_RDONLY);
	
	char buffer[bufsz];
	
	int content;
	while ((content = read(src, &buffer, bufsz)) > 0)
	{
	   write(dest, &buffer, content);
	}

	close(src);
	close(dest);
	return 0;
}
