# Monoids are associative, closed, and have an identity element
class Monoid:
    def __init__(self, monoid_set, operation, identity, name, associative= False):
        self.monoid_set = monoid_set
        self.operation = operation
        self.identity = identity
        self.name = name
        self.associative = associative
        self.verify_monoid()

    def verify_monoid(self):
        # Identity in monoid
        if self.identity not in self.monoid_set:
            raise TypeError(f"Identity must be in set: {self.identity}")
        # Valid Identity
        for a in self.monoid_set:
            if self.operation(a,self.identity) != a:
                raise TypeError(f"Invalid Identity: {a} ⨁ {self.identity} = {self.operation(a,self.identity)}, not {a}")

        # Closure
        for a in self.monoid_set:
            for b in self.monoid_set:
                if self.operation(a, b) not in self.monoid_set:
                    raise TypeError(f"Closure is not satisfied: {a} ⨁ {b} = {self.operation(a, b)}, is outside of set")

        # Associativity
        if not self.associative:
            for a in self.monoid_set:
                for b in self.monoid_set:
                    for c in self.monoid_set:
                        if self.operation(self.operation(a, b), c) != self.operation(a, self.operation(b, c)):
                            raise TypeError(f"Associativity is not satisfied")


    def operate(self,*args):
        if not args:
            return self.identity

        for a in args:
            if a not in self.monoid_set:
                raise ValueError(f"{a} is not in the set")

        result = args[0]
        for a in args[1:]:
            result = self.operation(result, a)
        return result

    def powers_of_element(self,a,exp):
        if a not in self.monoid_set:
            raise ValueError(f"{a} is not in the set")

        if exp < 0:
            raise ValueError(f"{exp} must be nonnegative")

        result = self.identity
        for _ in range(exp):
            result = self.operation(result,a)

        return result

    def is_generator(self,element):
        if element not in self.monoid_set:
            raise TypeError(f"{element} is not in the set")


        return self.generated_submonoid(element) == set(self.monoid_set)

    def generated_submonoid(self, a):
        if a not in self.monoid_set:
            raise ValueError(f"{a} is not in the set")
        generated = {self.identity}
        result = self.identity

        while True:
            result = self.operation(result, a)

            if result in generated:
                break

            generated.add(result)

        return generated

    def commutes(self):
        for a in self.monoid_set:
            for b in self.monoid_set:
                if self.operation(a,b) != self.operation(b,a):
                    return False

        return True
