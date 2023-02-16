//include headers
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>



int main()
{
    //create two processes
    int pid = fork();
    //if pid is 0, then it is child process
    if (pid == 0)
    {
        //child process
        printf("Child process is running");
        //child process will sleep for 5 seconds
        sleep(5);
        //child process will exit
        exit(0);
    }
    //if pid is greater than 0, then it is parent process
    else if (pid > 0)
    {
        //parent process
        printf("Parent process is running");
        //parent process will wait for child process to complete
        // Implment busy waiting for parent process
        while (1)
        {
            // parent process will check if child process is completed or not
            if (waitpid(pid, NULL, WNOHANG) == 0)
            {
                // if child process is not completed, then parent process will sleep for 1 second
                sleep(1);
            }
            else
            {
                // if child process is completed, then parent process will exit
                exit(0);
            }
        }
        wait(NULL);
        // parent process will exit
        exit(0);
    }

    return 0;
}