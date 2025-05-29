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

