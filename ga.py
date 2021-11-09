import numpy as np

from data import case_info, select_case_data

TEST_CASE = 6  # 1-based indexing
courses_catalog, teachers_catalog, courses_teachers_priorities = select_case_data(
    TEST_CASE-1)
case_info(courses_catalog, teachers_catalog, courses_teachers_priorities)

teachers = {k: int(v) for k, v in teachers_catalog}
classes = {k: int(v) for k, _, v in courses_catalog}
basic = [b for _, b, _ in courses_catalog]
priority_matrix = courses_teachers_priorities


def create_binary_solution(size):
    gen = np.zeros((size, size))
    index1 = np.arange(size)
    index2 = np.arange(size)
    np.random.shuffle(index2)

    for i in range(size):
        gen[index1[i], index2[i]] = 1

    return index2


def cal_fitness(gen, cost_matrix):
    fitness = 0
    for i in range(cost_matrix.shape[0]):
        j = gen[i]
        fitness += cost_matrix[i, j]
    return fitness


def create_population(max_pop, cost_matrix):
    size, _ = cost_matrix.shape
    populasi = []
    fitness = []

    for i in range(max_pop):
        gen = create_binary_solution(size)
        gen_fitness = cal_fitness(gen, cost_matrix)

        populasi.append(gen)
        fitness.append(gen_fitness)

    return populasi, fitness


def selection(populasi, fitness):
    parent = []
    parent_fitness = []

    # # Get 2 min fitness
    # arg_min_fitness = np.argmin(fitness)
    # parent.append(populasi[arg_min_fitness])
    # parent_fitness.append(fitness[arg_min_fitness])

    # min_value = np.inf
    # top_2_id =  None

    # for i in range(len(fitness)):
    #     if i == arg_min_fitness:
    #         continue

    #     if fitness[i] < min_value:
    #         min_value = fitness[i]
    #         top_2_id = i
    # parent.append(populasi[top_2_id])
    # parent_fitness.append(min_value)

    # Random pick
    parent_index = np.arange(len(fitness))
    np.random.shuffle(parent_index)

    for i in parent_index[:2]:
        parent.append(populasi[i])
        parent_fitness.append(fitness[i])

    return parent, parent_fitness


def crossover(parent, cost_matrix):
    child = []
    child_fitness = []

    dad = parent[0]
    mom = parent[1]

    child1 = []
    index = list(np.arange(cost_matrix.shape[0]))
    miss_index = []
    for i in range(cost_matrix.shape[0]):
        if i % 2 == 0:
            if dad[i] not in child1:
                child1.append(dad[i])
                index.remove(dad[i])
            else:
                child1.append(np.inf)
                miss_index.append(i)
        else:
            if mom[i] not in child1:
                child1.append(mom[i])
                index.remove(mom[i])
            else:
                child1.append(np.inf)
                miss_index.append(i)

    for i, idx in enumerate(miss_index):
        child1[idx] = index[i]
    mutation_idx = np.random.randint(0, 8, size=[2])
    new_child1 = child1.copy()
    new_child1[mutation_idx[0]] = child1[mutation_idx[1]]
    new_child1[mutation_idx[1]] = child1[mutation_idx[0]]

    fitness1 = cal_fitness(new_child1, cost_matrix)

    dad = parent[1]
    mom = parent[0]

    child2 = []
    index = list(np.arange(cost_matrix.shape[0]))
    miss_index = []
    for i in range(cost_matrix.shape[0]):
        if i % 2 == 0:
            if dad[i] not in child2:
                child2.append(dad[i])
                index.remove(dad[i])
            else:
                child2.append(np.inf)
                miss_index.append(i)
        else:
            if mom[i] not in child2:
                child2.append(mom[i])
                index.remove(mom[i])
            else:
                child2.append(np.inf)
                miss_index.append(i)

    for i, idx in enumerate(miss_index):
        child2[idx] = index[i]
    mutation_idx = np.random.randint(0, 8, size=[2])
    new_child2 = child2.copy()
    new_child2[mutation_idx[0]] = child2[mutation_idx[1]]
    new_child2[mutation_idx[1]] = child2[mutation_idx[0]]

    fitness2 = cal_fitness(new_child2, cost_matrix)

    child.append(new_child1)
    child.append(new_child2)
    child_fitness.append(fitness1)
    child_fitness.append(fitness2)

    return child, child_fitness


def mutation(child, cost_matrix, mutation_rate):
    mutant = []
    mutant_fitness = []

    for i in range(len(child)):
        data = child[i]

        for j in range(len(data)):
            for k in range(len(data)):
                if np.random.rand(1) <= mutation_rate:
                    data[j, k] = 1

        fitness = cal_fitness(data, cost_matrix)
        mutant.append(data)
        mutant_fitness.append(fitness)

    return mutant, mutant_fitness


def bestfitness(parent_fitness):
    fitness = min(parent_fitness)

    return fitness


def regeneration(mutant, mutant_fitness, populasi, fitness):
    for i in range(len(mutant)):
        bad_gen = np.argmax(fitness)
        populasi.pop(bad_gen)
        fitness.pop(bad_gen)

    for i in range(len(mutant)):
        populasi.append(mutant[i])
        fitness.append(mutant_fitness[i])

    return populasi, fitness


if __name__ == '__main__':
    num_teachers = 0
    teachers_list = []
    teachers_id_list = []

    for idx, (k, v) in enumerate(teachers.items()):
        num_teachers += v
        teachers_list.extend([k] * v)
        teachers_id_list.extend([idx] * v)

    num_classes = 0
    classes_list = []
    classes_id_list = []

    for idx, (k, v) in enumerate(classes.items()):
        num_classes += v
        classes_list.extend([k] * v)
        classes_id_list.extend([idx] * v)

    print('Number classes and teachers :', num_classes, num_teachers)
    print(classes_list)
    print(classes_id_list)
    print(teachers_list)
    print(teachers_id_list)

    cost_matrix = np.zeros((num_classes, num_teachers))

    for c in range(num_classes):
        for t in range(num_teachers):
            c_id = classes_id_list[c]
            t_id = teachers_id_list[t]
            cost_matrix[c, t] = priority_matrix[c_id, t_id]

    if num_teachers > num_classes:
        # Make sure each class is assigned with a teacher
        pass
    elif num_teachers < num_classes:
        # Make sure each teacher has a class
        # Add dummy teachers
        num_dummy_teacher = num_classes - num_teachers
        dummy_cols = np.zeros((num_classes, num_dummy_teacher))
        # Add cols in cost matrix
        new_cost_matrix = np.concatenate((cost_matrix, dummy_cols), axis=1)

        rs, cs = np.where(new_cost_matrix == 0)
        new_cost_matrix[rs, cs] = 100

        populasi, fitness = create_population(20, new_cost_matrix)
        parent, parent_fitness = selection(populasi, fitness)

        while True:
            child, child_fitness = crossover(parent, new_cost_matrix)
            if bestfitness(parent_fitness) <= bestfitness(child_fitness):
                continue

            populasi, fitness = regeneration(
                child, child_fitness, populasi, fitness)
            parent, parent_fitness = selection(populasi, fitness)

            if bestfitness(child_fitness) <= 300:
                min_idx = np.argmin(child_fitness)
                final_child = child[min_idx]

                for c_id, t_id in enumerate(final_child):
                    try:
                        class_name = classes_list[c_id]
                        teacher_name = teachers_list[t_id]
                        print(class_name, teacher_name,
                              new_cost_matrix[c_id, t_id])
                    except:
                        print('Matching with dummy node ', 100)
                        continue
                break
