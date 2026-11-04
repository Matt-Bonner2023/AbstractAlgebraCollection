from Monoids import Monoid
from itertools import permutations

class Group(Monoid):
    def __init__(self, monoid_set, operation, identity, name, associative=False, invertible=False):
        super().__init__(
            monoid_set,
            operation,
            identity,
            name,
            associative

        )
        self.invertible = invertible
        self.verify_group()

    def verify_group(self):
        invertible_elements = set()
        if not self.invertible:
            for a in self.monoid_set:
                for b in self.monoid_set:
                    if self.operation(a,b) == self.identity and self.operation(b,a) == self.identity:
                        invertible_elements.add(a)
                        break

            if len(invertible_elements) != len(self.monoid_set):
                raise TypeError(f"Every element in Group must have 1 inverse")


    def inverse(self, element):
        if element not in self.monoid_set:
            raise ValueError(f"{element} not in Group")

        for a in self.monoid_set:
            if self.operation(a,element) == self.identity and self.operation(element,a) == self.identity:
                return a

        raise ValueError(f"No inverse for {element} in Group")

    def is_abelian(self):
        return super().commutes()

    def order(self,element):
        if element not in self.monoid_set:
            raise ValueError(f"{element} not in Group")
        i = 0
        while i < len(self.monoid_set):
            i += 1
            if self.powers_of_element(element,i) == self.identity:
                return i

    def isomorphic_to(self, other):
        # Check that the groups have the same cardinality
        if len(self.monoid_set) != len(other.monoid_set):
            return False, (
                f"Isomorphic groups require the same cardinality: "
                f"{len(self.monoid_set)} != {len(other.monoid_set)}"
            )

        # Check that the groups have the same distribution of element orders
        orders = sorted(self.order(a) for a in self.monoid_set)
        other_orders = sorted(other.order(b) for b in other.monoid_set)

        if orders != other_orders:
            return False, "Isomorphic groups require matching element orders"

        # Establish sets without the identity elements
        no_identity_set = self.monoid_set.copy()
        other_no_identity_set = other.monoid_set.copy()

        no_identity_set.remove(self.identity)
        other_no_identity_set.remove(other.identity)

        # Check that the group operation is preserved:
        # f(a * b) = f(a) * f(b)
        sources = list(no_identity_set)
        mapping = {}
        for images in permutations(other_no_identity_set):
            mapping = {self.identity: other.identity}

            for source, image in zip(sources, images):
                mapping[source] = image

        return f"'{self.name}' is isomorphic to '{other.name}' by potential mapping:\n{mapping}"


    def cyclic_subgroup(self,element):
        if element not in self.monoid_set:
            raise ValueError(f"{element} not in Group")

        subgroup = []
        for exp in range(len(self.monoid_set)):
            if self.powers_of_element(element,exp) not in subgroup:
                subgroup.append(self.powers_of_element(element,exp))
            else:
                break

        subgroup.sort()

        return subgroup


    def generators(self):
        gens = []
        for item in self.monoid_set:
            if self.cyclic_subgroup(item) == self.monoid_set:
                gens.append(item)

        return gens

    def is_cyclic(self):
        if len(self.generators()) <= 0:
            return False
        return True



D3 = Group(
    monoid_set=[
        (0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1)
    ],
    operation=lambda a, b: (
        (a[0] + (-1) ** a[1] * b[0]) % 3,
        (a[1] + b[1]) % 2
    ),
    identity=(0, 0),
    name="D3"
)
def addition_mod_6(a,b):
    return (a+b)%6
Naturals_mod_6 = Group(
    monoid_set=[0, 1, 2,3,4,5],
    operation=addition_mod_6,
    identity= 0,
    name= "Naturals_mod_6"
)

G = Group(
    monoid_set=[0,2,4,6,8,10],
    operation= lambda a,b: (a+b)%12,
    identity= 0,
    name="Addition_mod_12_even_integers"
)

def multiplication_mod_7(a,b):
    return (a*b)%7

G7 = Group(
    monoid_set=[1,2,3,4,5,6],
    operation=multiplication_mod_7,
    identity=1,
    name="Multiplication_mod_7"
)
