import functions as f
import time


def main_alg(alpha, betta, mod, n):
    start = time.time()
    if mod > 100:
        dict_d = f.alg_3(n)
    else:
        dict_d = f.canon_rozklad(n)
    tables = f.get_tables(n, alpha, mod,dict_d)
    deviders = list(dict_d.keys())
    arr_x = []
    for i  in range(len(deviders)):
        x0 = f.get_x0(betta, n, mod, deviders[i], tables[i])
        arr_xi = f.get_xi(betta, n, mod, deviders[i],  tables[i], x0, alpha, dict_d[deviders[i]])
        x = f.get_x(arr_xi, deviders[i], dict_d[deviders[i]])
        arr_x.append(x)
    arr_a = f.get_arr_a(dict_d)
    result = f.chinese_theorem(arr_a,arr_x)
    print('x = ', result)
    end = time.time()
    answ = f.FastPow(alpha, result, mod)
    print('time passed :' , abs(end - start))
    #print(answ)

print('please enter a value for alpha')
alpha = int(input())
print('please enter a value for betta')
betta = int(input())
print('please enter a value for p')
p = int(input())


n = f.get_ord(alpha,p)
main_alg(alpha, betta, p, n)

