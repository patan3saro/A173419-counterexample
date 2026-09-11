# A173419-counterexample

Counterexamples to Kamenetsky's 2019 conjecture on OEIS
[A173419](https://oeis.org/A173419), with a self-contained verification script.

## The sequence

[A173419](https://oeis.org/A173419) (Charles R Greathouse IV, 2010) is the
length of the shortest computation yielding n using addition, subtraction and
multiplication, starting from 1. Equivalently: set x_0 = 1 and x_m = n, where
each x_k is x_i + x_j, x_i * x_j or x_i - x_j for some 0 <= i, j < k; then
a(n) is the least such m. For example

    1, 2, 4, 16, 15, 225, 3375, 3359

is such a computation for 3359 with 7 operations (2 = 1+1, 4 = 2*2, 16 = 4*4,
15 = 16-1, 225 = 15*15, 3375 = 225*15, 3359 = 3375-16), so a(3359) <= 7.

## The conjecture and its failure

In December 2019 Dmitry Kamenetsky conjectured, in a comment on A173419, that
`a(n) >= a(n-1)` whenever n is prime, noting that it holds for n < 1800 --
the range covered by the b-file available at the time.

The conjecture holds for every prime p < 3359 and fails there. There are
exactly four counterexamples below 5000:

| p    | a(p) | a(p-1) | p as             | shortest computation for p             |
|------|------|--------|------------------|----------------------------------------|
| 3359 | 7    | 8      | 15^3 - 16        | 1, 2, 4, 16, 15, 225, 3375, 3359       |
| 3623 | 8    | 9      | 29 * 125 - 2     | 1, 2, 4, 5, 25, 125, 29, 3625, 3623    |
| 4909 | 7    | 8      | 17^3 - 4         | 1, 2, 4, 16, 17, 289, 4913, 4909       |
| 4943 | 8    | 9      | 17 * 291 - 4     | 1, 2, 4, 16, 17, 289, 291, 4947, 4943  |

In each case the prime sits at a short additive distance from a product of
cheaply reachable numbers. Nine further pairs (p, p-1) with p prime below 5000
are left undecided by an exhaustive search at depth 8 -- 3323, 3803, 3929,
3947, 4139, 4583, 4783, 4871, 4987 -- and all nine satisfy a(p) = a(p-1) = 9,
so none of them is a counterexample.

These results are recorded in a comment on A173419 (Rosario Patanè, August 2026).

## What the script checks

`verify.py` performs four independent checks:

1. **Validity of the chains.** Each chain above starts at 1, ends at p, and
   every entry is obtained from two earlier entries by `+`, `-` or `*`.
2. **Agreement with OEIS.** It recomputes a(1)..a(108) by exhaustive
   enumeration and compares them with the published values of A173419.
3. **Exhaustiveness up to depth 8.** It enumerates all chains of length up to
   8 and reports every prime p < 5000 with a(p) < a(p-1). The four values
   above are the only ones.
4. **The undecided pairs.** It lists the primes that depth 8 cannot settle and
   verifies that each of them, and its predecessor, is reachable in 9
   operations.

## Running it

    python3 verify.py

No dependencies beyond the standard library. Tested with Python 3.12;
runtime about 10 seconds, peak memory about 130 MB.

Expected output:

    |F_1| = 1
    |F_2| = 2
    |F_3| = 8
    |F_4| = 59
    |F_5| = 663
    |F_6| = 10609
    |F_7| = 225219
    a(1)..a(108) match OEIS: True
    p = 3359: prime True, chain valid True, length 7, endpoint True, a(p) = 7, a(p-1) = 8
    p = 3623: prime True, chain valid True, length 8, endpoint True, a(p) = 8, a(p-1) = >= 9
    p = 4909: prime True, chain valid True, length 7, endpoint True, a(p) = 7, a(p-1) = 8
    p = 4943: prime True, chain valid True, length 8, endpoint True, a(p) = 8, a(p-1) = >= 9
    counterexamples with a(p) <= 8 below 5000: [3359, 3623, 4909, 4943]
    pairs undecided at depth 8: [3323, 3803, 3929, 3947, 4139, 4583, 4783, 4871, 4987]
    matches expected list: True
    all undecided pairs have a(p) = a(p-1) = 9: True

`output.txt` contains a stored copy of this run.

## Scope

The enumeration is exhaustive up to depth 8 only. Values equal to 9 are
established in two steps: the lower bound `a(n) >= 9` follows from the
exhaustive search at depth 8, and the upper bound `a(n) <= 9` from an explicit
computation of length 9. For a(3622) and a(4942) this is immediate: appending
one subtraction of 1 to the computations of 3623 and 4943 gives
`a(p-1) <= a(p) + 1 = 9`.

## Citing

Please cite the tagged release of this repository (tag and commit hash are
shown on the Releases page). See `CITATION.cff` for the metadata.


## Note on tools

The search and the verification code were developed with the assistance of a
large language model; all results reported here were independently re-run and
checked against the published values of A173419.

## License

MIT - see `LICENSE`.
