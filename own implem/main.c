#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <stdbool.h>
#include "gmp.h"
#include <time.h>
#include "discrete_log.c"
//#include "factorization.c"
//#include "primality.c"

int main(){
    //Discrete logarithm toy example
    mpz_t z_y, z_g, z_n, z_x;
    mpz_inits(z_n, z_y, z_g, z_x, NULL);
    printf("1");
    mpz_set_str(z_n, "16435463199403521097527247317555738576767212583797448981144408576334017736529893208026370815893125000920193145583861330438025347435249912569988086823385255893", 10);
    printf("2");
    mpz_set_ui(z_g, 196); //generator certified
    printf("3");
    mpz_set_str(z_y, "3212103434892445275361416933156061057971525110940349229634527410732096681637876975514094646957614459189450224875147817461509673107323664840468622198863418521", 10); //choose any one you want
    printf("4");
    pollard_rho(z_g, z_n, z_y, z_x);
    mpz_clears(z_y, z_g, z_n, z_x, NULL);
    //output must be 32
    return 0;
}
/* Some toy exemple of the algorithms
 * Discrete logarithm
int main(){
    //Discrete logarithm toy example
    mpz_t z_y, z_g, z_n, z_x;
    mpz_inits(z_n, z_y, z_g, z_x, NULL);
    mpz_set_ui(z_n, 97);
    mpz_set_ui(z_g, 5); //generator certified
    mpz_set_ui(z_y, 35); //choose any one you want
    baby_step_giant_step(z_g, z_n, z_y, 5, z_x);
    mpz_clears(z_y, z_g, z_n, z_x, NULL);
    //output must be 32
    return 0;
}
 * RSA Factorisation
int main(){
    mpz_t z_n, z_p, z_q, z_x;
    mpz_inits(z_n, z_p, z_q, NULL);
    mpz_set_ui(z_n, 14); // divisibility by 2 test
    naive_factorization_RSA(z_n, z_p,z_q);
    mpz_set_ui(z_n, 143); // 143 = 11 * 13
    naive_factorization_RSA(z_n, z_p,z_q);
    mpz_clears(z_n, z_p, z_q, NULL);
    return 0;
}
 * Factorisation (no RSA)
int main(){
    mpz_t z_n;
    mpz_inits(z_n, z_p, z_q, NULL);
    mpz_set_ui(z_n, 1400);
    naive_factorization(z_n);
    mpz_set_ui(z_n, 143); //
    naive_factorization(z_n, z_p,z_q);
    mpz_clears(z_n, NULL);
    return 0;
}
 */