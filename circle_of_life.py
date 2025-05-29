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
    
    def move(self, zebras):
        """주변에 얼룩말이 있는지 확인 (상하좌우)"""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            for zebra in zebras:
                if zebra.x == new_x and zebra.y == new_y:
                    """얼룩말이 바로 옆에 있으면 그 방향으로 이동 (사냥이므로 이동하지 않고 사냥 처리)"""
                    self.x = new_x
                    self.y = new_y
                    return
        """주변에 얼룩말이 없으면 무작위 이동"""
        super().move()
