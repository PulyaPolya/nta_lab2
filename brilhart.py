import math
import functions as f
from math import exp, sqrt, log2
from vectors import add_one
import numpy as np


def get_zepnaya_fraction_a(n, k):
    v = 1
    alpha_0=math.sqrt(n)
    alpha = alpha_0
    a=int(alpha)
    u=a
    arr_a=[]
    arr_a.append(a)
    i = 0
    while i < k:
        v = (n - u ** 2) / v
        alpha = (alpha_0 + u) / v
        a = int(alpha)
        u = a * v -u
        arr_a.append(a)
        i += 1
        #print('v = ', v, 'alpha = ', alpha, 'a = ', a, 'u = ', u)
    return arr_a

def get_fraction(n, k):
    v = 1
    alpha_0=math.sqrt(n)
    alpha = alpha_0
    a=int(alpha)
    u=a
    arr_a=[]
    arr_a.append(a)
    i = 0
    while i < k:
        v = (n - u ** 2) / v
        alpha = (alpha_0 + u) / v
        a = int(alpha)
        u = a * v -u
        arr_a.append(a)
        i += 1
        #print('v = ', v, 'alpha = ', alpha, 'a = ', a, 'u = ', u)
    return arr_a
def get_row_b_bsq(arr, n):
    b=1
    b_prev = 0
    b_arr=[]
    b_arr.append(b)
    b_sq = []
    b_sq.append(b)
    for a in arr:
        temp = b
        b = b * a + b_prev
        b = b % n

        b_arr.append(b)
        b_prev = temp
        b_square = (b ** 2) % n
        if b_square > n/2:
            b_square = b_square - n
        if b_square in b_sq:
            pass
        else:
            b_sq.append(b_square)
    return (b_arr, b_sq)
def get_mod(k,n):
    k = k%n
    if k > n/2:
        k = k - n
    return k
def get_primes():
    file_name= 'prime'
    res=[]
    with open(file_name, 'r') as file:
        content=file.read()
        numbers= content.split()
    for number in numbers:
        res.append(int(number))
    return res
def get_b(n, increment = 0):
    B = []
    B.append(-1)
    primes = get_primes()
    a = 1 / (sqrt(2))+0.1
    if increment:
        a += 5 * increment / n
    L=exp((log2(n) * log2(log2(n)))** 0.5)

    limit = L ** a
    for number in primes:
        if number < limit:
            if f.jacobi_symbol(n, number) == 1:
                B.append(number)
            elif f.jacobi_symbol(n, number) == 0:
                pass
                #raise Exception
        else:
            break
    B.pop(-2)
    return B
def get_gladki_vectors(n, b_normal, b_sq, B):
    k = len(B) - 1
    arr = get_zepnaya_fraction_a(n, k)
    #b_sq = get_row_b_bsq(arr, n)[1]
    gladki = []
    gladki_normal = []
    vectors = {}
    #B.remove(-1)
    b = -1
    for b in b_sq:
        vector = []
        b_value = b
        for prime in B:
            vector_comp = 0
            if b < 0:
                vector_comp += 1
                b = abs(b)
            if f.gcd(b, prime) != 1:
                while f.gcd(b, prime) != 1:
                    b = b / prime
                    vector_comp += 1
            vector.append(vector_comp)
        if abs(b) == 1 and b_value != 1:
            vectors[b_value] = vector
            gladki.append((b_value)%n)
            index = b_sq.index(b_value)
            gladki_normal.append(b_normal[index])
    return (vectors,gladki_normal, gladki)


def get_coef(vectors, zero):
    numb_of_vect = len(vectors)
    #vect_bin = copy.copy(vectors)
    vect_bin = {}
    for elem in vectors:
        vect_bin[elem] = vectors[elem].copy()
        for i in range(len(vect_bin[elem])):
            vect_bin[elem][i] = vect_bin[elem][i]%2
   #zero = [0] * len(vect_bin)
    max = 0
    arr = []

    arr_vect = []
    for elem in vect_bin:
        arr_vect.append(vect_bin[elem])
    zero_arr=[]
    keys = list(vect_bin.keys())
    length = len(vect_bin[keys[0]])
    for t in range (length):
        zero_arr.append(0)
    #zero_arr = result[:]
    result = zero_arr[:]
    zero_arr = np.array(zero_arr)
    start = 0
    numb_it = 0
    arr = zero[:]
    while start != 1 or not (result == zero_arr).all():
    #while True:

        arr = add_one(arr)
        result = zero_arr[:]
        start = 1
        '''
        for k in range (length):
            i = 0
            for number in keys:
                result[k] += vectors[number][k] * arr[i]
                result[k] = result[k] % 2
                i += 1
        '''
        vect = np.array(arr_vect)
        v = np.array(arr)
        v = np.reshape(v, (len(arr_vect), 1))
        result = np.multiply(vect, v)
        result = np.sum(result, axis=0, keepdims=False)
        result = result % 2
        #print(result)
        #print(arr, '\n')
        numb_prev = numb_it
        numb_it += 1
        if max < numb_it:
           max = numb_it
        #print(numb_it)
        if numb_it >= 4294967296 or numb_it < numb_prev:
            return "stop immedeatily!!!!"
    return arr
def get_X_Y(arr_x, vectors, gladki, B, k, n, b_sq):
    x = 1
    for i in range (len(vectors)):
        x =(x * (gladki[i] ** arr_x[i])) %n
    keys = list(vectors.keys())
    y = 1
    length = len(vectors[keys[0]])
    '''
    for j in range(length):
        deg_p = 0
        for number in keys:
            deg_p += vectors[number][j] * arr_x[j]
        y = y * (b[j] ** deg_p) % n
    '''
    #i = 0
    #while i < n:
    y = 1
    arr_k = list(vectors.keys())
    '''
    for j in range (len(arr_x)):
        if arr_x[j] !=0:
                y = y*arr_k[j]
                #y = y*  b_sq[j+1]
    y =int(sqrt(y))
    '''
    for j in range(length):
        deg_p = 0
        i = 0
        for number in keys:
            deg_p += vectors[number][j] * arr_x[i]
            i += 1
        y = y * (B[j] ** deg_p) % n

    y = int(sqrt(y))

    return (x,y)
def get_gcd(x, y, n):
    if f.gcd(x + y, n) != 1:
        return f.gcd(x + y, n)
    else:
        return f.gcd((x - y)%n, n)

def brilhart_moris(n,write_to_file=False):
    result = 1
    increment = 0
    X_arr = []
    B = get_b(n, increment)
    #random.shuffle(B)
    #print(B)
    k = len(B) -1
    arr_a = get_zepnaya_fraction_a(n, k + 1)
    arr_b,arr_b_sq  = get_row_b_bsq(arr_a, n)

    vectors, gladki, gladki_square = get_gladki_vectors(n, arr_b, arr_b_sq, B)

    #print('B',len(B))
    #print('gladki', len(gladki))
    #gladki = []
    i = 0
    increment += 1
    #print(vectors)
    #print(gladki)
    #print(gladki_square)
    arr_coef = [0] * len(vectors)
    while result == 1 or result == n:
        arr_coef = get_coef(vectors, arr_coef)
        X, Y = get_X_Y(arr_coef, vectors,gladki, B, k, n, arr_b_sq)
        X_arr.append(X)
        result = get_gcd(X, Y, n)
    if write_to_file:
        f.write_to_csv(write_to_file, str(result))
    return result
'''
arr = [99400891, 9073333, 12422253]
for n in arr:

    start = time.time()
    d = brilhart_moris(n)
    end = time.time()
    print('n= ', n, ' d= ', d, ' ', end - start, 's')
    '''
