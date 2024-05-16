import random

target_word = "МИР"

population_size = 10

mutation_rate = 0.1

def generate_random_word(length):
    return ''.join(random.choice('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ') for _ in range(length))

def fitness(word):
    target_codes = [ord(char) for char in target_word] 
    word_codes = [ord(char) for char in word]
    return sum((target - actual) ** 2 for target, actual in zip(target_codes, word_codes))


def tournament_selection(population, scores, k=2):
    selected = []
    for _ in range(len(population)):
        participants = random.sample(list(zip(population, scores)), k)
        selected.append(min(participants, key=lambda x: x[1])[0])
    return selected

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(word):
    index = random.randint(0, len(word) - 1)
    mutated_char = random.choice('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')
    return word[:index] + mutated_char + word[index + 1:]

population = [generate_random_word(len(target_word)) for _ in range(population_size)]

generations = 0
while True:
    scores = [fitness(word) for word in population]
    
    if 0 in scores:
        index = scores.index(0)
        print("Целевое слово найдено:", population[index])
        break
    
    selected_parents = tournament_selection(population, scores)
    
    children = []
    for i in range(0, len(selected_parents), 2):
        child1, child2 = crossover(selected_parents[i], selected_parents[i + 1])
        children.extend([child1, child2])
    
    mutated_children = [mutate(child) if random.random() < mutation_rate else child for child in children]
    
    population = mutated_children
    
    generations += 1

    if generations % 10 == 0:
        print(f"Поколение {generations}: лучшая особь - {population[scores.index(min(scores))]}, расстояние - {min(scores)}")
