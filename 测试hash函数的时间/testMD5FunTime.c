#include "time.h"
#include "sys/time.h"
#include<stdio.h>
#include<openssl/md5.h>
#include<string.h>

int main( int argc, char **argv )
{
  int timeuse;
struct timeval start, end;



  gettimeofday( &start, NULL );

  MD5_CTX ctx;
  unsigned char *data="123";
  unsigned char md[16];
  char buf[33]={'/0'};
  char tmp[3]={'/0'};
  int i;


    MD5_Init(&ctx);
    MD5_Update(&ctx,data,strlen(data));
    MD5_Final(md,&ctx);

    for( i=0; i<16; i++ ){
        sprintf(tmp,"%02X",md[i]);
        strcat(buf,tmp);
    }

    gettimeofday( &end, NULL );
    timeuse =  end.tv_usec -start.tv_usec;
  //printf("Setup Time: %.3f ms\n", timeuse/1000.000);
  printf("一次md5消耗 %d us\n", timeuse);
  printf("%s\n",buf);
    return 0;
}
