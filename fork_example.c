#include<stdio.h>
#include<stdlib.h>
#include<stdint.h>

int main()
{
    // each process created from a tree
    // Parent creates clone
    // each process clones and creates tree of processes
    //fork returns 0 - child
    //for return pid - parent
    pid_t pid = fork();
    //for child process pid will be always 0
    if( 0 == pid)
    {
        printf("child::Helloooooooooooooooooo - %d\n", getpid());
        //fflush to make sure system call "ps" wouldn't print it's output before printf statement
        fflush(stdout);
        sleep(1);
        printf("child::terminating\n");
        fflush(stdout);
    }
    else
    {
        printf("parent::Helloooooooooooooooooo - %d\n", getpid());
        fflush(stdout);
        system("ps");
        //Wait until the child process terminates
        int status;
        wait(&status);
        printf("parent::child process terminated with status %d\n", status);
        fflush(stdout);
        system("ps");
    }

    return 0;                                                                                                                                                                                  
}
