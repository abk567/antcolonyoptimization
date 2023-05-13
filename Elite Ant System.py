import numpy as np
import random
import math
from string import ascii_uppercase


# 货架坐标

# 参数设置
num_ants = 
alpha = 
beta = 
rho = 
max_iter = 
pheromone_add = 
elite_ratio = 

# 计算距离矩阵
num_shelves = len(shelves)
distances = np.zeros((num_shelves, num_shelves))
for i in range(num_shelves):
    for j in range(num_shelves):
        if i != j:
            distances[i, j] = math.sqrt((shelves[list(shelves.keys())[i]][0] - shelves[list(shelves.keys())[j]][0])**2 + (shelves[list(shelves.keys())[i]][1] - shelves[list(shelves.keys())[j]][1])**2)


# 初始化信息素矩阵
pheromones = np.ones((num_shelves, num_shelves))

# 初始化精英蚂蚁信息
elite_tour = []
elite_tour_length = float("inf")

# 蚁群算法
for _ in range(max_iter):
    tours = []
    tour_lengths = []

    # 每只蚂蚁寻找路径
    for _ in range(num_ants):
        tour = [random.randint(0, num_shelves - 1)]
        for _ in range(num_shelves - 1):
            current_shelf = tour[-1]
            remaining_shelves = [x for x in range(num_shelves) if x not in tour]
            probabilities = []

            for next_shelf in remaining_shelves:
                denom = sum([(pheromones[current_shelf, k] ** alpha) * ((1 / distances[current_shelf, k]) ** beta) for k in remaining_shelves])
                prob = (pheromones[current_shelf, next_shelf] ** alpha) * ((1 / distances[current_shelf, next_shelf]) ** beta) / denom
                probabilities.append(prob)

            tour.append(np.random.choice(remaining_shelves, 1, p=probabilities)[0])

        length = sum([distances[tour[i], tour[i+1]] for i in range(num_shelves - 1)]) + distances[tour[-1], tour[0]]
        tours.append(tour)
        tour_lengths.append(length)

        # 更新精英蚂蚁信息
        if length < elite_tour_length:
            elite_tour_length = length
            elite_tour = tour

    # 更新信息素
    pheromones *= (1 - rho)

    # 更新精英蚂蚁路径上的信息素
    for i in range(num_shelves - 1):
        pheromones[elite_tour[i], elite_tour[i + 1]] += elite_ratio * pheromone_add / elite_tour_length
    pheromones[elite_tour[-1], elite_tour[0]] += elite_ratio * pheromone_add / elite_tour_length

   