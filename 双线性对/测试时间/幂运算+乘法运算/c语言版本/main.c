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
	
	element_t g,s,res,temp;
	pairing_t pairing;
	
	// Pairing initialization
	pbc_demo_pairing_init(pairing, argc, argv);

	
	element_init_G1(temp, pairing);
	
	element_init_G1(g, pairing);
	element_random(g);
	
	element_init_Zr(s, pairing);
	element_random(s);
	
	element_init_G1(res, pairing);
	element_set1(res);
	
	gettimeofday( &start, NULL );
	int i=0;
	for(i=0;i<TIMES;i++){
		element_pow_zn(temp, g, s);
		element_mul(res,temp,res);
	}
	gettimeofday( &end, NULL );
	timeuse = 1000000 * ( end.tv_sec - start.tv_sec ) + end.tv_usec -start.tv_usec;
	//printf("Setup Time: %.3f ms\n", timeuse/1000.000);
	printf("%d 次幂运算 和 %d 次乘法运算花费 %.3f ms\n", TIMES, TIMES, timeuse/1000.000);
}

// gcc -I./pbc -I./pbc/include -lpbc -lgmp -std=c99 -o main main.c && clear && ./main < ./pbc/param/a.param

