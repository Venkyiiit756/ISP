#include <stdio.h>
#include <pthread.h>
//include headers
#include <sched.h>
#include <unistd.h>

void *thread_function(void *arg)
{

    //name thread
    pthread_setname_np(pthread_self(), "thread_function");


    printf("thread_function is running. Argument was %s\n", (char *)arg);
    sleep(1);
    return NULL;
}

int main()
{
    //print something
    printf("main function is running\n");

    //create pthread
    pthread_t thread;

    pthread_create(&thread, NULL, thread_function, NULL);

    //apply rt scheduling policy
    struct sched_param param;
    param.sched_priority = 50;
    pthread_setschedparam(thread, SCHED_FIFO, &param);

    //get scheduling policy
    int policy;
    pthread_getschedparam(thread, &policy, &param);
    printf("thread_function is running with policy %d and priority %d\n", policy, param.sched_priority);


    //wait for thread to finish
    pthread_join(thread, NULL);

    return 0;
}