#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>
#include "gmp.h"

#define MAX_FACTORS 100

typedef struct {
    mpz_t factor;
    int power;
}factor_tuple;

void set_tuple(factor_tuple my_tuple, mpz_t factor, int power){
    mpz_init(my_tuple.factor);
    mpz_set(my_tuple.factor, factor);
    my_tuple.power = power;
}

void free_tuple(factor_tuple my_tuple){
    mpz_clear(my_tuple.factor);
}

// The goal of this file is to write some factorization algorithm
// It can be used for attacking RSA with weak key-size, for instance
// These algorithm can be efficient for "small" prime, like 10 or 20 digits
// The RSA algorithms suppose that the module is a product of two prime (and only two)

// The naive way to attack the RSA module
void naive_factorization_RSA(mpz_t z_n, mpz_t z_p, mpz_t z_q){
    mpz_t z_sqrt, z_count;
    mpz_inits(z_sqrt, z_count, NULL);
    mpz_sqrt(z_sqrt, z_n);
    mpz_set_ui(z_count, 3);
    bool unfactorized = true;
    //first test: z_n is even? if yes, it's done
    mpz_cdiv_qr_ui(z_q, z_p, z_n, 2);
    if (mpz_cmp_ui(z_p,0)==0) {
        mpz_set_ui(z_p, 2);
        unfactorized = false;
        gmp_printf("Factorization of %Zu is done:\np = %Zu\nq = %Zu\n", z_n, z_p, z_q);
    }
    while (mpz_cmp(z_count, z_sqrt)<=0 && unfactorized){
        mpz_cdiv_qr(z_q, z_p, z_n, z_count); //z_p is used as residue, avoid an alloc
        if (mpz_cmp_ui(z_p,0)==0){
            mpz_set(z_p, z_count);
            unfactorized = false;
            gmp_printf("Factorization of %Zu is done:\np = %Zu\nq = %Zu\n", z_n, z_p, z_q);
        }
        mpz_add_ui(z_count, z_count, 2); //useless to try even divisors
    }
    if(unfactorized){gmp_printf("Your integer is a prime number.\n", z_n);}
    mpz_clears(z_sqrt, z_count, NULL);
}

// No value is stored
void naive_factorisation_print(mpz_t z_n){
    mpz_t z_sqrt, z_q, z_r, z_count, z_fact, z_fact_partial;
    int fact_power = 0;
    mpz_inits(z_sqrt, z_q, z_r, z_fact_partial, NULL);
    mpz_init_set(z_q, z_n);
    mpz_cdiv_ui(z_q, z_r, z_n, 2);
    if(mpz_cmp_ui(z_r, 0)==0){
        printf("Factor found: 2");
        while (mpz_cmp_ui(z_q, 1)>0 && mpz_cmp_ui(z_r, 0)==0) {
            fact_power += 1;
            mpz_cdiv_ui(z_q, z_r, z_q, 2);
        }
        printf("^%u\n", fact_power);
        mpz_div_exact_ui(z_fact, 2**fact_power);
    }
    mpz_init_set_ui(z_count, 3);
    while(mpz_cmp_ui(z_fact, 1)>0 && mpz_cmp_ui(z_count, z_sqrt)<=0){
        fact_power = 0;
        mpz_cdiv_ui(z_q, z_r, z_fact, z_count);
        if(mpz_cmp_ui(z_r, 0)==0){
            gmp_printf("Factor found: %Zu", z_count);
            while (mpz_cmp_ui(z_q, 1)>0 && mpz_cmp_ui(z_r, 0)==0) {
                fact_power += 1;
                mpz_cdiv_ui(z_q, z_r, z_q, z_count);
            }
            printf("^%u\n", fact_power);
            mpz_pow_ui(z_q, z_q, fact_power);
            mpz_divexact(z_fact, z_fact, z_q); //we update z_fact at each factor found
        }
    }
    printf("Factorization is done.\n");
}

void naive_factorisation(mpz_t z_n, factor_tuple* factors){
    mpz_t z_sqrt, z_q, z_r, z_count, z_fact, z_fact_partial;
    int fact_power = 0; //power of the factor
    int counter = 0; //enumeration of factor
    mpz_inits(z_sqrt, z_q, z_r, z_fact_partial, z_count, NULL);

    mpz_set_ui(z_count, 2);
    mpz_init_set(z_q, z_n);
    mpz_cdiv(z_q, z_r, z_n, z_count); //z_n = 2*z_q + z_r

    //if residue is 0, then 2 is a factor
    if(mpz_cmp_ui(z_r, 0)==0){
        //while the factorization isn't done and the residue is still 0
        while (mpz_cmp_ui(z_q, 1)>0 && mpz_cmp_ui(z_r, 0)==0) {
            fact_power++; //ie the actual factor can be factorized again, so ++
            mpz_cdiv_ui(z_q, z_r, z_q, 2);
        }
        set_tuple(factors[counter], z_count, fact_power);
        counter++;
        mpz_div_exact_ui(z_fact, z_fact, 2**fact_power); //remove powers of two
    }
    mpz_set_ui(z_count, 3); //set the divisor test to 3
    //while the factorization isn't done (if we achieve fact=1 and z_count = sqrt(n))
    //z_fact is the actual number we try to factorize, z_count the divisor
    while(mpz_cmp_ui(z_fact, 1)>0 && mpz_cmp_ui(z_count, z_sqrt)<=0){
        fact_power = 0;
        mpz_cdiv_ui(z_q, z_r, z_fact, z_count);
        if(mpz_cmp_ui(z_r, 0)==0){
            while (mpz_cmp_ui(z_q, 1)>0 && mpz_cmp_ui(z_r, 0)==0) {
                fact_power += 1;
                mpz_cdiv_ui(z_q, z_r, z_q, z_count);
            }
            set_tuple(factors[counter], z_count, fact_power);
            mpz_pow_ui(z_q, z_q, fact_power);
            mpz_divexact(z_fact, z_q); //we update z_fact at each factor found
        }
        counter++;
    }
}
