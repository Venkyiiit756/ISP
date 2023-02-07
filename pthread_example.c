/* Pthread demonstration*/
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <assert.h>

void *print_message_function( void *ptr );

unsigned long int gv = 0;
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;

//syncronization is a way to make sure that the threads are not running at the same time
void *print_message_function( void *ptr )
{

    char *message;
    //type cast the void pointer to char pointer
    message = (char *) ptr;
    printf("%s\n", message);
    //Mutex is a way to make sure that only one thread is running at a time
    //this is a critical section
    for(unsigned long int i = 0; i < 10000000; i++)
    {
        
        pthread_mutex_lock( &mutex1 );
        gv++;
        pthread_mutex_unlock( &mutex1 );
    }
}

int main()
{

    pthread_t thread1, thread2;
    pthread_mutex_init(&mutex1, NULL);

    char *message1 = "Thread 1";
    char *message2 = "Thread 2";
    int  iret1, iret2;

    /* Create independent threads each of which will execute function */

    //why do we need to pass the address of the thread? it is because the function is going to modify the thread
    // why do we need to pass the address of the function? it is because the function is going to modify the function
    // why do typecase message1 and message2 to void*? 
    // It might be because the function is expecting a void pointer

    iret1 = pthread_create( &thread1, NULL, print_message_function, (void*) message1);
    iret2 = pthread_create( &thread2, NULL, print_message_function, (void*) message2);

    /* Wait till threads are complete before main continues. Unless we  */
    /* wait we run the risk of executing an exit which will terminate   */
    /* the process and all threads before the threads have completed.   */

    pthread_join( thread1, NULL);
    pthread_join( thread2, NULL); 

    //global variable value
    printf("Global variable value: %lu, expected value: 20000000 \n", gv);
    printf("Thread 1 returns: %d\n", iret1);
    printf("Thread 2 returns: %d\n", iret2);

    assert(gv == 20000000);

    exit(0);
}