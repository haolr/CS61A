from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.

def do_define_form(expressions, env):
    """Evaluate a define form.
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2
        # BEGIN PROBLEM 4
        #计算表达式  （不确定是否要rest.first）
        value = scheme_eval(expressions.rest.first,env)
        #创建当前的环境帧 ？ 绑定值
        env.define(signature,value)
        
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g.   这个是lambda的简化形式
        # (define (f x y)<- 这个是signature (+ x y))<- 这个是expressions 
        # BEGIN PROBLEM 10
        "*** YOUR CODE HERE ***"
        func_name = signature.first  #取出函数f 
        formals = signature.rest  #取出 形式参数 比如（X Y）
        body = expressions  #函数式
        lambda_proc = do_lambda_form(expressions,env)  #创建一个lambda 对象
        env.define(func_name,lambda_proc)
        return func_name
        
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """Evaluate a quote form.

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    return expressions.first
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """Evaluate a begin form.

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):#把一个expressions 拆成 lambda 
    """Evaluate a lambda form.

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)#检查两个部分
    formals = expressions.first
    validate_formals(formals)#检查合法性
    # BEGIN PROBLEM 7
    body = expressions.rest
    return LambdaProcedure(formals, body, env)#这是一个lambdaprodure对象 存 函数名 和 形参
    # END PROBLEM 7

def do_if_form(expressions, env):
    """Evaluate an if form. 

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    # if 1评估条件 2 eval 正确条件并return
    
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating (and #f (print 1))
    False
    >>> # evaluating (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12

    if expressions is nil:  # 没有表达式，and 返回 True
        return True

    result = None
    while expressions is not nil:
        expr = expressions.first
        result = scheme_eval(expr, env)  # 逐个求值
        if is_scheme_false(result):      # 一旦遇到 False，立即返回
            return result
        expressions = expressions.rest
    return result  # 全为真，返回最后一个值


    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating (or #f 2 3 #t #f)
    2
    >>> # evaluating (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    if expressions is nil:  # 没有表达式，or 返回 False
        return False

    result = None
    while expressions is not nil:
        expr = expressions.first
        result = scheme_eval(expr, env)  # 逐个求值
        if is_scheme_true(result):       # 一旦遇到真，立即返回
            return result
        expressions = expressions.rest
    return result  # 全为假，返回最后一个（False）
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else': #如果是else子句，直接为真
            test = True
            if expressions.rest != nil:#但是else只能是最后一个子句
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env) #评估谓语表达式
            
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if clause.rest is nil:        # 子句没有结果表达式
                return test               # 返回谓词本身的值
            else:
                return eval_all(clause.rest, env)  # 有结果表达式就全评估并返回最后一个
            # END PROBLEM 13
        expressions = expressions.rest

def do_let_form(expressions, env):
    """Evaluate a let form.

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression."""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    symbols = []  # 用于最后检查重复名

    pointer = bindings  # 临时变量用于遍历绑定列表
    while pointer is not nil:
        bind = pointer.first  # 每个 bind 是一个 Pair，形如 (symbol expr)
        validate_form(bind, 2, 2)  # 必须恰好有两个元素：一个 symbol，一个表达式

        symbol = bind.first
        expr = bind.rest.first

        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol in let binding')

        val = scheme_eval(expr, env)  # 在“外部环境”求值
        names = Pair(symbol, names)
        vals = Pair(val, vals)
        symbols.append(symbol)

        pointer = pointer.rest

    validate_formals(scheme_list(*symbols))  # 检查变量名是否唯一
    # END PROBLEM 14
    return env.make_child_frame(names, vals)



def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV."""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV."""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################

def do_mu_form(expressions, env):
    """Evaluate a mu form."""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    body = expressions.rest
    return MuProcedure(formals,body)
    
    
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}