#Jonathan Hein
#11532242
#HW5
#start: 11/24/18
#due: 11/28/18

import re


# /n 5 def
# /fact {
#     0 dict begin
#         /n exch def
#         n 2  lt
#         { 1}
#         {n 1  sub fact n mul stack}
#         ifeslse
#     end
# } def
# n fact stack

#------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
opstack = []

# now define functions to push and pop values to the top of to/from the top of
#the stack (end of the list). Recall that `pass` in Python is a space
#holder: replace it with your code.
def opPop():
    return opstack.pop()
def opPush(value):
    opstack.append(value)

# Remember that there is a Postscript operator called "pop" so we choose
#different names for these functions.

#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = [({},0)]

# now define functions to push and pop dictionaries on the dictstack, to define
#name, and to lookup a name
def dictPop():
    return dictstack.pop()
# dictPop pops the top dictionary from the dictionary stack.
def dictPush(d): #line36
    dictstack.append(d)
#should pop the empty dictionary from the opstack and push it onto the dictstack
#by calling dictPush. You may either pass this dictionary (which you popped from
#opstack) to dictPush as a parameter or just simply push a new empty dictionary
#in dictPush.
def define(name, value):
    dictstack[-1][0][name] = value

#name when you add it to the top dictionary) Your psDef function should pop the

def lookup(name):
    for item in reversed(dictstack):
        if "/"+name in item[0].keys():
            return item[0]["/"+name]
    return False
            
# return the value associated with name.
# What is your design decision about what to do when there is no definition for
# name? If name is not defined, your program should not break, but should
# give an appropriate error message.

#--------------------------- 15% -------------------------------------
# Arithmetic and comparison operators:
#define all the arithmetic and
#comparison operators here -- add, sub, mul, div, eq, lt, gt
def add():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    opPush(num1 + num2)
def sub():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    opPush(num1 - num2)
def mul():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    opPush(num1 * num2)
def div():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    if((isinstance(num1,int) or isinstance(num1,float)) and ((isinstance(num2,int) or isinstance(num2,float)) and num2!=0)):
        opPush(num1/float(num2))
    else:
        return ('ERROR: invalid operation')
def eq():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    if num1 == num2:
        opPush(True)
    else:
        opPush(False)
def lt():
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    if num1 < num2:
        opPush(True)
    else:
        opPush(False)
def gt(): 
    if len(opstack) < 2:
        return False
    num2 = opPop()
    num1 = opPop()
    if num1>num2:
        opPush(True)
    else:
        opPush(False)
#Make sure to check the operand stack has the correct number of parameters and
#types of the parameters are correct.44.

#--------------------------- 15% -------------------------------------
# Array operators: define the array operators length, get
def length():
    array = opPop()
    opPush(len(array))
def get():
    index = opPop()
    array = opPop()
    opPush(array[index])

#--------------------------- 15% -------------------------------------
# Boolean operators: define the boolean operators psAnd, psOr, psNot
#Remember that these take boolean operands only. Anything else is an error
def psAnd():
    if len(opstack) < 2:
        return False
    op2 = opPop()
    op1 = opPop()
    if op1 == True and op2 == True:
        opPush(True)
    else:
        opPush(False)
def psOr():
    if len(opstack) < 2:
        return False
    op2 = opPop()
    op1 = opPop()
    if op1 == True or op2 == True:
        opPush(True)
    else:
        opPush(False)
def psNot():
    op1 = opPop()
    if op1 == True:
        opPush(False)
    else:
        opPush(True)
#--------------------------- 25% -------------------------------------
# Define the stack manipulation and print operators:
#dup, exch, pop, copy,
#clear, stack
def dup():
    opPush(opstack[-1])
def exch():
    if len(opstack) < 2:
        return False
    op2 = opPop()
    op1 = opPop()
    opPush(op2)
    opPush(op1)
def pop():
    opPop()
def copy():
    numcopy = opPop()
    array = []
    if numcopy > len(opstack):
        return False
    else:
        for i in range(numcopy):
            array.append(opstack[len(opstack)-(i+1)])
        for var in array:
            opPush(var)
def clear():
    for i in range(len(opstack)):
        opPop()
#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in
#Python.
def psDict():
    op1 = opPop()
    opPush({})
def begin():
    op = opPop()
    if type(op) is dict:
        dictPush(op)
    else:
        return False
def end():
    dictPop()
def psDef():
    if len(opstack) < 2:
        return False
    else:
        val = opPop()
        name = opPop()

        define(name,val)

# Note: The psDef operator will pop the value and name from the opstack and
#call your own "define" operator (pass those values as parameters). Note that
#psDef()wn't have any parameters.
#------- Part 1 TEST CASES--------------
def testDefine():
    define("/n1", 4)
    if lookup("n1") != 4:
        return False
    return True

def testLookup():
    opPush("/n1")
    opPush(3)
    psDef()
    if lookup("n1") != 3:
        return False
    return True

#Arithmatic operator tests
def testAdd():
    opPush(1)
    opPush(2)
    add()
    if opPop() != 3:
        return False
    return True

def testSub():
    opPush(10)
    opPush(4.5)
    sub()
    if opPop() != 5.5:
        return False
    return True

def testMul():
    opPush(2)
    opPush(4.5)
    mul()
    if opPop() != 9:
        return False
    return True

def testDiv():
    opPush(10)
    opPush(4)
    div()
    if opPop() != 2.5:
        return False
    return True
    
#Comparison operators tests
def testEq():
    opPush(6)
    opPush(6)
    eq()
    if opPop() != True:
        return False
    return True

def testLt():
    opPush(3)
    opPush(6)
    lt()
    if opPop() != True:
        return False
    return True

def testGt():
    opPush(3)
    opPush(6)
    gt()
    if opPop() != False:
        return False
    return True

#boolean operator tests
def testPsAnd():
    opPush(True)
    opPush(False)
    psAnd()
    if opPop() != False:
        return False
    return True

def testPsOr():
    opPush(True)
    opPush(False)
    psOr()
    if opPop() != True:
        return False
    return True

def testPsNot():
    opPush(True)
    psNot()
    if opPop() != False:
        return False
    return True

#Array operator tests
def testLength():
    opPush([1,2,3,4,5])
    length()
    if opPop() != 5:
        return False
    return True

def testGet():
    opPush([1,2,3,4,5])
    opPush(4)
    get()
    if opPop() != 5:
        return False
    return True

#stack manipulation functions
def testDup():
    opPush(10)
    dup()
    if opPop()!=opPop():
        return False
    return True

def testExch():
    opPush(10)
    opPush("/x")
    exch()
    if opPop()!=10 and opPop()!="/x":
        return False
    return True

def testPop():
    l1 = len(opstack)
    opPush(10)
    pop()
    l2= len(opstack)
    if l1!=l2:
        return False
    return True

def testCopy():
    opPush(1)
    opPush(2)
    opPush(3)
    opPush(4)
    opPush(5)
    opPush(2)
    copy()
    if opPop()!=5 and opPop()!=4 and opPop()!=5 and opPop()!=4 and opPop()!=3 and opPop()!=2:
        return False
    return True

def testClear():
    opPush(10)
    opPush("/x")
    clear()
    if len(opstack)!=0:
        return False
    return True

#dictionary stack operators
def testDict():
    opPush(1)
    psDict()
    if opPop()!={}:
        return False
    return True

def testBeginEnd():
    opPush("/x")
    opPush(3)
    psDef()
    opPush({})
    begin()
    opPush("/x")
    opPush(4)
    psDef()
    end()
    if lookup("x")!=3:
        return False
    return True

def testpsDef():
    opPush("/x")
    opPush(10)
    psDef()
    if lookup("x")!=10:
        return False
    return True

def testpsDef2():
    opPush("/x")
    opPush(10)
    psDef()
    opPush(1)
    psDict()
    begin()
    if lookup("x")!=10:
        end()
        return False
    end()
    return True


# def main_part1():
#     testCases = [('define',testDefine),('lookup',testLookup),('add', testAdd), ('sub', testSub),('mul', testMul),('div', testDiv), \
#                  ('lt',testLt),('gt', testGt), ('psAnd', testPsAnd),('psOr', testPsOr),('psNot', testPsNot), \
#                  ('length', testLength),('get', testGet), ('dup', testDup), ('exch', testExch), ('pop', testPop), ('copy', testCopy), \
#                  ('clear', testClear), ('dict', testDict), ('begin', testBeginEnd), ('psDef', testpsDef), ('psDef2', testpsDef2)]
#     # add you test functions to this list along with suitable names
#     failedTests = [testName for (testName, testProc) in testCases if not testProc()]
#     if failedTests:
#         return ('Some tests failed', failedTests)
#     else:
#         return ('All part-1 tests OK')

# if __name__ == '__main__':
#     print(main_part1())

# clear()
# dictstack = [{}] #fix later =============================================================================
#----------------------------- Copied from given samplecode on blackboard -----------------------------
def tokenize(s):
    return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[[][a-zA-Z0-9_\s!][a-zA-Z0-9_\s!]*[]]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# The it argument is an iterator. The sequence of return characters should
# represent a string of properly nested {} parentheses pairs, from which
# the leasing '{' has been removed. If the parentheses are not properly
# nested, returns False.
def groupMatching(it):
    res = []
    for c in it:
        if c == '}':
            return res
        else:
            # Note how we use a recursive call to group the inner matching
            # parenthesis string and append it as a whole to the list we are
            # constructing. Also note how we have already seen the leading
            # '{' of this inner group and consumed it from the iterator.
            res.append(groupMatching(it))
    return False

# Function to parse a string of { and } braces. Properly nested parentheses
# are arranged into a list of properly nested lists.
def group(s):
    res = []
    it = iter(s)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false
            return False
        else:
            res.append(groupMatching(it))
    return res

#group("{{}{{}}}")


# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code array for the inner
            # paranthesis, it will be appended to the list we are constructing
            # as a whole.
            res.append(groupMatching2(it))
        else:
            res.append(c)
    return False


# RENAME THIS FUNCTION AS parse
# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.

def parsehelp(L): #turns code into a list of strings and nested lists
    res = []
    floatflag = False
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false since there is
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            res.append(groupMatching2(it))
        elif floatflag == True:
            left = res.pop()
            res.append(left+'.'+c)
            floatflag = False
        elif c=='.':
            floatflag = True
        else:
            res.append(c)
    return res
def parse(L):
    #Note: - Make sure that the integer/real constants are converted to Python integers/floats.
    #      - Make sure that the boolean constants are converted to Python booleans.
    #      - Make sure that the array constants are converted to Python lists.
    #      - Make sure that code arrays are represented as sublists.
    code = parsehelp(L)
    res = []
    for tok in code:
        if tok[0] == '[': #string of a list of integers
            intlist = re.findall("[\d]+",tok)
            intlist = map(int, intlist)
            res.append(intlist)
        elif isinstance(tok,list): #is list possibly nested so recursive call
                subres = []
                for x in tok:
                    if isinstance(x,list):
                        subres.append(parse(x))
                    else:
                        try:
                            subres.append(int(x))
                        except ValueError:
                            if x == 'true':
                                subres.append(True)
                            elif x == 'false':
                                subres.append(False)
                            else:
                                subres.append(x)
                res.append(subres)
        elif tok == 'true': #boolean true
            res.append(True)
        elif tok == 'false': #boolean false
            res.append(False)
        else: #integer or string
            try:
                res.append(int(tok)) #integer
            except  ValueError:
                try:
                    res.append(float(tok)) # float
                except ValueError:
                    res.append(tok) #string              
    return res


# Write the necessary code here; again write
# auxiliary functions if you need them. This will probably be the largest
# function of the whole project, but it will have a very regular and obvious
# structure if you've followed the plan of the assignment.
#
def interpretSPS(code,scope):
    fundict = {'def':psDef,'begin':begin,'end':end,'dict':psDict,'clear':clear,
    'copy':copy,'exch':exch,'dup':dup,'not':psNot,'or':psOr,'and':psAnd,'get':get,
    'length':length,'gt':gt,'lt':lt,'eq':eq,'div':div,'mul':mul,'sub':sub,'add':add,'if':psIf,
    'ifelse':psIfelse,'for':psFor,'forall':psForall,'pop':pop}
    if (isinstance(code, (int,float)) and not isinstance(code,bool)):
        opPush(code)
    else:
        for tok in code:
            if tok in fundict.keys():
                fundict[tok]()
            elif tok == 'stack':
                stack()
            else: 
                try: #if function call, push a new dictionary
                    token = lookup1(tok,scope)
                    if isinstance(token[0],list): #code block so new dict
                        dictstack.append(({},token[1]))
                        interpretSPS(token[0],scope)
                        dictstack.pop()
                    else:
                        interpretSPS(token[0],scope)

                except:
                    opPush(tok)
def lookup1(name,scope):
    if scope == "static":
        diclen = len(dictstack)-1
        if "/"+name in dictstack[diclen][0].keys():
            return (dictstack[diclen][0]["/"+name],diclen)
        elif "/"+name in dictstack[dictstack[diclen][1]][0].keys():
            return (dictstack[dictstack[diclen][1]][0]["/"+name],dictstack[diclen][1])
        return False
    else:
        for item in reversed(dictstack):
            if "/"+name in item[0].keys():
                return (item[0]["/"+name],item[1])
        return False
def psIf():
    op1 = opPop()
    op2 = opPop()
    if op2:
        interpretSPS(op1)
    else:
        pass
def psIfelse():
    op1 = opPop()
    op2 = opPop()
    op3 = opPop()
    if op3: #true
        interpretSPS(op2)
    else:
        interpretSPS(op1)
def psFor(): 
    op1 = opPop() #op
    op2 = int(opPop()) #final
    op3 = int(opPop()) #increment
    op4 = int(opPop()) #initial
    if op3 < 0:
        for x in range(op4,op2-1,op3): #since range does not include max, subtract 1 for neg increment
            opPush(x)
            interpretSPS(op1)
    else:
        for x in range(op4,op2+1,op3): #"...", add 1 for pos increment
            opPush(x)
            interpretSPS(op1) 
def psForall():
    op1 = opPop()
    op2 = opPop()
    for x in op2:
        opPush(x)
        interpretSPS(op1)
def stack():
    print("=======================")
    for op in reversed(opstack):
        print(op)
    print("=======================")
    diclength = len(dictstack)
    for dic in reversed(dictstack):
        diclength = diclength-1
        print("----"+str(diclength)+"----"+str(dic[1])+"----")
        for item in dic[0]:
            print(item+"    "+str(dic[0][str(item)]))
    print("=======================")

# Copy this to your HW4_part2.py file>
def interpreter(s,scope): # s is a string
    interpretSPS(parse(tokenize(s)),scope)




#testing

# input1 = """
# /m 50 def
# /n 100 def
# /egg1 {/m 25 def n} def
# /chic {
# /n 1 def
# /egg2 { n } def
# m n
# egg1
# egg2
# stack } def
# n
# chic
# """

# input2 = """
# /x 4 def
# /g { x stack } def
# /f { /x 7 def g } def
# f
# """

# input3 = """
# /x 10 def
# /A { x } def
# /C { /x 40 def A stack } def
# /B { /x 30 def /A { x } def C } def
# B
# """

# input4 = """
# /a 20 def
# /b { /d a def } def
# /c { /d 2 def 3 stack } def
# b
# c
# """
# input5 = """
# /d 32 def
# /b { d stack } def
# /e { /d 9 def b } def
# e
# """
# print("----------------------------test input 1----------------------------")
# print("STATIC")
# interpreter(input1,"static")
# print("DYNAMIC")
# interpreter(input1,"dynamic")
# opstack = [] # reset after each test
# dictstack = [({},0)] # reset after each test
# print("----------------------------test input 2----------------------------")
# print("STATIC")
# interpreter(input2,"static")
# print("DYNAMIC")
# interpreter(input2,"dynamic")
# opstack = [] # reset after each test
# dictstack = [({},0)] # reset after each test
# print("----------------------------test input 3----------------------------")
# print("STATIC")
# interpreter(input3,"static")
# print("DYNAMIC")
# interpreter(input3,"dynamic")
# opstack = [] # reset after each test
# dictstack = [({},0)] # reset after each test
# print("----------------------------test input 4----------------------------")
# print("STATIC")
# interpreter(input4,"static")
# print("DYNAMIC")
# interpreter(input4,"dynamic")
# opstack = [] # reset after each test
# dictstack = [({},0)] # reset after each test
# print("----------------------------test input 5----------------------------")
# print("STATIC")
# interpreter(input5,"static")
# print("DYNAMIC")
# interpreter(input5,"dynamic")
# opstack = [] # reset after each test
# dictstack = [({},0)] # reset after each test
def main_SSPS():
    # # ---------Test Case 1 (10pts)-------
    # print("\n---------Test Case 1 -------")
    # testcase1 = """
    # /x 4 def
    # /g { x stack } def
    # /f { /x 7 def g } def
    # f
    # """
    # print("Static")
    # interpreter(testcase1, "static")
    # opstack = []
    # dictstack = [({},0)]
    # print("Dynamic")
    # interpreter(testcase1, "dynamic")
    # opstack = []
    # dictstack = [({},0)]  # clear the stack for next test case

    # # ---------Test Case 2 (10pts) -------
    # print("\n---------Test Case 2 -------")
    # testcase2 = """
    # /out true def
    # /xand { out not exch not or stack} def
    # /put { out xand } def
    # /f { /out false def  put } def
    # f
    # """
    # print("Static")
    # interpreter(testcase2, "static")
    # opstack.clear()
    # dictstack.clear()
    # print("Dynamic")
    # interpreter(testcase2, "dynamic")
    # opstack.clear()
    # dictstack.clear()  # clear the stack for next test case

    # # ---------Test Case 3 (15pts) -------
    # print("\n---------Test Case 3 -------")
    # testcase3 = """
    # /m 50 def
    # /n 100 def
    # /egg1 {/m 25 def n} def
    # /chic
    # 	{/n 1 def
	#     /egg2 { n } def
	#     m  n
	#     egg1
	#     egg2
	#     stack} def
    # n
    # chic
    # """
    # print("Static")
    # interpreter(testcase3, "static")
    # opstack.clear()
    # dictstack.clear()
    # print("Dynamic")
    # interpreter(testcase3, "dynamic")
    # opstack.clear()
    # dictstack.clear()  # clear the stack for next test case

    # # ---------Test Case 4 (15pts)-------
    # print("\n---------Test Case 4 -------")
    # testcase4 = """
    # /x 1 def
    # /P1 {  x } def
    # /P2 { /x 2 def P1 } def
    # /P3 { /x 3 def /P1 { x } def P1 P2 stack} def
    # P3
    # """
    # print("Static")
    # interpreter(testcase4, "static")
    # opstack.clear()
    # dictstack.clear()
    # print("Dynamic")
    # interpreter(testcase4, "dynamic")
    # opstack.clear()
    # dictstack.clear()  # clear the stack for next test case

    # # ---------Test Case 5 (15pts)-------
    # print("\n---------Test Case 5 -------")
    # testcase5 = """
    # /a 50 def
    # /b 100 def
    # /F1 { /b 5 def a } def
    # /G
    #         { /a 1 def
    #           F1
    #          /F1 { a } def
    #          /F3 { /a 10 def F1 a stack } def
    #          a
    #          F3
    #          } def
    # G
    # """
    # print("Static")
    # interpreter(testcase5, "static")
    # opstack.clear()
    # dictstack.clear()
    # print("Dynamic")
    # interpreter(testcase5, "dynamic")
    # opstack.clear()
    # dictstack.clear()  # clear the stack for next test case

    # # ---------Test Case 6 (15pts)-------
    # print("\n---------Test Case 6 -------")
    # testcase6 = """
    # /x 10 def
    # /A { x } def
    # /C { /x 40 def A stack } def
    # /B { /x 30 def /A { x } def C } def
    # B
    # """
    # print("Static")
    # interpreter(testcase6, "static")
    # opstack.clear()
    # dictstack.clear()
    # print("Dynamic")
    # interpreter(testcase6, "dynamic")
    # opstack.clear()
    # dictstack.clear()  # clear the stack for next test case

    # ---------Test Case 7 (15pts)-------
    print("\n---------Test Case 7 -------")
    testcase7 = """
    /x 10 def
    /func3 {/func1 { x 2 stack } def /func4 {/x 50 def func1} def  func4}  def
    /func2 { /x 30 def func3} def
     func2

    """
    print("Static")
    interpreter(testcase7, "static")
    opstack = []
    dictstack = [({},0)]
    print("Dynamic")
    interpreter(testcase7, "dynamic")
    opstack = []
    dictstack = [({},0)]  # clear the stack for next test case


if __name__ == '__main__':
    main_SSPS()
#-------------------------------------------------------------------------------------------------------