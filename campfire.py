#A very basic first interpreter for campfire language https://github.com/barbuz/campfire/

import sys
import re

class Stack:
    #A particular implementation of a stack, with implicit 0s at the bottom and a secondary stack to push popped values to
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
        second = 0 if len(self.values)<2 else self.values.pop(-2)
        self.values.append(second)
    
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
            stack.push(int(eval(a+instruction+b))) #easy and ugly
        elif instruction=='/=':
            b=str(stack.pop())
            a=str(stack.pop())
            stack.push(int(eval(a+instruction*2+b))) #easy and uglier
        elif instruction=='!':
            stack.push(int(not stack.pop()))
        elif instruction=='~':
            char=sys.stdin.read(1)
            if len(char)==0:
                stack.push(0)
            else:
                stack.push(ord(char))
        elif instruction=='&':
            stack.push(int(input())) #doesn't work properly, will be fixed (eventually)
        elif instruction==',':
            print(chr(stack.pop()),end='')
        elif instruction=='.':
            print(stack.pop(),end=' ') #are there better ideas than adding a space after every int?
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
        
        occurrences = [match.start() for match in re.finditer(re.escape(instruction),code)] #list of all positions of the current instruction
        if len(occurrences)==1:
            return
        if stack.tos!=0:
            direction=-direction
        next_occurrence=occurrences[(occurrences.index(position)+direction)%len(occurrences)] #next occurrence depends on direction, and wraps
        position=(next_occurrence+direction)%len(code) #the next instruction executed is the one after the next occurrence of the current instruction

def main(args):
    with open(args[1],'r') as program:
        lines=program.readlines()
    code=""
    for line in lines: #remove comments and newlines
        if line[0]!='#':
           code+=line.strip('\n') 
    run(code,len(args)>2) #any argument is --debug! (support for different arguments may come in the future)

if __name__ == '__main__':
    sys.exit(main(sys.argv))