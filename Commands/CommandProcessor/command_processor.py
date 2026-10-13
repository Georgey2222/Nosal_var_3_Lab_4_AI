import time

class CommandProcessor:
    def __init__(self,game):
        self.__game=game
        self.__game.display()

    def execute(self,command):
        if not command:
            return True
        parts=command.split()
        name = parts[0].lower()

        match name:
            case "reset":
                return self.__reset(parts)
            case "clear":
                return self.__clear(parts)
            case "default":
                return self.__default(parts)
            case "set":
                return self.__set_random(parts)
            case "step":
                return self.__step(parts)
            case "back":
                return self.__back(parts)
            case "exit":
                return self.__exit(parts)
            case "set_pattern":
                return self.__set_pattern(parts)
            case _:
                print("Невідома команда")
                return True

    def __reset(self,parts):
        if len(parts)==1:
            self.__game.reset()
            self.__game.display()
            return True
        if len(parts)==2:
            try:
                size = int(parts[1])
                if size<1:
                    print("Розмір поля повинен бути натуральним числом, 1 <= N <= 256")
                    return True
                self.__game.reset_size(size)
                self.__game.display()

            except ValueError:
                print("Розмір роля повинен бути натуральним числом, 1 <= N <= 256")

            return True
        print("Некоректний запис reset [N]")
        return True

    def __clear(self,parts):
        if len(parts)!=1:
            print("Некоректний запис clear")
            return True
        self.__game.clear()
        self.__game.display()

        return True

    def __default(self,parts):
        if len(parts)!=1:
                print("Некоректний запис default")
                return True
        self.__game.default()
        self.__game.display()
        return True

    def __set_random(self,parts):
        if len(parts)!=2:
            print("Некоректний запис set N")
            return True

        try:
            n = int(parts[1])
            self.__game.set_random(n)
            self.__game.display()
        except ValueError:
            print("N повинно бути цілим числом в межах 0 <= N <= size^2")
        return True

    def __step(self,parts):
        if len(parts)==1:
            self.__game.step()
            self.__game.display()
            return True

        if parts[1]=="-d":
            return self.__step_animation(parts)

        if len(parts)==2:
            try:
                n = int(parts[1])
                self.__game.step(n)
                self.__game.display()
            except ValueError:
                print("N має бути натуральним числом")

            return True

        print("Некоректний запис step [n]")
        return True

    def __step_animation(self,parts):
        if len(parts)<3 or len(parts)>4:
            print("Некоректний запис step -d [N] [delay]")
            return True

        try:
            n = int(parts[2])
            if n<1:
                print("N повинно бути натуральним числом")
                return True
            delay = 0.3
            if len(parts)==4:
                delay = float(parts[3])

                if delay<0:
                    print("Затримка не може бути менша за 0")
                    return True
            try:
                print("\033[s", end="")
                for _ in range(n):
                    self.__game.step(1)
                    self.__game.display(_+1)
                    time.sleep(delay)
                    print(f"\033[{self.__game.get_size()+5}A")
                self.__game.display(n)
            except KeyboardInterrupt:
                print("\033[u",end="")
        except ValueError:
            print("N та Delay повинні бути числами")

        return True

    def __back(self,parts):
        if len(parts)==1:
            self.__game.back()
            self.__game.display()
            return True

        if parts[1]=="-d":
            return self.__back_animation(parts)

        if len(parts)==2:
            try:
                n = int(parts[1])
                self.__game.back(n)
                self.__game.display()

            except ValueError:
                print("N повинно бути натуральним числом")

            return True
        print("Некоректний запис back [N]")
        return True


    def __back_animation(self,parts):
        if len(parts)<3 or len(parts)>4:
            print("Некоректний запис back -d [N] [delay]")
            return True

        try:
            n = int(parts[2])
            if n<1:
                print("N повинно бути натуральним числом")
                return True
            n = min(n,self.__game.get_steps())
            delay = 0.3
            if len(parts)==4:
                delay = float(parts[3])

                if delay<0:
                    print("Затримка не може бути менша за 0")
                    return True

            try:
                print("\033[s", end="")
                for _ in range(n):
                    self.__game.back(1)
                    self.__game.display(n-(_+1))
                    time.sleep(delay)
                    print(f"\033[{self.__game.get_size()+5}A")
                self.__game.display(0)
            except KeyboardInterrupt:
                print("\033[u",end="")

        except ValueError:
            print("N та Delay повинні бути числами")

        return True

    def __exit(self,parts):
        if len(parts)!=1:
            print("Некоректний запис exit")
            return True

        return False

    def __set_pattern(self, parts):
        if len(parts) not in [2,3]:
            print("Некоректний запис set_pattern")
            return True
        try:
            n,m = int(parts[1]),int(parts[1])
            if len(parts)==3:
                m = int(parts[2])

            if n>self.__game.get_size() or m>self.__game.get_size() or n<1 or m<1:
                print("Розміри паттерну повинні бути натуральними та не більшими за розмір поля")
                return True
            patterns = []
            for i in range(n):
                temp = list(map(int,list(input())))

                if len(temp)<m:
                    temp+=[0]*(m-len(temp))

                if len(temp)>m:
                    print("Розмір рядка не повинен перевищувати m")
                    return True
                patterns.append(temp.copy())

            self.__game.set_pattern(patterns)
            self.__game.display()
            return True

        except ValueError:
            print("n та m повинні бути натуральними числами")
            return True
            