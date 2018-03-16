#include <sys/times.h>
#include <time.h>
#include <stdio.h> 
#include <pthread.h> 



struct timespec tpBegin3,tpEnd3;  //These are inbuilt structures to store the time related activities

double compute(struct timespec start,struct timespec end) //computes time in milliseconds given endTime and startTime timespec structures.
{
  double t;
  t=(end.tv_sec-start.tv_sec)*1000;
  t+=(end.tv_nsec-start.tv_nsec)*0.000001;

  return t;
}

int array[1600];

void *expensive_function(void *param) {     
  int   index = *((int*)param);
  int   i;
  for (i = 0; i < 100000000; i++)
    array[index]+=1;
} 

int main(int argc, char *argv[]) { 
  int       first_elem  = 0;
  int       bad_elem    = 1;
  int       good_elem   = 99;
  int i;
  int indexes[16]; 
  double time1;
  double time2;
  double time3;
  pthread_t     threads[16];
  for(i=0; i<16;i++)indexes[i]=i*good_elem;

  //---------------------------START--------parallel computation without False Sharing------------------------

  clock_gettime(CLOCK_REALTIME,&tpBegin3); 
  for(i=0; i<16;i++){
    pthread_create(&threads[i], NULL,expensive_function, (void*)&indexes[i]);
  }
  for(i=0; i<16;i++){
    pthread_join(threads[i], NULL);
  }
  clock_gettime(CLOCK_REALTIME,&tpEnd3);

  //---------------------------END--------parallel computation without False Sharing------------------------


  //--------------------------START------------------OUTPUT STATS--------------------------------------------
  printf("array[first_element]: %d\t\t array[bad_element]: %d\t\t array[good_element]: %d\n\n\n", array[first_elem],array[bad_elem],array[good_elem]);

  time3 = compute(tpBegin3,tpEnd3);
  printf("Time taken without false sharing  : %f ms\n", time3);

  //--------------------------END------------------OUTPUT STATS--------------------------------------------
  

  return 0; 
}

