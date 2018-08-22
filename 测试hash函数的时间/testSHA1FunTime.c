#include "time.h"
#include "sys/time.h"
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

int main()
{
  int timeuse;
struct timeval start, end;

  gettimeofday( &start, NULL );

unsigned char digest[SHA_DIGEST_LENGTH];
char string[] = "hello world";

SHA1((unsigned char*)&string, strlen(string), (unsigned char*)&digest);

char mdString[SHA_DIGEST_LENGTH*2+1];

int i = 0;
for(i= 0; i < SHA_DIGEST_LENGTH; i++){
sprintf(&mdString[i*2], "%02x", (unsigned int)digest[i]);
}
gettimeofday( &end, NULL );
timeuse = end.tv_usec -start.tv_usec;
printf("一次sha1消耗 %d us\n", timeuse);
printf("SHA1 digest: %s\n", mdString);

return 0;
}
