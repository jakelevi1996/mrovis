""" See https://docs.python.org/3/howto/mro.html """

class _Displayer:
    def __init__(self):
        self.set_indent("|   ")
        self.set_sep("+")
        self.set_sep(" + ", long=True)
        self._lin_stack: list[str] = []
        self._merge_stack: list[list[type]] = []

    def set_indent(self, indent_str: str):
        self._indent_str = indent_str

    def set_sep(self, sep: str, long=False):
        if long:
            self._long_sep = sep
        else:
            self._short_sep = sep

    def get_arg_str(self, *c_lists: list[type], long=False):
        sep = self._long_sep if long else self._short_sep
        return ", ".join(
            sep.join(
                c.__name__.replace("object", "O")
                for c in c_list
            )
            for c_list in c_lists
        )

    def push_linearise(self, c: type):
        indent = self._indent_str * len(self._lin_stack)
        c_str = c.__name__.replace("object", "O")
        call_str = "%sL(%s) =" % (indent, c_str)
        merge_args = [
            *[
                "L(%s)" % b.__name__.replace("object", "O")
                for b in c.__bases__
            ],
            self.get_arg_str(c.__bases__),
        ]
        expr_str = "%s + merge(%s)" % (c_str, ", ".join(merge_args))
        self._lin_stack.append(call_str)
        self._merge_stack.append([c])
        print(call_str, expr_str)

    def pop_linearise(self, *c_lists: list[type]):
        call_str = self._lin_stack.pop()
        arg_str = self.get_arg_str(*c_lists, long=True)
        self._merge_stack.pop()
        print(call_str, arg_str)

    def display_merge(self, *c_lists: list[type]):
        merged_str = self.get_arg_str(self._merge_stack[-1], long=True)
        arg_str = self.get_arg_str(*c_lists)
        call_str = "%s + merge(%s)" % (merged_str, arg_str)
        print(self._lin_stack[-1], call_str)

    def push_merge(self, head: type):
        self._merge_stack[-1].append(head)

displayer = _Displayer()

def linearise(c: type) -> list[type]:
    if len(c.__bases__) == 0:
        return [c]

    displayer.push_linearise(c)

    tail = merge(
        *[linearise(b) for b in c.__bases__],
        [b for b in c.__bases__],
    )

    displayer.pop_linearise([c] + tail)
    return [c] + tail

def merge(*c_lists: list[type]) -> list[type]:
    if len(c_lists) == 0:
        return []

    displayer.display_merge(*c_lists)

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

    displayer.push_merge(head)
    return [head] + merge(*pruned_c_lists)

O = object
class F(O): pass
class E(O): pass
class D(O): pass
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
