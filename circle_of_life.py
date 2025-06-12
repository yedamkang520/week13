import random

class Animal:
    def __init__(self,x,y):
        """동물 초기 위치와 나이 설정"""
        self.x = x
        self.y = y
        self.age = 0
    
    def increment_age(self):
        """동물 나이 1년씩 증가"""
        self.age += 1

    def move(self):
        """동물의 동서남북 중 한 칸 무작위 이동"""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        dx, dy = random.choice(directions)
        new_x = self.x + dx
        new_y = self.y + dy
        """범위 내에서 이동"""
        if 0 <= new_x < 50:
            self.x = new_x
        if 0 <= new_y < 50:
            self.y = new_y

class Zebra(Animal):
    """3년후 번식 가능"""
    def reproduce(self):
        return self.age >= 3

class Lion(Animal):
    def __init__(self, x, y):
        """사자는 초기에 굶주림 (hunger = 0)"""
        super().__init(x,y)
        self.hunger = 0

    def can_reproduce(self):
        """사자가 5살 이상이면 번식 가능"""
        return self.age >= 5
    
    def is_starving(self):
        """사자가 5년 동안 못 먹으면 굶어 죽음"""
        return self.hunger >= 5    

class Ecosystem:
    """전체 생태계(50x50)와 동물 배치, 시뮬레이션 관리"""
    def __init__(self):
        self.size = 50
        self.zebras = []
        self.lions = []
        self.timestep = 0  
        self.place_animals()

    def print_map(self):
        print(f'Clock: {getattr(self, "timestep", 0)}')  

        top_coord_str = ' '.join([f'{coord}' for coord in range(self.size)])
        print('   ' + top_coord_str)

        grid = [['.' for _ in range(self.size)] for _ in range(self.size)]

        for zebra in self.zebras:
            "얼룩말 위치 표시"
            grid[zebra.y][zebra.x] = 'Z'
        for lion in self.lions:
            "사자 위치 표시"
            if grid[lion.y][lion.x] == 'Z':
                grid[lion.y][lion.x] = 'X'
            else:
                grid[lion.y][lion.x] = 'L'

        for row, line in enumerate(grid):
            print(f'{row:2} ' + ' '.join(line))

        key = input('enter [q] to quit:')
        if key == 'q':
            exit()