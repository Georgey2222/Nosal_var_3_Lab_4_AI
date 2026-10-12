import random

class Board:
    offsets = ((0,1),(1,0),(1,1),(1,-1),(-1,1),(-1,-1),(0,-1),(-1,0))

    patterns = ((5,15),(5,16),(5,17),(5,21),(5,22),(5,23),(7,13),(7,18),(7,20),(7,25),(7,79),(8,13),(8,18),
                (8,20),(8,25),(8,79),(8,81),(9,13),(9,18),(9,20),(9,25),(9,82),(9,83),(10,15),(10,16),(10,17),
                (10,21),(10,22),(10,23),(10,68),(10,69),(10,82),(10,83),(10,88),(10,89),(11,68),(11,69),
                (11,82),(11,83),(11,88),(11,89),(12,15),(12,16),(12,17),(12,21),(12,22),(12,23),(12,79),
                (12,81),(13,13),(13,18),(13,20),(13,25),(13,79),(14,13),(14,18),(14,20),(14,25),(15,13),
                (15,18),(15,20),(15,25),(17,15),(17,16),(17,17),(17,21),(17,22),(17,23),(17,61),(18,62),
                (19,60),(19,61),(19,62),(23,69),(24,70),(25,68),(25,69),(25,70),(35,54),(35,55),(35,56),
                (35,57),(35,58),(35,59),(36,53),(36,60),(37,52),(37,61),(38,53),(38,60),(39,54),(39,55),
                (39,56),(39,57),(39,58),(39,59),(46,31),(46,32),(46,33),(47,32),(47,33),(47,34),(58,25),
                (59,5),(59,25),(59,26),(59,27),(60,4),(60,7),(60,28),(61,7),(61,27),(61,29),(62,4),(62,7),
                (62,28),(63,5),(63,6),(63,7),(65,29),(65,30),(66,29),(66,30),(73,67),(73,68),(73,69),(74,67),
                (74,68),(74,69),(75,67),(75,68),(75,69),(76,70),(76,71),(76,72),(77,70),(77,71),(77,72),
                (78,70),(78,71),(78,72),(81,5),(82,4),(82,7),(83,7),(84,4),(84,7),(85,5),(85,6),(85,7),
                (88,69),(88,70),(89,62),(89,64),(89,65),(89,69),(89,70),(89,71),(90,58),(90,61),(90,65),
                (90,71),(90,72),(90,74),(91,57),(91,58),(91,61),(91,66),(91,71),(91,74),(91,80),(91,81),
                (92,56),(92,57),(92,63),(92,64),(92,65),(92,66),(92,71),(92,72),(92,74),(92,80),(92,81),
                (93,46),(93,47),(93,55),(93,56),(93,57),(93,65),(93,69),(93,70),(93,71),(94,46),(94,47),
                (94,56),(94,57),(94,69),(94,70),(95,57),(95,58),(96,58))

    def __init__(self,size):
        self.reset_size(size)

    def default(self):
        self.reset_size(100)
        for i,j in self.patterns:
            self.__field[i][j]=1
                
    def set_pattern(self,pattern):
        pattern_rows=len(pattern)
        if pattern_rows==0:
            raise ValueError("Паттерн не повинен бути порожнім")
        pattern_columns=max(map(len,pattern))
        for x in pattern:
            for y in x:
                if y not in [0,1]:
                    raise ValueError("Паттерн повинен містити лише 0 та 1")
        if pattern_rows>self.__size or pattern_columns>self.__size:
            raise ValueError("Розмірність паттерну не повинна перевищувати розмірність поля")

        for i in range(len(self.__field)):
            for j in range(len(self.__field[i])):
                self.__field[i][j]=0

        start_row = (self.__size - pattern_rows)//2
        start_column = (self.__size - pattern_columns)//2
        for i in range(pattern_rows):
            for j, x in enumerate(pattern[i]):
                self.__field[start_row+i][start_column+j] = x
        
    def clear(self):
        for i in range(len(self.__field)):
            for j in range(len(self.__field)):
                self.__field[i][j] = 0

    def reset_size(self,size):
        if size<1 or size>256:
            raise ValueError("N повинно бути натуральним числом та не перевищувати 256")
        self.__size=size
        self.__field=[[0 for _ in range(size)] for _ in range(size)]

    def set_random(self,n):
        if n<0 or n>self.__size**2:
            raise ValueError("N бути натуральним числом та не перевищувати size^2")
        self.clear()
        cells = [(i,j) for i in range(self.__size) for j in range(self.__size)]
        random.shuffle(cells)
        for i,j in cells[:n]:
            self.__field[i][j] = 1

    def set_field(self,field):
        if field==[]:
            raise ValueError("Некоректний розмір матриці")
        rows = len(field)
        columns = len(field[0])
        if rows!=columns:
            raise ValueError("Некоректний розмір матриці")
        for x in field:
            if len(x)!=columns:
                raise ValueError("Некоректний розмір матриці")

        for x in field:
            for y in x:
                if y not in [0,1]:
                    raise ValueError("Паттерн повинен містити лише 0 та 1")

        self.__field=[row.copy() for row in field]
        self.__size=len(field)

    def __count_live_neighbors(self,field,i,j):
        count = 0

        for di,dj in self.offsets:
            ni=(i+di)%self.__size
            nj=(j+dj)%self.__size
            count+=field[ni][nj]
        return count

    def next_generation(self):
        old_field = [row.copy() for row in self.__field]
        for i in range(self.__size):
            for j in range(self.__size):
                neighbors=self.__count_live_neighbors(old_field,i,j)
                if old_field[i][j]==0:
                    if neighbors==3:
                        self.__field[i][j]=1
                else:
                    if neighbors not in [2,3]:
                        self.__field[i][j]=0

    def get_state(self):
        return [row.copy() for row in self.__field]
    
    def get_size(self):
        return self.__size