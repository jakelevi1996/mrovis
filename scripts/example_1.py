import mrovis as mv

class F: pass
class E: pass
class D: pass
class C(D,F): pass
class B(D,E): pass
# class B(E,D): pass
class A(B,C): pass

mv.displayer.set_sep("")
mv.linearise(A)
