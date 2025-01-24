#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>
#include "gmp.h"

// We gonna do all the functions over the group Z/nZ
// The goal of these algorithms is to solve the equation y = g^x mod n
// This equation is hard to solve if we choose good parameters
// But sometimes, it can happen that a parameter made the solving easier

// The most generic algorithm, with compromise time memory
void baby_step_giant_step(mpz_t z_g, mpz_t z_n, mpz_t z_y, unsigned long long table_size, mpz_t z_x){
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
        mpz_set(table[i], z_a);
        mpz_mul(z_a, z_a, z_g);
        mpz_mod(z_a, z_a, z_n);
    }
    //printf("The table is done!\n"); //good news!
    mpz_set(z_a, z_y);
    mpz_powm_ui(z_g_inv_m, z_g, table_size, z_n);
    mpz_invert(z_g_inv_m, z_g_inv_m, z_n);
    mpz_div_ui(z_compute_size, z_n, table_size);
    mpz_set_ui(z_count, 0);
    bool search_solution = true;
    while(mpz_cmp(z_count, z_compute_size)<0 || search_solution){
        for(int j=0; j<table_size; j++){
            if(mpz_cmp(z_a, table[j])==0){
                mpz_mul_ui(z_x, z_count, table_size);
                mpz_add_ui(z_x, z_x, j);
                gmp_printf("Log of %Zu in base %Zu mod %Zu: %Zu\n", z_y, z_g, z_n, z_x);
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

// If the group order is easily factorisable, one can compute discrete logarithm with Pohlig-Hellman algorithm
void pohlig_hellman(mpz_t z_g, mpz_t z_n, mpz_t z_y, mpz_t z_x){
    // first step: factorisation
    // second step: BsGs with for each factors
    // third step: CRT for retrieve original log
}


void pollard_function(mpz_t x, mpz_t a, mpz_t b, mpz_t g, mpz_t y, mpz_t n){
    mpz_t residue;
    mpz_init(residue);
    mpz_mod_ui(residue, x, 3);
    if(mpz_cmp_ui(residue, 1)==0){
        mpz_add_ui(b, b, 1);
        mpz_mul(x, x, y);
        mpz_mod(x, x, n);
    } else if (mpz_cmp_ui(residue, 0)==0){
        mpz_mul_ui(a, a, 2);
        mpz_mul_ui(b, b, 2);
        mpz_powm_ui(x, x, 2, n);
    } else if(mpz_cmp_ui(residue,2)==0){
        mpz_add_ui(a, a, 1);
        mpz_mul(x, x, g);
        mpz_mod(x, x, n);
    }
    mpz_clear(residue);
}

void pollard_rho(mpz_t z_g, mpz_t z_n, mpz_t z_y, mpz_t z_x){
    //goal: find a collision x_i=x_2i using floyd's algorithm
    //we need to construct a "random" function
    mpz_t x0, x1, a0, a1, b0, b1, z_order; // such as xi = g^ai * y^bi
    mpz_inits(x0, x1, a0, a1, b0, b1, z_order, NULL);
    mpz_sub_ui(z_order, z_n, 1);
    mpz_set_ui(a0, 0);
    mpz_set_ui(b0, 0);
    mpz_set_ui(x0, 1);
    pollard_function(x0, a0, b0, z_g, z_y, z_n);
    mpz_set(x1, x0);
    mpz_set(a1, a0);
    mpz_set(b1, b0);
    pollard_function(x1, a1, b1, z_g, z_y, z_n);
    int i = 1;
    //floyd algorithm, we are looking for a collision
    while(mpz_cmp(x0,x1)!=0){
        pollard_function(x0, a0, b0, z_g, z_y, z_n);
        pollard_function(x1, a1, b1, z_g, z_y, z_n);
        pollard_function(x1, a1, b1, z_g, z_y, z_n);
        i++;
    }
    gmp_printf("a0: %Zu, a1: %Zu, b0: %Zu, b1: %Zu\n", a0, a1, b0, b1);
    mpz_sub(b0, b0, b1); //b0-b1
    mpz_mod(b0, b0, z_order);
    mpz_sub(a0, a1, a0); //a1-a0
    mpz_mod(a0, a0, z_order);
    mpz_powm_ui(b0, b0, -1, z_order); //inv mod n
    mpz_mul(a0, a0, b0);
    mpz_mod(z_x, a0, z_order); //z_x = (a1-a0)*(b0-b1)^-1
    gmp_printf("Log of %Zu in base %Zu mod %Zu: %Zu\n", z_y, z_g, z_n, z_x);
    mpz_powm(x0, z_g, z_x, z_n);
    gmp_printf("%Zu\n", x0);
    mpz_clears(x0, x1, a0, a1, b0, b1, NULL);
}