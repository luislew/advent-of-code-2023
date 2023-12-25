import dataclasses
from math import prod
from typing import Optional, Tuple

from day_19 import parse_lines, Condition, APPROVED, REJECTED


@dataclasses.dataclass()
class SolutionSpace:
    x: Tuple[int, int] = (1, 4000)
    m: Tuple[int, int] = (1, 4000)
    a: Tuple[int, int] = (1, 4000)
    s: Tuple[int, int] = (1, 4000)

    def __hash__(self):
        return hash(
            (
                self.x_min,
                self.x_max,
                self.m_min,
                self.m_max,
                self.a_min,
                self.a_max,
                self.s_min,
                self.s_max,
            )
        )

    def __str__(self):
        return f"x: {self.x_min}-{self.x_max}, m: {self.m_min}-{self.m_max}, a: {self.a_min}-{self.a_max}, s: {self.s_min}-{self.s_max}"

    def __repr__(self):
        return str(self)

    @property
    def x_min(self):
        return self.x[0]

    @property
    def x_max(self):
        return self.x[1]

    @property
    def m_min(self):
        return self.m[0]

    @property
    def m_max(self):
        return self.m[1]

    @property
    def a_min(self):
        return self.a[0]

    @property
    def a_max(self):
        return self.a[1]

    @property
    def s_min(self):
        return self.s[0]

    @property
    def s_max(self):
        return self.s[1]

    @property
    def combinations(self):
        return prod(
            (
                abs(self.x_max - self.x_min + 1),
                abs(self.m_max - self.m_min + 1),
                abs(self.a_max - self.a_min + 1),
                abs(self.s_max - self.s_min + 1),
            )
        )

    def apply(self, condition: Condition, invert=False):
        field = condition.field
        if not field:
            return dataclasses.replace(self)

        operator = condition.operator
        value = condition.value
        current_min, current_max = getattr(self, field)
        if invert:
            operator = "<" if operator == ">" else ">"
            value = value - 1 if operator == ">" else value + 1
        if operator == "<":
            current_min = min(value - 1, current_min)
            current_max = min(value - 1, current_max)
        elif operator == ">":
            current_min = max(value + 1, current_min)
            current_max = max(value + 1, current_max)

        return dataclasses.replace(self, **{field: (current_min, current_max)})


def find_all_approved_solution_spaces(
    rules_map,
    condition: Optional[Condition] = None,
    current_solution_space=None,
    solution_spaces=None,
):
    if solution_spaces is None:
        solution_spaces = []
    if current_solution_space is None:
        current_solution_space = SolutionSpace()

    if condition and condition.result == APPROVED:
        current_solution_space = current_solution_space.apply(condition)
        solution_spaces.append(current_solution_space)
        return
    elif condition and condition.result == REJECTED:
        return

    if condition:
        current_solution_space = current_solution_space.apply(condition)
        rule = rules_map[condition.result]
    else:
        rule = rules_map["in"]
    for condition in rule:
        find_all_approved_solution_spaces(
            rules_map, condition, current_solution_space, solution_spaces
        )
        if current_solution_space:
            current_solution_space = current_solution_space.apply(
                condition, invert=True
            )
    return list(set(solution_spaces))


if __name__ == "__main__":
    rules_map, _ = parse_lines()
    approved_solution_spaces = find_all_approved_solution_spaces(rules_map)
    print(
        sum(solution_space.combinations for solution_space in approved_solution_spaces)
    )
