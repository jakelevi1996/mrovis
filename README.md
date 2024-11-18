# mrovis

## Examples

```python
class F: pass
class E: pass
class D: pass
class C(D,F): pass
class B(D,E): pass
# class B(E,D): pass
class A(B,C): pass

displayer.set_sep("")
linearise(A)

# L(A) = A + merge(L(B), L(C), BC)
# |   L(B) = B + merge(L(D), L(E), DE)
# |   |   L(D) = D + merge(L(O), O)
# |   |   L(D) = D + merge(O, O)
# |   |   L(D) = D + O
# |   |   L(E) = E + merge(L(O), O)
# |   |   L(E) = E + merge(O, O)
# |   |   L(E) = E + O
# |   L(B) = B + merge(DO, EO, DE)
# |   L(B) = B + D + merge(O, EO, E)
# |   L(B) = B + D + E + merge(O, O)
# |   L(B) = B + D + E + O
# |   L(C) = C + merge(L(D), L(F), DF)
# |   |   L(D) = D + merge(L(O), O)
# |   |   L(D) = D + merge(O, O)
# |   |   L(D) = D + O
# |   |   L(F) = F + merge(L(O), O)
# |   |   L(F) = F + merge(O, O)
# |   |   L(F) = F + O
# |   L(C) = C + merge(DO, FO, DF)
# |   L(C) = C + D + merge(O, FO, F)
# |   L(C) = C + D + F + merge(O, O)
# |   L(C) = C + D + F + O
# L(A) = A + merge(BDEO, CDFO, BC)
# L(A) = A + B + merge(DEO, CDFO, C)
# L(A) = A + B + C + merge(DEO, DFO)
# L(A) = A + B + C + D + merge(EO, FO)
# L(A) = A + B + C + D + E + merge(O, FO)
# L(A) = A + B + C + D + E + F + merge(O, O)
# L(A) = A + B + C + D + E + F + O

class F: pass
class E: pass
class D: pass
class C(D,F): pass
# class B(D,E): pass
class B(E,D): pass
class A(B,C): pass

displayer.set_sep("")
linearise(A)

# L(A) = A + merge(L(B), L(C), BC)
# |   L(B) = B + merge(L(E), L(D), ED)
# |   |   L(E) = E + merge(L(O), O)
# |   |   L(E) = E + merge(O, O)
# |   |   L(E) = E + O
# |   |   L(D) = D + merge(L(O), O)
# |   |   L(D) = D + merge(O, O)
# |   |   L(D) = D + O
# |   L(B) = B + merge(EO, DO, ED)
# |   L(B) = B + E + merge(O, DO, D)
# |   L(B) = B + E + D + merge(O, O)
# |   L(B) = B + E + D + O
# |   L(C) = C + merge(L(D), L(F), DF)
# |   |   L(D) = D + merge(L(O), O)
# |   |   L(D) = D + merge(O, O)
# |   |   L(D) = D + O
# |   |   L(F) = F + merge(L(O), O)
# |   |   L(F) = F + merge(O, O)
# |   |   L(F) = F + O
# |   L(C) = C + merge(DO, FO, DF)
# |   L(C) = C + D + merge(O, FO, F)
# |   L(C) = C + D + F + merge(O, O)
# |   L(C) = C + D + F + O
# L(A) = A + merge(BEDO, CDFO, BC)
# L(A) = A + B + merge(EDO, CDFO, C)
# L(A) = A + B + E + merge(DO, CDFO, C)
# L(A) = A + B + E + C + merge(DO, DFO)
# L(A) = A + B + E + C + D + merge(O, FO)
# L(A) = A + B + E + C + D + F + merge(O, O)
# L(A) = A + B + E + C + D + F + O

for c in [A, B, C, D, E, F]:
    assert tuple(linearise(c)) == c.__mro__
```
