import copy
from enum import IntEnum
from typing import List, Tuple, Dict

from .lex.token import Token
from .lex.scanner import Scanner
from .lex.token_type import TokenType


class Cat:
    """
    Category name, and list of
    acceptable overlapping categories
    """

    def __init__(
            self,
            cat_id: int,
            name: str,
            min_area: float,
            overlapping: Dict[int, int] = None,
            proportion: Dict[int, float] = None
    ):
        self.cat_id = cat_id
        self.name = name
        self.min_area = min_area
        self.overlapping = {} if overlapping is None else overlapping
        self.proportion = {} if proportion is None else proportion


class OverlapPosition(IntEnum):
    """
    Represents the position in an object where
    the bounding-boxes of two objects intersect
    """
    NONE = 0
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3


class Box:
    """
    Bounding-box size and position
    """

    def __init__(
            self,
            box: List[float],
            frame_height: int,
            frame_width: int,
            normalized: bool = True
    ):
        if normalized:
            self.min_x = int(box[1] * frame_width)
            self.min_y = int(box[0] * frame_height)
            self.max_x = int(box[3] * frame_width)
            self.max_y = int(box[2] * frame_height)
            self.norm_min_x = box[1]
            self.norm_min_y = box[0]
            self.norm_max_x = box[3]
            self.norm_max_y = box[2]
        else:
            self.min_x = int(box[1])
            self.min_y = int(box[0])
            self.max_x = int(box[3])
            self.max_y = int(box[2])
            self.norm_min_x = box[1] / frame_width
            self.norm_min_y = box[0] / frame_height
            self.norm_max_x = box[3] / frame_width
            self.norm_max_y = box[2] / frame_height

    def inside(self, b) -> float:
        """
        Determines which fraction of the area is inside Box b
        :param b: the other Box
        :return: float
        """
        # determine the (x, y)-coordinates of the intersection rectangle
        xa = max(self.norm_min_x, b.norm_min_x)
        ya = max(self.norm_min_y, b.norm_min_y)
        xb = min(self.norm_max_x, b.norm_max_x)
        yb = min(self.norm_max_y, b.norm_max_y)

        # compute the area of intersection rectangle
        inter_area = max(0.0, xb - xa) * max(0.0, yb - ya)

        inside = inter_area / self.norm_area()
        return inside

    # def area(self) -> int:
    #     return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)

    def norm_area(self) -> float:
        return (self.norm_max_x - self.norm_min_x) * (self.norm_max_y - self.norm_min_y)

    def child_position(self, child) -> OverlapPosition:
        height = self.max_y - self.min_y
        distance = child.min_y - self.min_y
        if distance < height / 3:
            position = OverlapPosition.TOP
        elif distance < 2 * height / 3:
            position = OverlapPosition.MIDDLE
        else:
            position = OverlapPosition.BOTTOM
        return position


class Target:
    """
    Represents the properties of an object
    observed by AND in an image
    The area, in pixels, of the object must
    be greater than the value specified for its Category
    """

    def __init__(
            self,
            target_id: int,  # target unique index within an image
            category_name: str,  # target category name
            class_id: int,  # target class number
            box: Box,  # bounding-box
            score: float,  # inference score
            parent_id: int = -1,  # overlapped target id
            overlaps: Dict[int, int] = None,  # dict of acceptable child count indexed by class
    ):
        self.id = target_id  # target unique id
        self.category_name: str = category_name  # target category name
        self.class_id: int = class_id  # target class number
        self.box = box  # target bounding-box
        self.score: float = score  # target score
        self.parent_id: int = parent_id  # parent must accept class_id as child

        self.overlaps: Dict[int, int] = {} if overlaps is None else overlaps


class Rule:
    """
    Represents criteria to determine if a certain combination
    of targets overlapping one other target is a non-compliance.
    Each rule has a name and is applied to the targets of a certain category.
    Special rules have name starting with '*', and are applied to
    combinations of targets of a certain category detected in an image.
    Each rule is expressed by a logical expression containing category names,
    integer values, comparison operators and logical operators.
    Comparison operators are used to indicate the required number of
    operators are used to connect the comparisons. Parentheses may
    be used to specify the order (priority) of calculations.

        exp -> exp OR trm | trm
        trm -> trm AND fat | fat
        fat -> NOT cmp | cmp | ( exp )
        cmp -> WORD opc INT
        opc -> < | <= | = | >= | >

    All rules are validated during setup
    """

    def __init__(
            self,
            name: str,  # rule name
            category_name: str,  # name of the category te rule applies to
            expression: str,  # logical expression
    ):
        self.name = name
        self.category_name = category_name
        self.scanner = Scanner(expression)
        self.tokens: List[Token] = self.scanner.tokenlist

    def __str__(self):
        print(f'Rule: {self.name} for {self.category_name}:')
        for tk in self.tokens:
            print(tk)


class NonCompliance:
    """
    Represents a a non_compliance
    detected by a rule
    """
    def __init__(
            self,
            rule: Rule,  # rule applied
            target: Target = None,  # target where alarm was detected
            categories: dict = None,  # category count on image
            reason: str = ''  # reason of rejection
    ):
        self.rule_name: str = rule.name
        self.category_name: str = rule.category_name
        self.target_id: int | None = None
        self.box: Box = Box([0, 0, 0, 0], 0, 0, True)
        self.detail: str = ''
        self.reason = reason

        if target is not None:
            self.target_id = target.id
            self.box = target.box
            out: str = f'    rule: {rule.name}\ncategory: {target.category_name}\n  target: {str(target.id)}'
            det = ''
            for item in target.overlaps.items():
                if item[1] != 0:
                    det += f' {cat_dict[item[0]]}={item[1]}'
            out += f'\nobserved: [ {det} ]'
            self.detail: str = out

        if categories is not None:
            det = ''
            for item in categories.items():
                if item[1] != 0:
                    det += f'{item[0]}={str(item[1])} '
            self.detail = f'\n    rule: {rule.name}\nobserved: [ {det} ]'


# cat_dict: Dict[int, Cat] = {}
cat_dict = {0: Cat(cat_id=0, min_area=0.0, name='eye-glass', overlapping={}, proportion={}),
            1: Cat(cat_id=1, min_area=0.0, name='face-shield', overlapping={}, proportion={}),
            2: Cat(cat_id=2, min_area=0.0, name='glove', overlapping={}, proportion={}),
            3: Cat(cat_id=3, min_area=0.0, name='helmet', overlapping={}, proportion={}),
            4: Cat(cat_id=4, min_area=0.0, name='mask', overlapping={}, proportion={}),
            5: Cat(cat_id=5, min_area=0.0090633, name='person',
                   overlapping={0: 1, 1: 1, 2: 0, 3: 1, 4: 1, 6: 3},
                   proportion={0: 0.008902, 1: 0.0365, 2: 0.034138, 3: 0.054, 4: 0.017134, 6: 0.031776}),
            6: Cat(cat_id=6, min_area=0.0, name='safety-shoe', overlapping={}, proportion={})
            }

rule_list = [
    Rule(name='Count_person', category_name=None,
         expression='person<=2'),
    Rule(name='Check_PPE', category_name='person',
         expression='helmet=1 and (safety-shoe=1 or safety-shoe=2) and \
         (glove=1 or glove=2) and (mask=1 or eye-glass=1 or face-shield=1)')
]


cat_id_by_name: Dict[str, int] = {}
for i in cat_dict.keys():
    cat_id_by_name[cat_dict[i].name] = i


class Alarm:
    """
    Decides whether an image contains
    one or more non-compliance
    """

    def __init__(self):
        self.targets: List[Target] = []  # targets detected everywhere

    # ----- PUBLIC METHODS -----
    def add_target(
            self,
            category_name: str,  # target category name
            class_id: int,  # target class number
            box: Box,  # target bounding-box
            score: float  # target score
    ) -> int:
        """
        Add a target to the image list of targets.
        The target width x height, in pixels, must be
        greater than the value defined for its Category
        Args:
            category_name: target category name
            class_id: target class number
            box: target bounding box
            score: target score
        Returns: an integer indicating the added target id
                 -1 if target is discarded
        """
        try:
            if class_id not in cat_dict.keys():
                return -1
            target_id = len(self.targets)
            target = Target(target_id=target_id,
                            category_name=category_name,
                            class_id=class_id,
                            box=box,
                            score=score)
            for item in cat_dict[class_id].overlapping:
                target.overlaps[item] = 0
            self.targets.append(target)
            return target_id
        except Exception as ex:
            raise Exception('(Alarm.add_target) ' + str(ex))

    def get_alarms(self) -> List[NonCompliance]:
        alarms: List[NonCompliance] = []
        try:
            _count_target_overlaps(self.targets)
            # Count targets on image
            image_categories_count: dict = {}
            for target in self.targets:
                if target.parent_id == -1:
                    if target.class_id not in image_categories_count.keys():
                        image_categories_count[target.class_id] = 1
                    else:
                        image_categories_count[target.class_id] += 1
            for rule in rule_list:
                # Check rules that apply to the image
                if rule.category_name is None:
                    alarms += _check_image_compliance(rule=rule,
                                                      category_count=image_categories_count)
                else:
                    # Check rules that apply to each target that may have overlaps
                    for target in self.targets:
                        if target.category_name == rule.category_name and \
                                len(target.overlaps) > 0:
                            alarms += _check_target_compliance(rule=rule, target=target)
        except Exception as ex:
            raise Exception('(Alarm.get_alarms) ' + str(ex))
        return alarms


def _evaluate(rule: List[Token]) -> Token:
    """
    exp -> trm OR trm | trm
    trm -> fat AND fat | fat
    fat -> NOT cmp | ( exp ) | cmp
    cmp -> WORD opc INT
    opc -> < | <= | = | >= | >
    """
    # Initialize evaluation process
    exp_value, rule = _exp(rule)
    if exp_value.token_type != TokenType.XVL:
        raise Exception('Alarm._evaluate - invalid rule expression')
    return exp_value


def _accept(rule: List[Token], token_type: TokenType) -> bool:
    return rule[0].token_type == token_type


def _expect(rule: List[Token], token_type: TokenType) -> bool:
    if _accept(rule, token_type):
        return True
    raise Exception('_evaluate - expect- unexpected token: ' + token_type.name)


def _expect_one_of(rule: List[Token], token_types: Tuple[TokenType]) -> bool:
    if rule[0].token_type in token_types:
        return True
    raise Exception('_evaluate- unexpected token')


def _exp(rule: List[Token]) -> (Token, List[Token]):
    val, rule = _trm(rule)
    while _accept(rule, TokenType.OR):
        rule = rule[1:]
        val2, rule = _trm(rule)
        val = _or(val, val2)
    return val, rule


def _trm(rule: List[Token]) -> (Token, List[Token]):
    val, rule = _fat(rule)
    while _accept(rule, TokenType.AND):
        rule = rule[1:]
        val2, rule = _fat(rule)
        val = _and(val, val2)
    return val, rule


def _fat(rule: List[Token]) -> (Token, List[Token]):
    inv = False
    if _accept(rule, TokenType.NOT):
        inv = True
        rule = rule[1:]
        while _accept(rule, TokenType.NOT):
            inv = not inv
            rule = rule[1:]
    if _accept(rule, TokenType.LPAR):
        rule = rule[1:]
        exp_val, rule = _exp(rule)
        if not _accept(rule, TokenType.RPAR):
            raise Exception('_evaluate - missing ) in rule expression')
        rule = rule[1:]
    else:
        exp_val, rule = _cmp(rule)
    if inv:
        exp_val.value = not exp_val.value
    return exp_val, rule


opcomp: tuple = (TokenType.LT,
                 TokenType.LE,
                 TokenType.EQ,
                 TokenType.GE,
                 TokenType.GT,
                 TokenType.NE)


def _cmp(rule: List[Token]) -> (Token, List[Rule]):
    if _expect(rule, TokenType.WORD):
        cat = rule[0].text
        obs_val = rule[0].value
        rule = rule[1:]
        if _expect_one_of(rule, opcomp):
            comp = rule[0].token_type
            rule = rule[1:]
        if _expect(rule, TokenType.INT):
            req_val = rule[0].value
            rule = rule[1:]
            res = _compare(required=req_val,
                           comparison=comp,
                           observed=obs_val)
            reason = _tell_reason(cat, _negate(comp), req_val) if not res else ''
            return Token(text=reason, token_type=TokenType.XVL, value=res), rule


def _compare(required: int, comparison: TokenType, observed: int) -> bool:
    req = int(required)
    obs = int(observed)
    if comparison == TokenType.LT:
        return obs < req
    elif comparison == TokenType.LE:
        return obs <= req
    elif comparison == TokenType.EQ:
        return obs == req
    elif comparison == TokenType.GE:
        return obs >= req
    elif comparison == TokenType.GT:
        return obs > req
    elif comparison == TokenType.NE:
        return obs != req
    else:
        return False


def _or(a: Token, b: Token) -> Token:
    if not a.value and not b.value:
        return Token(f'{a.text} and {b.text}', TokenType.XVL, False)

    return Token('', TokenType.XVL, True)


def _and(a: Token, b: Token):
    if a.value and b.value:
        return Token('', TokenType.XVL, True)
    if not a.value and not b.value:
        return Token(f'{a.text} and {b.text}', TokenType.XVL, False)
    if not a.value:
        return Token(a.text, TokenType.XVL, False)
    if not b.value:
        return Token(b.text, TokenType.XVL, False)


def _negate(token_type: TokenType) -> str:
    if token_type == TokenType.EQ:
        return '!='
    elif token_type == TokenType.GE:
        return '<'
    elif token_type == TokenType.GT:
        return '<='
    elif token_type == TokenType.LE:
        return '>'
    elif token_type == TokenType.LT:
        return '>='
    elif token_type == TokenType.NE:
        return '='
    else:
        return '?'


def _tell_reason(cat: str, comp: str, val: str):
    val = int(val)
    if val <= 1:
        return f'no {cat}'

    return f'{cat}{comp}{val}'


def _match_overlay_position(target: Target, child: Target) -> bool:
    """
    Determines if the child object inside position is in conformity
    """
    overlapping = cat_dict[target.class_id].overlapping
    position = overlapping.get(child.class_id)
    if position is None:
        return False
    if position == OverlapPosition.NONE:
        return True
    return position == target.box.child_position(child.box)


def _check_target_compliance(rule: Rule, target: Target) -> List[NonCompliance]:
    problems: List[NonCompliance] = []
    try:
        observed: List[Token] = copy.deepcopy(rule.tokens)
        # print_obs('_check_target_compliance', observed)
        i = 0
        while i < len(observed):
            if observed[i].token_type == TokenType.WORD:
                cat_id = cat_id_by_name[observed[i].text]
                observed[i].value = target.overlaps[cat_id]
                i += 3
            else:
                i += 1
        exp_value = _evaluate(observed)
        if not exp_value.value:
            problems.append(NonCompliance(rule=rule,
                                          target=target,
                                          reason=exp_value.text))
        return problems
    except Exception as ex:
        raise Exception('(Alarm._check_target_compliance) ' + str(ex))


def _check_image_compliance(rule: Rule, category_count: dict) -> List[NonCompliance]:
    problems: List[NonCompliance] = []
    try:
        observed: List[Token] = copy.deepcopy(rule.tokens)
        # print_obs('_check_image_compliance', observed)
        for i in range(len(observed)):
            if observed[i].token_type == TokenType.WORD:
                class_id = cat_id_by_name[observed[i].text]
                if class_id in category_count.keys():
                    observed[i].value = category_count[class_id]
        exp_value = _evaluate(observed)
        if not exp_value.value:
            problems.append(NonCompliance(rule=rule,
                                          categories=category_count,
                                          reason=exp_value.text))
        return problems
    except Exception as ex:
        raise Exception('(Alarm._check_image_compliance) ' + str(ex))


def _count_target_overlaps(targets: List[Target]) -> None:
    """
    Complete targets definitions counting allowed targets overlaps
    Returns:
    """
    try:
        ndx_tab = [[i, k] if i != k else None for i in range(len(targets)) for k in range(len(targets))]

        for row in ndx_tab:
            if row is None:
                continue
            i, k = row
            target_i, target_k = (targets[i], targets[k])
            if target_k.class_id not in target_i.overlaps.keys():
                continue
            if target_k.box.inside(target_i.box) < 0.9:
                continue
            if not _match_overlay_position(target_i, target_k):
                continue
            # Handle superposition of parent targets
            if target_k.parent_id != -1 and target_k.parent_id != i:
                # --------------------------------------------------------------------------------------------------------------------------------------
                k_area = target_k.box.norm_area()
                # --------------------------------------------------------------------------------------------------------------------------------------
                parent_area = targets[target_k.parent_id].box.norm_area()
                child_proportion: float = float(k_area) / float(parent_area)
                existing_diff = abs(child_proportion -
                                    cat_dict[targets[target_k.parent_id].class_id]
                                    .proportion[target_k.class_id])
                # --------------------------------------------------------------------------------------------------------------------------------------
                current_parent = target_i.box.norm_area()
                current_proportion: float = float(k_area) / float(current_parent)
                current_diff = abs(current_proportion -
                                   cat_dict[target_i.class_id]
                                   .proportion[target_k.class_id])
                # --------------------------------------------------------------------------------------------------------------------------------------
                if current_diff < existing_diff:
                    targets[target_k.parent_id].overlaps[target_k.class_id] -= 1
                # --------------------------------------------------------------------------------------------------------------------------------------
            target_i.overlaps[target_k.class_id] += 1
            target_k.parent_id = i

    except Exception as ex:
        raise Exception('(Alarm.count_overlaps) ' + str(ex))


def print_obs(where: str, obs: List[Token]):
    print(f'In {where}')
    for tk in obs:
        print(tk)
    print('End')
