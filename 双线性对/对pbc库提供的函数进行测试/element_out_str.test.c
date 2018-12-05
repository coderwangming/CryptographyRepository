//gcc -I./pbc -I./pbc/include -lpbc -lgmp -std=c99 -o test element_out_str.test.c && clear && ./test < ./pbc/param/a.param

#include <pbc.h>
#include <pbc_test.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  pairing_t pairing;
  element_t g;

  pbc_demo_pairing_init(pairing, argc, argv);

  element_init_G2(g, pairing);
  element_random(g);
  element_printf("g = %B\n", g);
  
  FILE * file_demo = fopen("./text.txt","w");
  element_out_str(file_demo,2,g);
  element_out_str(file_demo,10,g);
  element_out_str(file_demo,16,g);
  fclose(file_demo);

  element_clear(g);
  pairing_clear(pairing);
  
  
  return 0;
}

