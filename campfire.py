#A very basic first interpreter for campfire language https://github.com/barbuz/campfire/

import sys
import re

class Stack:
    def __init__(self,other=None):
        self.values=list()
        self.other=other
    
    @property
    def tos(self):
        return 0 if len(self.values)==0 else self.values[-1]
    
    def push(self,val):
        self.values.append(val)
    
    def pop(self):
        val = 0 if len(self.values)==0 else self.values.pop()
        self.other.push(val)
        return val
    
    def swap(self):
        self.values.append(self.values.pop(-2))
    
    def clear(self):
        self.values=list()

def run(code,debug=False):
    stack=Stack()
    auxiliary=Stack(stack)
    stack.other=auxiliary
    position=0
    direction=1
    string_mode=False
    while True:
        instruction=code[position]
        if debug:
            print(instruction,stack.tos,position,direction)

        if instruction=='"':
            string_mode = not string_mode
        elif string_mode:
            stack.push(ord(instruction))
        elif instruction in '0123456789':
            stack.push(int(instruction))
        elif instruction in '-+*%><':
            b=str(stack.pop())
            a=str(stack.pop())
            stack.push(int(eval(a+instruction+b)))
        elif instruction=='/=':
            b=str(stack.pop())
            a=str(stack.pop())
            stack.push(int(eval(a+instruction*2+b)))
        elif instruction=='!':
            stack.push(int(not stack.pop()))
        elif instruction=='`':
            stack.push(-stack.pop())
        elif instruction=='~':
            char=sys.stdin.read(1)
            if len(char)==0:
                stack.push(0)
            else:
                stack.push(ord(char))
        elif instruction=='&':
            stack.push(int(input())) #TODO: fix
        elif instruction==',':
            print(chr(stack.pop()),end='')
        elif instruction=='.':
            print(stack.pop(),end=' ')
        elif instruction=='_':
            stack.pop()
        elif instruction=='^':
            auxiliary.pop()
        elif instruction=='$':
            stack.swap()
        elif instruction=='#':
            auxiliary.clear()
        else:
            pass
        
        occurrences = [match.start() for match in re.finditer(re.escape(instruction),code)]
        if len(occurrences)==1:
            return
        if stack.tos!=0:
            direction=-direction
        next_occurrence=occurrences[(occurrences.index(position)+direction)%len(occurrences)]
        position=(next_occurrence+direction)%len(code)

def main(args):
    with open(args[1],'r') as program:
        lines=program.readlines()
    code=""
    for line in lines:
        if line[0]!='#':
           code+=line.strip('\n') 
    run(code,len(args)>2)

if __name__ == '__main__':
    sys.exit(main(sys.argv))