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