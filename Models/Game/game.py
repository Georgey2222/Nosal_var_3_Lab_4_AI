import sys
from Models.Board.board import Board

class Game:
    def __init__(self,size):
        self.__board=Board(size)
        self.__history=[]
        self.__steps=0

    def get_steps(self):
        return self.__steps

    def __save_state(self):
        self.__steps+=1
        self.__history.append(self.__board.get_state())

    def reset(self):
        self.__board.clear()
        self.__history.clear()
        self.__steps = 0

    def reset_size(self, size):
        if not 1 <= size <= 256:
            raise ValueError("Розмір поля має бути в межах 1–256")
        self.__history.clear()
        self.__board.reset_size(size)

    def clear(self):
        self.__save_state()
        self.__board.clear()

    def default(self):
        self.__history.clear()
        self.__board.default()

    def set_pattern(self,patterns):
        self.__save_state()
        try:
            self.__board.set_pattern(patterns)
        except ValueError:
            self.__history.pop()
            self.__steps -= 1
            raise


    def set_random(self,n):
        if n<0 or n>self.__board.get_size()**2:
            raise ValueError("N повинно бути в межах 0 <= N <= size^2")
        self.__save_state()
        self.__board.set_random(n)

    def step(self, n=1):
        if n<1:
            raise ValueError("N аовинно бути натуральним числом")
        for _ in range(n):
            self.__save_state()
            self.__board.next_generation()

    def back(self, n=1):
        if n<1:
            raise ValueError("N повинно бути натуральним числом")
        n = min(n,self.__steps)

        for _ in range(n):
            self.__board.set_field(self.__history.pop())
            self.__steps -= 1

    def display(self,num=0):
        size = self.__board.get_size()
        output="\033[97m"+"---"*(size+3)+"\n"
        output+= f"\033[97m| {num%10000:4} |"
        for i in range(0,size):
            output+=f"{i:2X} "
        output+="|\n"+"---"*(size+3)+"\n"
        st = 1
        for row in self.__board.get_state():
            if st<=26:
                output+=f"\033[97m|    {chr(st+64)} |"
            else:
                output+=f"\033[97m|   {chr(st//26+64)}{chr(st%26+1+64)} |"
            for cell in row:
                if cell:
                    output+="\033[1;94m ● \033[0m"
                else:
                    output+="\033[90m - \033[0m"
            output+="\033[97m|\n"
            st+=1
        output+="---"*(self.__board.get_size()+3)+"\n"
        sys.stdout.write(output)

    def get_size(self):
        return self.__board.get_size()
