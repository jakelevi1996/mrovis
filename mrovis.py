""" See https://docs.python.org/3/howto/mro.html """

class Displayer:
    def __init__(self):
        self._indent_str = "| "
        self._stack = []

    def get_arg_str(self, *c_lists: list[type]):
        return ", ".join(
            "".join(
                c.__name__.replace("object", "O")
                for c in c_list
            )
            for c_list in c_lists
        )

    def push(self, function_name, *c_lists: list[type]):
        indent = self._indent_str * len(self._stack)
        arg_str = self.get_arg_str(*c_lists)
        call_str = "%s%s(%s) =" % (indent, function_name, arg_str)
        self._stack.append(call_str)
        print(call_str, "...")

    def pop(self, *c_lists: list[type]):
        arg_str = self.get_arg_str(*c_lists)
        call_str = self._stack.pop()
        print(call_str, arg_str)

displayer = Displayer()

def linearise(c: type) -> list[type]:
    displayer.push("linearise", [c])

    if len(c.__bases__) == 0:
        tail = []
    else:
        tail = merge(
            *[linearise(b) for b in c.__bases__],
            [b for b in c.__bases__],
        )

    displayer.pop([c] + tail)
    return [c] + tail

def merge(*c_lists: list[type]) -> list[type]:
    displayer.push("merge", *c_lists)

    tail_set = set(
        c
        for c_list in c_lists
        for c in c_list[1:]
    )
    good_heads = [
        c_list[0]
        for c_list in c_lists
        if c_list[0] not in tail_set
    ]
    if len(good_heads) == 0:
        raise ValueError("No good heads")

    head = good_heads[0]
    pruned_c_lists = [
        [c for c in c_list if (c is not head)]
        for c_list in c_lists
    ]
    pruned_c_lists = [
        c_list
        for c_list in pruned_c_lists
        if len(c_list) > 0
    ]
    tail = merge(*pruned_c_lists) if (len(pruned_c_lists) > 0) else []

    displayer.pop([head] + tail)
    return [head] + tail


O = object
class F(O): pass
class E(O): pass
class D(O): pass
class C(D,F): pass
# class B(D,E): pass
class B(E,D): pass
class A(B,C): pass

linearise(A)

# linearise(A) = ...
# | linearise(B) = ...
# | | linearise(E) = ...
# | | | linearise(O) = ...
# | | | linearise(O) = O
# | | | merge(O, O) = ...
# | | | merge(O, O) = O
# | | linearise(E) = EO
# | | linearise(D) = ...
# | | | linearise(O) = ...
# | | | linearise(O) = O
# | | | merge(O, O) = ...
# | | | merge(O, O) = O
# | | linearise(D) = DO
# | | merge(EO, DO, ED) = ...
# | | | merge(O, DO, D) = ...
# | | | | merge(O, O) = ...
# | | | | merge(O, O) = O
# | | | merge(O, DO, D) = DO
# | | merge(EO, DO, ED) = EDO
# | linearise(B) = BEDO
# | linearise(C) = ...
# | | linearise(D) = ...
# | | | linearise(O) = ...
# | | | linearise(O) = O
# | | | merge(O, O) = ...
# | | | merge(O, O) = O
# | | linearise(D) = DO
# | | linearise(F) = ...
# | | | linearise(O) = ...
# | | | linearise(O) = O
# | | | merge(O, O) = ...
# | | | merge(O, O) = O
# | | linearise(F) = FO
# | | merge(DO, FO, DF) = ...
# | | | merge(O, FO, F) = ...
# | | | | merge(O, O) = ...
# | | | | merge(O, O) = O
# | | | merge(O, FO, F) = FO
# | | merge(DO, FO, DF) = DFO
# | linearise(C) = CDFO
# | merge(BEDO, CDFO, BC) = ...
# | | merge(EDO, CDFO, C) = ...
# | | | merge(DO, CDFO, C) = ...
# | | | | merge(DO, DFO) = ...
# | | | | | merge(O, FO) = ...
# | | | | | | merge(O, O) = ...
# | | | | | | merge(O, O) = O
# | | | | | merge(O, FO) = FO
# | | | | merge(DO, DFO) = DFO
# | | | merge(DO, CDFO, C) = CDFO
# | | merge(EDO, CDFO, C) = ECDFO
# | merge(BEDO, CDFO, BC) = BECDFO
# linearise(A) = ABECDFO
