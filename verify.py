LIM = 5000
UNDECIDED = [3323, 3803, 3929, 3947, 4139, 4583, 4783, 4871, 4987]
CHAINS = {
    3359: [1, 2, 4, 16, 15, 225, 3375, 3359],
    3623: [1, 2, 4, 5, 25, 125, 29, 3625, 3623],
    4909: [1, 2, 4, 16, 17, 289, 4913, 4909],
    4943: [1, 2, 4, 16, 17, 289, 291, 4947, 4943],
}


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def chain_is_valid(chain):
    for k in range(1, len(chain)):
        prev, v = chain[:k], chain[k]
        if not any(v == x + y or v == x * y or v == x - y
                   for x in prev for y in prev):
            return False
    return chain[0] == 1


def enumerate_up_to_depth_8(limit):
    best = {1: 0}

    def record(v, d):
        if 0 < v <= limit and (v not in best or d < best[v]):
            best[v] = d

    levels = {frozenset([1])}
    for d in range(1, 7):
        nxt = set()
        for S in levels:
            vals = sorted(S)
            for i in range(len(vals)):
                for j in range(i, len(vals)):
                    a, b = vals[i], vals[j]
                    for v in (a + b, a * b, b - a):
                        if v > 0 and v not in S:
                            record(v, d)
                            nxt.add(S | {v})
        levels = nxt
        print("|F_%d| = %d" % (d, len(levels)))

    seen7 = set()
    for S in levels:
        vals = sorted(S)
        new = set()
        for i in range(len(vals)):
            for j in range(i, len(vals)):
                a, b = vals[i], vals[j]
                for v in (a + b, a * b, b - a):
                    if v > 0 and v not in S:
                        new.add(v)
        for w in new:
            record(w, 7)
            S7 = S | {w}
            seen7.add(S7)
            v7 = sorted(S7)
            for i in range(len(v7)):
                for j in range(i, len(v7)):
                    a, b = v7[i], v7[j]
                    for v in (a + b, a * b, b - a):
                        if 0 < v <= limit and v not in S7:
                            record(v, 8)
    print("|F_7| = %d" % len(seen7))
    return best


def main():
    best = enumerate_up_to_depth_8(LIM)

    published = [0, 1, 2, 2, 3, 3, 4, 3, 3, 4, 4, 4, 5, 4, 4, 3, 4, 4, 5, 4, 5,
                 5, 5, 4, 4, 5, 4, 5, 5, 5, 5, 4, 5, 5, 5, 4, 5, 5, 5, 5, 6, 5,
                 6, 6, 5, 6, 6, 5, 5, 5, 6, 6, 6, 5, 6, 5, 6, 6, 6, 5, 6, 5, 5,
                 4, 5, 5, 6, 5, 6, 6, 6, 5, 6, 6, 5, 6, 6, 5, 5, 5, 4, 5, 5, 5,
                 6, 6, 6, 6, 6, 5, 6, 6, 6, 6, 6, 5, 6, 6, 5, 5, 6, 6, 6, 6, 6,
                 6, 6, 5]
    mismatch = [n for n in range(1, len(published) + 1)
                if best.get(n) != published[n - 1]]
    print("a(1)..a(%d) match OEIS: %s" % (len(published), not mismatch))

    for p, chain in sorted(CHAINS.items()):
        print("p = %d: prime %s, chain valid %s, length %d, endpoint %s, "
              "a(p) = %d, a(p-1) = %s"
              % (p, is_prime(p), chain_is_valid(chain), len(chain) - 1,
                 chain[-1] == p, best[p], best.get(p - 1, ">= 9")))

    viol = []
    for p in range(2, LIM + 1):
        if not is_prime(p):
            continue
        ap, am = best.get(p), best.get(p - 1)
        if ap is not None and (am is None or ap < am):
            viol.append(p)
    print("counterexamples with a(p) <= 8 below %d: %s" % (LIM, viol))

    undecided = [p for p in range(2, LIM + 1)
                 if is_prime(p) and p not in best and p - 1 not in best]
    print("pairs undecided at depth 8: %s" % undecided)
    print("matches expected list: %s" % (undecided == UNDECIDED))

    def at_most_9(n):
        for off in (1, -1, 2, -2):
            m = n - off
            if best.get(m, 99) <= 8:
                return True
        return n % 2 == 0 and best.get(n // 2, 99) <= 8

    resolved = all(at_most_9(p) and at_most_9(p - 1) for p in undecided)
    print("all undecided pairs have a(p) = a(p-1) = 9: %s" % resolved)


if __name__ == "__main__":
    main()
