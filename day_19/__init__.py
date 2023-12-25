import dataclasses
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

from typing import Optional, List, Dict

"""
--- Day 19: Aplenty ---

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny

Then, each part is sent through a series of workflows that will ultimately accept or reject the part.
Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part
if the condition is true. The first rule that matches the part being considered is applied immediately,
and the part moves on to the destination described by the rule.
(The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules.
If workflow ex were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).

If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns.
If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort
a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}

The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort.
All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A

Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts
gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127.
Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers
for all of the parts that ultimately get accepted?

--- Part Two ---

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000.
Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant.
How many distinct combinations of ratings will be accepted by the Elves' workflows?
"""

APPROVED = "A"
REJECTED = "R"


def get_lines(fname="input.txt"):
    with open(os.path.join(__location__, fname)) as f:
        for line in f.readlines():
            yield line.strip()


def parse_lines(fname="input.txt"):
    rules_map = {}
    parts = []
    in_rules_section = True
    for line in get_lines(fname):
        if not line:
            in_rules_section = False
            continue
        if in_rules_section:
            name, conditions = parse_rule(line)
            rules_map[name] = conditions
        else:
            parts.append(Part.from_line(line))

    return rules_map, parts


def parse_rule(line):
    # ex{x>10:one,m<20:two,a>30:R,A}
    name, conditions_str = line[:-1].split("{")
    conditions = conditions_str.split(",")
    return name, [Condition.from_str(condition) for condition in conditions]


def evaluate_rule(rule: List["Condition"], part):
    for condition in rule:
        result = condition.evaluate(part)
        if result:
            return result
    return condition.result


def get_result_for_part(part, rules_map: Dict[str, List["Condition"]], rule_name="in"):
    rule = rules_map[rule_name]
    result = evaluate_rule(rule, part)
    if result in (APPROVED, REJECTED):
        return result
    else:
        return get_result_for_part(part, rules_map, result)


@dataclasses.dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def __hash__(self):
        return hash((self.x, self.m, self.a, self.s))

    @classmethod
    def from_line(cls, line: str) -> "Part":
        x, m, a, s = line[1:-1].split(",")
        return cls(
            int(x.split("=")[1]),
            int(m.split("=")[1]),
            int(a.split("=")[1]),
            int(s.split("=")[1]),
        )

    @property
    def total_rating(self):
        return self.x + self.m + self.a + self.s


@dataclasses.dataclass(frozen=True)
class Condition:
    result: str
    field: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[int] = None

    def __hash__(self):
        return hash((self.field, self.operator, self.value))

    @classmethod
    def from_str(cls, condition_str: str) -> "Condition":
        # a<2006:qkq
        if ":" in condition_str:
            field_operator_value, result = condition_str.split(":")
            if "<" in field_operator_value:
                field, value = field_operator_value.split("<")
                operator = "<"
            elif ">" in field_operator_value:
                field, value = field_operator_value.split(">")
                operator = ">"
            return cls(result, field, operator, int(value))
        return cls(condition_str)

    def evaluate(self, part) -> Optional[str]:
        if self.field:
            if self.operator == "<":
                if getattr(part, self.field) < self.value:
                    return self.result
            elif self.operator == ">":
                if getattr(part, self.field) > self.value:
                    return self.result
            return None
        return self.result
