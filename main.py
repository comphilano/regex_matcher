from NFA import *

def IsOperand(c):
    return c != ')' and c != '(' and c != '+' and c != '*' and c != '.'

def InsertConcatOperator(str):
    str = str.replace(' ', '')
    i = 1
    while i < len(str):
        if (str[i - 1] == ')' or str[i - 1] == '*' or IsOperand(str[i - 1])) and (str[i] == '(' or IsOperand(str[i])):
            str = str[:i] + '.' + str[i:]
        else:
            i += 1
    return str

def ToPostfix(infix):
    def LessOrEqualPriority(a, b):
        if b == '(':
            return False
        if a == '+':
            return True
        elif a == '.':
            return b == '*' or b == '.'
        else:
            return b == '*'
    stack = []
    postfix = ''
    for c in infix:
        if IsOperand(c):
            postfix += c
        else:
            if c == '(':
                stack.append(c)
            elif c == ')':
                operator = stack.pop()
                while operator != '(':
                    postfix += operator
                    operator = stack.pop()
            else:
                while (stack) and LessOrEqualPriority(c,stack[-1]):
                    postfix += stack.pop()
                stack.append(c)

    while (stack):
        postfix += stack.pop()
    return postfix

def ToNFA(Postfix):
    stack = []
    if Postfix:
        for token in Postfix:
            if token == '*':
                nfa = stack.pop()
                nfa.Closure()
                stack.append(nfa)
            elif token == '+':
                right = stack.pop()
                left = stack.pop()
                left.Union(right)
                stack.append(left)
            elif token == '.':
                right = stack.pop()
                left = stack.pop()
                left.Concat(right)
                stack.append(left)
            else:
                stack.append(NFA(token))
    else:
        stack.append(NFA(''))
    return stack.pop()

re = input("Input RE:")
new_re = InsertConcatOperator(re)
p = ToPostfix(new_re)
nfa = ToNFA(p)
s = input("Input string:")
print(nfa.Search(s))