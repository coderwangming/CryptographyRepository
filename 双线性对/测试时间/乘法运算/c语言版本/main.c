
//////////////////////////////////////////////////////////////////////
// 如何运行
// gcc -I./pbc -I./pbc/include -lpbc -lgmp -std=c99 -o main main.c && clear && ./main < ./pbc/param/a.param
// g++ -I/root/gmp-6.1.2 -lgmp -lntl -lm  -std=c++11 -o main main.cpp PrGlib.cpp RSA.cpp
//////////////////////////////////////////////////////////////////////


#include <stdio.h>
#include <stdlib.h>

#include "time.h"
#include "sys/time.h"

#include <pbc.h>
#include <pbc_test.h>
#include <pbc_poly.h>
#include "./pbc/misc/darray.c"
#include "./pbc/arith/fp.c"
#include "./pbc/arith/poly.c"

#define TIMES 10000

int main(int argc, char **argv){
	int timeuse;
	struct timeval start, end;
	
	element_t g,res;
	pairing_t pairing;
	
	// Pairing initialization
	pbc_demo_pairing_init(pairing, argc, argv);

	
	element_init_G1(g, pairing);
	element_random(g);

	
	element_init_G1(res, pairing);
	element_set1(res);
	
	gettimeofday( &start, NULL );
	int i=0;
	for(i=0;i<TIMES;i++){
		element_mul(res,g,res);
	}
	gettimeofday( &end, NULL );
	timeuse = 1000000 * ( end.tv_sec - start.tv_sec ) + end.tv_usec -start.tv_usec;
	//printf("Setup Time: %.3f ms\n", timeuse/1000.000);
	printf("%d 次G域上的乘法运算花费 %.3f ms\n", TIMES, TIMES, timeuse/1000.000);
}

