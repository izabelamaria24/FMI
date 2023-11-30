def primes_gen():
    primes = []
    it = 2

    while True:
        if all(it % prime != 0 for prime in primes):
            yield it
            primes.append(it)
        it += 1


n = int(input())

# primes <= n
gen_instance1 = primes_gen()
x = next(gen_instance1)
while x <= n:
    print(x)
    x = next(gen_instance1)


# first n primes
gen_instance2 = primes_gen()
for i in range(n):
    print(next(gen_instance2))
