from copy import deepcopy
### FONCTIONS FOR HILL DECRYPT ###

def supp_row_col(M: list,i,j):
    L = deepcopy(M)
    for k in range(len(L)):
        L[k].remove(M[k][j])
    L.remove(L[i])
    return L
    

def matrix_mod_product(A,B,n):
    if A==None or B==None:
        return None
    if len(A[0])!=len(B):
        raise ArithmeticError("The sizes of matrix doesn't correspond for the product")
    if type(B[0])==list:
        P = [[0 for i in range(len(A))] for j in range(len(B[0]))]
        for i in range(len(A)):
            for j in range(len(B[0])):
                for k in range(len(A[0])):
                    P[i][j] = (P[i][j]+A[i][k]*B[k][j]) % n
        return P
    P = [0 for i in range(len(A))]
    for i in range(len(A)):
        for j in range(len(A[0])):
            P[i] = (P[i]+(A[i][j]*B[j])) %n

    return P

def matrix_mod_det(M, n):
    det = 0
    if len(M)==2 and len(M[0])==2:
        return (M[0][0]*M[1][1]-M[1][0]*M[0][1])%n
    for k in range(len(M[0])):
        #we choose the first line to compute the determinant
        a_k = (-1)**(k)*M[0][k] % n 
        Mk = []
        for i in range(1, len(M)):
            Li = []
            for j in range(len(M[0])):
                #we go to each rows, but don't take the column k
                if j!=k:
                    Li.append(M[i][j])
            Mk.append(Li)
        det += (M[0][k]*matrix_mod_det(Mk,n)) % n
    return det

#Invert a matrix M modulo n
def matrix_mod_inv(M, n):
    if matrix_mod_det(M,n)==0:
        print("Matrix isn't invertible, because determinant is zero.")
        return None
    try:
        d = pow(matrix_mod_det(M,n), -1, n)
    except ValueError:
        print("The determinant isn't invertible with the current modulo.")
        return None
    if len(M)==2:
        return [[(d*M[1][1])%n, (-M[1][0]*d)%n],
                [(-M[0][1]*d)%n, (d*M[0][0])%n]] # easy way
    Inv = [[0 for i in range(len(M[0]))] for j in range(len(M[0]))]
    #We compute first the covariant matrix, then the inverse
    for i in range(len(M)):
        for j in range(len(M[0])):
            Mij = supp_row_col(M,i,j)
            Inv[i][j] = ((-1)**(i+j)*d*matrix_mod_det(Mij, n)) % n
    Inv = [[Inv[j][i]%n for i in range(len(Inv))] for j in range(len(Inv[0]))]
    return Inv

#######################################

def floyd(f, x0) -> (int, int):
    """Floyd's cycle detection algorithm."""
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # at some point, the distance between them will be
    # divisible by the period λ.
    tortoise = f(x0) # f(x0) is the element/node next to x0.
    hare = f(f(x0))
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))
  
    # At this point the tortoise position, ν, which is also equal
    # to the distance between hare and tortoise, is divisible by
    # the period λ. So hare moving in cycle one step at a time, 
    # and tortoise (reset to x0) moving towards the cycle, will 
    # intersect at the beginning of the cycle. Because the 
    # distance between them is constant at 2ν, a multiple of λ,
    # they will agree as soon as the tortoise reaches index μ.

    # Find the position μ of first repetition.    
    mu = 0
    tortoise = x0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)   # Hare and tortoise move at same speed
        mu += 1
 
    # Find the length of the shortest cycle starting from x_μ
    # The hare moves one step at a time while tortoise is still.
    # lam is incremented until λ is found.
    lam = 1
    hare = f(tortoise)
    while tortoise != hare:
        hare = f(hare)
        lam += 1
 
    return lam, mu