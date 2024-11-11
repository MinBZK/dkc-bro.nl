import timeit
from pathlib import Path
from statistics import mean

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.cpt_rules.CPT0002 import CPT0002
from app.expert.rules.cpt_rules.CPT0002B import CPT0002B
from app.expert.rules.cpt_rules.CPT0004 import CPT0004
from app.expert.rules.cpt_rules.CPT0004B import CPT0004B


def CPT2_CPT4_parser():
    document_path = Path(__file__).parent / "CPT1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    return parser


def performance_parser_CPT2(parser: object):
    rule_CPT0002 = CPT0002()
    rule_CPT0002.applyRule(parser)


def performance_parser_CPT2B(parser: object):
    rule_CPT0002B = CPT0002B()
    rule_CPT0002B.applyRule(parser)


def performance_parser_CPT4(parser: object):
    rule_CPT0004 = CPT0004()
    rule_CPT0004.applyRule(parser)


def performance_parser_CPT4B(parser: object):
    rule_CPT0004B = CPT0004B()
    rule_CPT0004B.applyRule(parser)


if __name__ == "__main__":
    print(
        mean(
            timeit.repeat(
                setup="from __main__ import CPT2_CPT4_parser, performance_parser_CPT2B",
                stmt="performance_parser_CPT2B(CPT2_CPT4_parser())",
                repeat=100,
                number=1,
            )
        )
        - mean(
            timeit.repeat(
                setup="from __main__ import CPT2_CPT4_parser, performance_parser_CPT2",
                stmt="performance_parser_CPT2(CPT2_CPT4_parser())",
                repeat=100,
                number=1,
            )
        )
    )

    print(
        mean(
            timeit.repeat(
                setup="from __main__ import CPT2_CPT4_parser, performance_parser_CPT4B",
                stmt="performance_parser_CPT4B(CPT2_CPT4_parser())",
                repeat=100,
                number=1,
            )
        )
        - mean(
            timeit.repeat(
                setup="from __main__ import CPT2_CPT4_parser, performance_parser_CPT4",
                stmt="performance_parser_CPT4(CPT2_CPT4_parser())",
                repeat=100,
                number=1,
            )
        )
    )
