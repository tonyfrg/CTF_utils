#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>
#include "gmp.h"
#include <time.h>

// We did all the functions over the group Z/nZ
// The goal of these algorithms is to solve the equation y = g^x mod n
// This equation is hard to solve if we choose good parameters
// But sometimes, it can happen that a parameter made the solving easier

// The most generic algorithm, with compromise time memory
void baby_step_giant_step(mpz_t z_g, mpz_t z_n, mpz_t z_y, unsigned long table_size, mpz_t z_x){
    //mpz_t z_m;
    //mpz_init(z_m);
    mpz_t z_a, z_g_inv_m, z_compute_size, z_count;
    mpz_inits(z_a, z_g_inv_m, z_compute_size, z_count, NULL);
    //mpz_sqrt(z_m, z_n);
    mpz_t* table = (mpz_t*) malloc(table_size*sizeof(mpz_t));
    mpz_set_ui(z_a, 1);
    // initialisation of the table (not with size = sqrt(n))
    for(int i=0; i<table_size; i++){
        mpz_init(table[i]);
        mpz_mul(z_a, z_a, z_g);
        mpz_mod(z_a, z_a, z_n);
        mpz_set(table[i], z_a);
    }
    //printf("The table is done!\n"); //good news!
    mpz_set(z_a, z_y);
    mpz_powm_ui(z_g_inv_m, z_g, table_size, z_n);
    mpz_invert(z_g_inv_m, z_g_inv_m, z_n);
    mpz_div_ui(z_compute_size, z_n, table_size);
    bool search_solution = true;
    while(mpz_cmp(z_count, z_compute_size)<0 || search_solution){
        for(int j=0; j<table_size; j++){
            if(mpz_cmp(z_a, table[j])==0){
                mpz_mul_ui(z_x, z_count, table_size);
                mpz_add_ui(z_x, z_x, j);
                gmp_printf("Solution found: %Zu\n", z_x);
                for(int i=0; i<table_size; i++){
                    mpz_clear(table[i]);
                }
                free(table);
                search_solution = false; // end of the program
            }
        }
        mpz_mul(z_a, z_a, z_g_inv_m);
        mpz_mod(z_a, z_a, z_n);
        mpz_add_ui(z_count, z_count, 1);
    }
    mpz_clears(z_a, z_g_inv_m, z_compute_size, z_count, NULL);
    if(search_solution){
        for(int i=0; i<table_size; i++){
            mpz_clear(table[i]);
        }
        free(table);
        printf("No solution found!\n");
    }
}

