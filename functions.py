import math
import random
def FastPow(t, k, mod):
    res = 1
    while k:
        if (k & 1):
            res *= t
            res = res% mod
        k = k >> 1
        if k == 0:
            break
        t *= t
        t = t% mod
    res = res% mod
    return res
def gcd(x, y):
    if x > 0:
        x = -x
    if y < 0:
        y = -y
    while (y):
        x, y = y, x % y

    return x
def func(x):
    return x**2+1
def count_pollard_v1(n,x_0=2, write_to_file=False):
    arr=[]
    arr.append(x_0)
    r = 1
    i=0
    while r==1 or r==n:
        for x_i in arr:
            r=gcd(arr[-1]-x_i,n)
            i += 1
            if r!=1 and r!=n:
                break
        x=func(arr[-1])%n
        arr.append(x)
    return r
def jacobi_symbol(a,n):
    if gcd(a,n) != 1:
        return 0
    res = 1
    while a != 1:
        if a < 0:
            a = -a
            res = res * (-1)** ((n-1)/2)
        while a % 2 == 0:
            a = a / 2
            res = res * (-1) ** ((n**2 - 1) / 8)
        if a == 1 :
            break

        if a < n:
           temp = a
           a = n
           n = temp
           res = res * (-1) ** ((n - 1) / 2 * ((a-1)/ 2))
        if a > n:
            a = a % n
    if a == 1:
        return 1 * res
def pseudo_simple(a,p):
    if gcd(a,p) != 1:
        return 'no'
    else:
        jac = jacobi_symbol(a, p)
        if jac == -1:
            jac = p - 1
        deg = int((p - 1) / 2)
        pow = FastPow(a, deg, p)
        #pow = a ** deg
        if jac == pow % p:
            return 'yes'
        else:
            return 'no'
def count_solovei(p, k):
    i = 0
    while i < k:
        x= random.randint(2,p-1)
        if gcd(x,p) == 1:
           if pseudo_simple(a = x, p = p) == 'no':
               return 'no'
           else:
               i += 1
        else:
            return 'no'
    if i == k:
        return 'yes'



def alg_3(n):
    res = count_solovei(n, 10)
    dict_d = {}
    while res != 'yes':
        d = count_pollard_v1(n, 2)

        if d != 1:
            n = int(n / d)
            dict_d_i =canon_rozklad(d)
            if not dict_d_i:
                if d in dict_d:
                    dict_d[d]+= 1
                else:
                    dict_d[d] = 1
            for elem in list(dict_d_i.keys()):
                if elem in dict_d:
                    dict_d[elem]+= 1
                else:
                    dict_d[elem] = 1
        res = count_solovei(n, 10)
    empty_dict = canon_rozklad(n)
    if not empty_dict:
        if n in dict_d:
            dict_d[n] += 1
        else:
            dict_d[n] = 1
        return dict_d

    else:
        dict_d_i = canon_rozklad(n)
        for elem in list(dict_d_i.keys()):
            if elem in dict_d:
                dict_d[elem] += 1
            else:
                dict_d[elem] = 1
        return dict_d
def canon_rozklad(n):
    dict_d = {}

    for i in range(2,n):
        if n % i == 0:
            dict_d[i] = 1
            n = n / i
            while n % i == 0:
                dict_d[i] += 1
                n = n / i
    return dict_d
def evklid(a,n):
    arr_r = []
    arr_r.append(a)
    arr_r.append(n)
    arr_q = []
    arr_s = []
    arr_t = []
    arr_s.append(1)
    arr_s.append(0)
    arr_t.append(0)
    arr_t.append(1)
    r = -10
    while r != 1 or r !=0:
       r = arr_r[-2]%arr_r[-1]
       q = arr_r[-2] // arr_r[-1]
       arr_r.append(r)
       arr_q.append(q)
       s = arr_s[-2] - arr_q[-1] *arr_s[-1]
       t = arr_t[-2] - arr_q[-1] * arr_t[-1]
       arr_s.append(s)
       arr_t.append(t)
       #print(q,r,s,t)
       if r == 0:
           break
    return (arr_r[-2], arr_s[-2], arr_t [-2])


def get_minus(a , n):
    a = a %n
    d = math.gcd(a, n)
    if d == 1:
        r, s, t = evklid(a, n)

        a_minus = s
        return a_minus%n
    else:
        return ':('

def get_tables(n, alpha, mod, dict_d):
    deviders = list(dict_d.keys())
    tables = []
    for p in deviders:
        table_r = []
        for j in range(p):
            r = FastPow(alpha, int(((n*j) / p)), mod)
            table_r.append(int(r))
        tables.append(table_r)
    return tables

def get_x0(betta, n, mod, p, table):
    left_part = FastPow(betta, int(n / p), mod)
    for elem in table:
        if elem == left_part:
            x0 = table.index(elem)
            return x0

def get_xi(betta, n, mod, p, table, x0, alpha, deg_p):
    alpha_minus = get_minus(alpha, mod)
    arr_x = []
    arr_x.append(x0)
    deg = 0
    for i in range(1,deg_p):

        j = len(arr_x) -1
        deg += arr_x[j] * FastPow(p,j,mod)
        bottom  = (betta* FastPow(alpha_minus, deg, mod)) % mod
        right_part = FastPow(bottom, int(n/(p**(i+1))), mod)
        for elem in table:
            if elem == right_part:
                xi = table.index(elem)
                #print( xi)
                arr_x.append(xi)
                break
    return arr_x

def get_x(arr_x, p, deg_p):
    mod = p **deg_p
    x = 0
    for j in range(deg_p):
        x += arr_x[j]*(p**j)
        x = x % mod
    return x


def chinese_theorem(arr_a, arr_r):
    M = 1
    for elem in arr_a:
        M *= elem
    arr_M = []
    n = len(arr_a)
    arr_M_minus = []
    for i in range(n):
        Mi = int(M / arr_a[i])
        arr_M.append(Mi)
        Mi_minus = get_minus(Mi , arr_a[i])
        arr_M_minus.append(Mi_minus)
    x = 0
    for i in range(n):
        x += arr_r[i]* arr_M[i]*arr_M_minus[i]
        x = x % M
    return x

def get_arr_a(dict_d):
    deviders = list(dict_d.keys())
    arr_a = []
    n = len(deviders)
    for i in range(n):
        ai = deviders[i]**dict_d[deviders[i]]
        arr_a.append(ai)
    return arr_a


def get_ord(alpha, mod):
    lucky_check = FastPow(alpha, mod-1, mod)
    if lucky_check == 1:
        return mod-1
    if lucky_check != 1:
        for i in range(1,mod-1):
            res = FastPow(alpha, i, mod)
            if res == 1:
                return i

