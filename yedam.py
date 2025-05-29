import random

# Animal 클래스: 동물의 기본 속성(좌표, 나이)과 이동 기능을 담당
class Animal:
    def __init__(self, x, y):
        # 동물의 초기 위치와 나이 설정
        self.x = x
        self.y = y
        self.age = 0

    def increment_age(self):
        # 동물의 나이를 1 증가
        self.age += 1

    def move(self):
        # 동물이 상하좌우 중 한 칸 무작위로 이동
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        dx, dy = random.choice(directions)
        new_x = self.x + dx
        new_y = self.y + dy
        # 이동 위치가 0~49 범위 내에 있으면 이동
        if 0 <= new_x < 50:
            self.x = new_x
        if 0 <= new_y < 50:
            self.y = new_y

# Zebra 클래스: Animal을 상속받아 얼룩말 특유의 번식 기능 추가
class Zebra(Animal):
    def can_reproduce(self):
        # 얼룩말이 3살 이상이면 번식 가능
        return self.age >= 3

# Lion 클래스: Animal을 상속받아 사자 특유의 사냥, 굶주림, 번식 기능 추가
class Lion(Animal):
    def __init__(self, x, y):
        # 사자는 초기에 굶주림 상태(hunger)가 0
        super().__init__(x, y)
        self.hunger = 0

    def can_reproduce(self):
        # 사자가 5살 이상이면 번식 가능
        return self.age >= 5

    def is_starving(self):
        # 사자가 5년 동안 못 먹으면 굶어 죽음
        return self.hunger >= 5

# Ecosystem 클래스: 전체 생태계(50x50)와 동물 배치, 시뮬레이션 관리
class Ecosystem:
    def __init__(self):
        self.size = 50
        self.zebras = []
        self.lions = []
        self.place_animals()

    def print_map(self):
        grid = [['.' for _ in range(self.size)] for _ in range(self.size)]
        for zebra in self.zebras:
            grid[zebra.y][zebra.x] = 'Z'
        for lion in self.lions:
            if grid[lion.y][lion.x] == 'Z':
                grid[lion.y][lion.x] = 'X'  # 사자와 얼룩말이 겹친 경우 표시
            else:
                grid[lion.y][lion.x] = 'L'
        for row in grid:
            print(''.join(row))
        print()  # 줄 바꿈

    def simulate_year(self):
        # 기존 simulate_year() 내용 그대로
        ...
        return len(self.zebras), len(self.lions)

    # place_animals: 20마리 얼룩말과 5마리 사자를 무작위로 배치
    def place_animals(self):
        positions = set()  # 위치 중복 방지용
        # 얼룩말 20마리 배치
        while len(self.zebras) < 20:
            x, y = random.randint(0, 49), random.randint(0, 49)
            if (x, y) not in positions:
                self.zebras.append(Zebra(x, y))
                positions.add((x, y))
        # 사자 5마리 배치
        while len(self.lions) < 5:
            x, y = random.randint(0, 49), random.randint(0, 49)
            if (x, y) not in positions:
                self.lions.append(Lion(x, y))
                positions.add((x, y))

    # simulate_year: 1년 동안 생태계의 변화를 시뮬레이션
    def simulate_year(self):
        # 모든 얼룩말 이동
        for zebra in self.zebras:
            zebra.move()
        # 모든 사자 이동
        for lion in self.lions:
            lion.move()

        # 사자 사냥 시도
        for lion in self.lions:
            hunted = False
            for zebra in self.zebras:
                # 사자와 얼룩말이 바로 옆칸(상하좌우)에 있으면 사냥
                if abs(lion.x - zebra.x) + abs(lion.y - zebra.y) == 1:
                    self.zebras.remove(zebra)
                    lion.hunger = 0  # 사냥 성공 시 굶주림 초기화
                    hunted = True
                    break
            # 사냥 실패 시 굶주림 증가
            if not hunted:
                lion.hunger += 1

        # 모든 동물 나이 증가
        for zebra in self.zebras:
            zebra.increment_age()
        for lion in self.lions:
            lion.increment_age()

        # 굶어 죽은 사자 제거
        self.lions = [lion for lion in self.lions if not lion.is_starving()]

        # 얼룩말 번식
        new_zebras = []
        for zebra in self.zebras:
            if zebra.can_reproduce():
                # 상하좌우 중 빈 칸에 새끼 생성
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = zebra.x + dx, zebra.y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        if not any(z.x == nx and z.y == ny for z in self.zebras) and not any(l.x == nx and l.y == ny for l in self.lions):
                            new_zebras.append(Zebra(nx, ny))
                            break

        # 사자 번식
        new_lions = []
        for lion in self.lions:
            if lion.can_reproduce():
                # 상하좌우 중 빈 칸에 새끼 생성
                for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nx, ny = lion.x + dx, lion.y + dy
                    if 0 <= nx < 50 and 0 <= ny < 50:
                        if not any(z.x == nx and z.y == ny for z in self.zebras) and not any(l.x == nx and l.y == ny for l in self.lions):
                            new_lions.append(Lion(nx, ny))
                            break

        # 새로 태어난 얼룩말과 사자 추가
        self.zebras.extend(new_zebras)
        self.lions.extend(new_lions)

        # 현재 얼룩말과 사자 수 반환
        return len(self.zebras), len(self.lions)

# 실행 예시
ecosystem = Ecosystem()
for year in range(1, 6):
    zebras, lions = ecosystem.simulate_year()
    print(f"—— {year}년차 ——")
    print(f"얼룩말 수: {zebras}, 사자 수: {lions}")
    ecosystem.print_map()