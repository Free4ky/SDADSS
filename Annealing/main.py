import math
import random

limit_x1 = 50
limit_x2 = 50


def update_temperature(T, k):
    #return T / math.log(1 + k)
    return T * 0.95


def target_func(x1, x2):
    return 260 * x1 + 300 * x2


def limitations(x1, x2):
    return 16 * x1 + 12 * x2 <= 1200 and \
           0.2 * x1 + 0.4 * x2 <= 30 and \
           6 * x1 + 5 * x2 <= 600 and \
           3 * x1 + 4 * x2 <= 300 \
           and x1 >= 0 \
           and x2 >= 0


def init_vals():
    x1 = range(0, limit_x1)
    x2 = range(0, limit_x2)
    return x1, x2


def make_move(domain, current_state, T):
    new_state = random.choice(list(domain.keys()))
    print(f'CURRENT STATE: {new_state}')
    delta = domain[current_state] - domain[new_state]
    if delta < 0:
        return new_state
    else:
        try:
            p = math.exp(-delta / T)
        except OverflowError:
            return current_state
        return new_state if random.random() < p else current_state


def filter_domain(domain):
    for k in list(domain.keys()):
        x1, x2 = k
        if not limitations(x1, x2):
            del domain[k]
    return domain


def get_domain(x1, x2):
    result = {}
    for i in x1:
        for j in x2:
            result[(i, j)] = target_func(i, j)
    result = filter_domain(result)
    return result


def annealing():
    x1, x2 = init_vals()
    domain = get_domain(x1, x2)
    best_state = (random.choice(x1), random.choice(x2))
    T = 1.
    k = 1
    while T > 1e-3:
        new_state = make_move(domain, best_state, T)
        print(f'BEST STATE: {best_state}')
        if target_func(new_state[0], new_state[1]) > target_func(best_state[0], best_state[1]):
            best_state = new_state
        T = update_temperature(T, k)
        k += 1
        print(f'Iteration:{k}')
    return new_state, best_state, target_func(best_state[0], best_state[1])


if __name__ == '__main__':
    last_state, best_state, max_value = annealing()
    print(f'Max: {max_value}\nBest_state: x1 = {best_state[0]}, x2 = {best_state[1]}')
