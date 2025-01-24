#include "stdbool.h"
#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "gmp.h"

// The goal of these functions is to have some primality test (not certificate)
// The Rabin-Miller one is the most efficient here, with the less false-positive rate
// You can improve this with a sieve, or with residues

bool test_fermat_base(mpz_t z_n, mpz_t z_a, mpz_t z_ord){
    mpz_powm(z_a, z_a, z_ord, z_n); //z_a=a^ord mod n
    if(mpz_cmp_ui(z_a, 1)!=0){
        return false;
    }
    return true;
}

bool test_fermat(mpz_t z_n, int t){
    mpz_t z_base, z_ord;
    mpz_inits(z_base, z_ord, NULL);
    mpz_sub_ui(z_ord, z_n, 1); //z_ord = z_n-1
    gmp_randstate_t r_gen;
    gmp_randinit_default (r_gen);
    gmp_randseed_ui(r_gen, time(NULL));
    for(int i=0; i<t; i++){
        mpz_urandomm(z_base, r_gen, z_ord); //generate random number in [0, z_n-2]
        if(mpz_cmp_ui(z_base, 1)<=0){
            if (mpz_cmp_ui(z_n, 3)==0){
                gmp_randclear(r_gen);
                mpz_clears(z_base, z_ord, NULL);
                return true;
            }//because 3 is prime, and add 2 make some troubles
            mpz_add_ui(z_base, z_base, 2);} //z_base need to be greater than 2
        if(!test_fermat_base(z_n, z_base, z_ord)){
            gmp_randclear(r_gen);
            mpz_clears(z_base, z_ord, NULL);
            return false;
        }
    }
    gmp_randclear(r_gen);
    mpz_clears(z_base, z_ord, NULL);
    return true;
}

bool test_miller_rabin_base(mpz_t z_n, mpz_t z_a, mpz_t z_ord, mpz_t z_r, int s){
    mpz_powm(z_a, z_a, z_r, z_n); //z_a=z_a^r mod n
    if(mpz_cmp_ui(z_a, 1)!=0 && mpz_cmp(z_a, z_ord)!=0){
        int j = 1;
        while(j<=s-1 && mpz_cmp(z_a,z_ord)!=0){
            mpz_powm_ui(z_a, z_a, 2, z_n); // z_a = z_a^2 mod n
            if(mpz_cmp_ui(z_a, 1)==0){ return false;}
            j++;
        }
        if(mpz_cmp(z_a, z_ord)!=0){ return false;}
    }
    return true;
}

bool test_miller_rabin(mpz_t z_n, int t){
    mpz_t z_base, z_ord, z_r;
    int s=0;
    mpz_inits(z_base, z_ord, z_r, NULL);
    mpz_sub_ui(z_ord, z_n, 1); //z_ord = z_n-1
    mpz_set(z_r, z_ord);
    gmp_randstate_t r_gen;
    gmp_randinit_default (r_gen);
    gmp_randseed_ui(r_gen, time(NULL));
    //while loop gives z_r*2^s=z_n-1 decomposition
    while(mpz_even_p(z_r)==0){
        s += 1;
        mpz_divexact_ui(z_r, z_r, 2);
    }
    for(int i=0; i<t; i++){
        mpz_urandomm(z_base, r_gen, z_ord); //generate random number in [0, z_n-2]
        if(mpz_cmp_ui(z_base, 1)<=0){
            if (mpz_cmp_ui(z_n, 3)==0){//because 3 is prime, and add 2 make some troubles
                mpz_clears(z_base, z_ord, z_r, NULL);
                return true;
            }
            mpz_add_ui(z_base, z_base, 2);} //z_base need to be greater than 2
        if(!test_miller_rabin_base(z_n, z_base, z_ord, z_r, s)){
            gmp_randclear(r_gen);
            mpz_clears(z_base, z_ord, z_r, NULL);
            return false;
        }
    }
    gmp_randclear(r_gen);
    mpz_clears(z_base, z_ord, z_r, NULL);
    return true;
}

//put k-th first prime in the sieve
void init_sieve(unsigned long* sieve, int size){
    if(size==0){printf("The sieve is empty !?\n");}
    else{
        sieve[0] = 3;
        mpz_t z_n;
        mpz_init_set_ui(z_n, 5);
        int i = 1;
        //fill the sieve until we reach k primes
        while(i<size){
            //we choose to fix t=5, because z_n is relatively low
            if(test_miller_rabin(z_n, 5)){
                unsigned long prime = mpz_get_ui(z_n);
                sieve[i] = prime;
                i++;
            }
            mpz_add_ui(z_n, z_n, 1); // z_n += 1
        }
        mpz_clear(z_n);
    }
}

void init_residue(unsigned long* sieve, unsigned long* residue, mpz_t z_n, int size){
    mpz_t z_r;
    mpz_init(z_r);
    for(int i=0; i<size; i++){
        mpz_mod_ui(z_r, z_n, sieve[i]);
        residue[i] = mpz_get_ui(z_r);
    }
    mpz_clear(z_r);
}

void update_residue(unsigned long* sieve, unsigned long* residue, mpz_t z_n, int size){
    bool residue_zero = true;
    //while a residue is zero, we increment by 2 the number and residue (mod sieve)
    while(residue_zero==true){
        residue_zero = false;
        mpz_add_ui(z_n, z_n, 2);
        for(int i=0; i<size; i++){
            residue[i] = (residue[i]+2) % sieve[i];
            if(residue[i]==0){residue_zero=true;}
        }
    }
}

bool test_miller_rabin_sieve(mpz_t z_n, int t, int sieve_size){
    gmp_randstate_t n_gen;
    gmp_randinit_default (n_gen);
    gmp_randseed_ui(n_gen, time(NULL));
    unsigned long* sieve = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    init_sieve(sieve, sieve_size);
    for(int i=0; i<sieve_size; i++){
        if(mpz_divisible_ui_p(z_n, sieve[i])==1){
            free(sieve);
            return true;
        }
    }
    free(sieve);
}

void next_prime(mpz_t z_n, int round, int sieve_size){
    unsigned long* sieve = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    unsigned long* residue = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    init_sieve(sieve, sieve_size);
    init_residue(sieve, residue, z_n, sieve_size);
    do {
        update_residue(sieve, residue, z_n, sieve_size);
    } while(!test_miller_rabin(z_n, round));
    free(sieve);
    free(residue);
}

//a prime generator, with a given bit-size, with next prime method
void prime_generator_np_method(mpz_t z_n, int bit_size, int sieve_size, int round){
    gmp_randstate_t n_gen;
    gmp_randinit_default (n_gen);
    gmp_randseed_ui(n_gen, time(NULL));
    unsigned long* sieve = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    unsigned long* residue = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    mpz_urandomb(z_n, n_gen, bit_size);
    mpz_setbit(z_n, bit_size);
    mpz_setbit(z_n, 0);
    init_residue(sieve, residue, z_n, sieve_size);
    while(!test_miller_rabin(z_n, round)){
        update_residue(sieve, residue, z_n, sieve_size);
    }
    free(sieve);
    free(residue);
    gmp_randclear(n_gen);
}

// 7 seconds for generate 100 1024-bits prime
void prime_generator(mpz_t z_n, int bit_size, int sieve_size, int round){
    gmp_randstate_t n_gen;
    gmp_randinit_default (n_gen);
    gmp_randseed_ui(n_gen, time(NULL));
    unsigned long* sieve = (unsigned long*) malloc(sieve_size * sizeof(unsigned long));
    bool is_div_sieve = true;
    mpz_urandomb(z_n, n_gen, bit_size);
    mpz_setbit(z_n, bit_size);
    mpz_setbit(z_n, 0);
    do{
        is_div_sieve = true;
        while(is_div_sieve){
            mpz_urandomb(z_n, n_gen, bit_size);
            mpz_setbit(z_n, bit_size); //exactly bit_size bit prime
            mpz_setbit(z_n, 0);
            is_div_sieve = false;
            for(int i=0; i<sieve_size; i++){
                if(mpz_divisible_ui_p(z_n, sieve[i])==1){is_div_sieve = true;}
            }
        }
        //gmp_printf("Number %Zu complete the sieve test. Now it's time for Miller-Rabin.\n", z_n);
    }while(!test_miller_rabin(z_n, round));
    free(sieve);
    gmp_randclear(n_gen);
}