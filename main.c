#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>
#include "gmp.h"
#include <time.h>
#include "discrete_log.c"

int main(){
    //Discrete logarithm toy example
    mpz_t z_y, z_g, z_n, z_x;
    mpz_inits(z_n, z_y, z_g, z_x, NULL);
    mpz_set_ui(z_n, 97);
    mpz_set_ui(z_g, 5); //generator certified
    mpz_set_ui(z_y, 32); //choose any one you want
    baby_step_giant_step(z_g, z_n, z_y, 5, z_x);
    return 0;
}