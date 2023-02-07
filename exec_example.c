#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    //fork a child process
    pid_t pid = fork();

    if (pid < 0) //error occurred
    {
        fprintf(stderr, "Fork Failed");
        return 1;
    }
    else if (pid == 0) //child process
    {
        printf("Child::ps\n");
        fflush(stdout);
        execlp("ps", "ps", NULL);
    }
    else //parent process
    {
        printf("Parent::Enter with child pid %d\n", pid);
        fflush(stdout);
        //parent will wait for the child to complete
        wait(NULL);
        printf("Parent::Child Complete\n");
        fflush(stdout);
    }
    return 0;
}
