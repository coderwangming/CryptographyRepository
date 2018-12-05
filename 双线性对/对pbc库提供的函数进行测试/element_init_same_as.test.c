//gcc -I./pbc -I./pbc/include -lpbc -lgmp -std=c99 -o test element_init_same_as.test.c && clear && ./test < ./pbc/param/a.param

#include <pbc.h>
#include <pbc_test.h>

int main(int argc, char **argv) {
  pairing_t pairing;
  element_t g,h;

  pbc_demo_pairing_init(pairing, argc, argv);

  element_init_G2(g, pairing);

  element_random(g);
  element_printf("g = %B\n", g);
  
  element_init_same_as(h,g);
  element_printf("h = %B\n", h);

  element_clear(g);
  element_clear(h);
  pairing_clear(pairing);
  return 0;
}
