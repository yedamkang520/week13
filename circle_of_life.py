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
        super().__init__(x,y)
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

    def place_animals(self):
        positions = set() 
        while len(self.zebras) < 20:
            """얼룩말 배치"""
            x, y = random.randint(0, 49), random.randint(0, 49)
            if (x, y) not in positions:
                self.zebras.append(Zebra(x, y))
                positions.add((x, y))

        while len(self.lions) < 5:
            """사자 배치"""
            x, y = random.randint(0, 49), random.randint(0, 49)
            if (x, y) not in positions:
                self.lions.append(Lion(x, y))
                positions.add((x, y))

    def simulate_year(self):
        "1년 동안 생태계의 변화를 시뮬레이션"
        for zebra in self.zebras:
            "모든 얼룩말 이동"
            zebra.move()
        for lion in self.lions:
            "모든 사자 이동"
            lion.move()

        for lion in self.lions:
            "사자 사냥 시도"
            hunted = False
            for zebra in self.zebras:
                "사자와 얼룩말이 바로 옆칸(상하좌우)에 있으면 사냥"
                if abs(lion.x - zebra.x) + abs(lion.y - zebra.y) == 1:
                    self.zebras.remove(zebra)
                    lion.hunger = 0  # 사냥 성공 시 굶주림 초기화
                    hunted = True
                    break
            # 사냥 실패 시 굶주림 증가
            if not hunted:
                lion.hunger += 1

        """나이 증가"""        
        for zebra in self.zebras:
            zebra.increment_age()
        for lion in self.lions:
            lion.increment_age()

        """죽은 사자 제거"""
        self.lions = [lion for lion in self.lions if not lion.is_starving()]

        new_zebras = []
        for zebra in self.zebras:
            if zebra.reproduce():
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = zebra.x + dx, zebra.y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        if not any(z.x == nx and z.y == ny for z in self.zebras) and not any(l.x == nx and l.y == ny for l in self.lions):
                            new_zebras.append(Zebra(nx, ny))
                            break

        new_lions = []
        for lion in self.lions:
            if lion.can_reproduce():
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = lion.x + dx, lion.y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        if not any(z.x == nx and z.y == ny for z in self.zebras) and not any(l.x == nx and l.y == ny for l in self.lions):
                            new_lions.append(Lion(nx, ny))
                            break

        "새로 태어난 얼룩말과 사자 추가"
        self.zebras.extend(new_zebras)
        self.lions.extend(new_lions)

        "시간 한 해 증가"
        self.timestep += 1

        "현재 얼룩말과 사자 수 반환"
        return len(self.zebras), len(self.lions)
    
ecosystem = Ecosystem()
for year in range(1, 6):
    zebras, lions = ecosystem.simulate_year()
    print(f"—— {year}년차 ——")
    print(f"얼룩말 수: {zebras}, 사자 수: {lions}")
    ecosystem.print_map()