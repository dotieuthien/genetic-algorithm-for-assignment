import numpy as np

from data import case_info, select_case_data
import time

start_time = time.time()
np.random.seed()

INF = 100
TEST_CASE = 1  # 1-based indexing
courses_catalog, teachers_catalog, courses_teachers_priorities = select_case_data(
    TEST_CASE-1)
case_info(courses_catalog, teachers_catalog, courses_teachers_priorities)

teachers = {k: int(v) for k, v in teachers_catalog}
classes = {k: int(v) for k, _, v in courses_catalog}
basic = [b for _, b, _ in courses_catalog]
basic_dict = {k: b for k, b, _ in courses_catalog}

max_priority = np.max(courses_teachers_priorities)
min_priority = np.min(courses_teachers_priorities)
priority_matrix = np.zeros(courses_teachers_priorities.shape)

for i, row in enumerate(courses_teachers_priorities):
    row = [x if x < INF else 0 for x in row]
    if basic[i] == '0':
        for j, cl in enumerate(row):
            if cl != 0:
                row[j] = row[j] + max_priority
    priority_matrix[i] = row

# priority_matrix = courses_teachers_priorities


def create_binary_solution(size, basic_id_list, dummy_id):
    gen = np.zeros((size, size))
    index1 = np.arange(size)
    index2 = np.arange(size)
    np.random.shuffle(index2)
    # check
    while True:
        teacher_id = index2[basic_id_list]
        len_inter = len(np.intersect1d(teacher_id, dummy_id))
        if len_inter != 0:
            np.random.shuffle(index2)
        else:
            break

    return index2


def cal_fitness(gen, cost_matrix):
    fitness = 0
    for i in range(cost_matrix.shape[0]):
        j = gen[i]
        fitness += cost_matrix[i, j]
    return fitness


def create_population(max_pop, cost_matrix, basic_id_list, dummy_id):
    size, _ = cost_matrix.shape
    populasi = []
    fitness = []

    for i in range(max_pop):
        gen = create_binary_solution(size, basic_id_list, dummy_id)
        gen_fitness = cal_fitness(gen, cost_matrix)

        populasi.append(gen)
        fitness.append(gen_fitness)

    return populasi, fitness


def selection(populasi, fitness):
    parent = []
    parent_fitness = []

    # Random pick
    parent_index = np.arange(len(fitness))
    np.random.shuffle(parent_index)

    for i in parent_index[:2]:
        parent.append(populasi[i])
        parent_fitness.append(fitness[i])

    return parent, parent_fitness


def crossover(parent, cost_matrix, basic_id_list, dummy_id):
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
        if idx in basic_id_list and index[i] in dummy_id:
            return None, None
        child1[idx] = index[i]

    mutation_idx = np.random.randint(0, cost_matrix.shape[0], size=[2])
    while True:
        len_inter_basic = len(np.intersect1d(basic_id_list, mutation_idx))
        mutation_value = [child1[i] for i in mutation_idx]
        len_inter_dummy = len(np.intersect1d(dummy_id, mutation_value))

        if len_inter_basic == 1 and len_inter_dummy == 1:
            mutation_idx = np.random.randint(0, cost_matrix.shape[0], size=[2])
        else:
            break

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
        if idx in basic_id_list and index[i] in dummy_id:
            return None, None
        child2[idx] = index[i]

    mutation_idx = np.random.randint(0, cost_matrix.shape[0], size=[2])
    while True:
        len_inter_basic = len(np.intersect1d(basic_id_list, mutation_idx))
        mutation_value = [child2[i] for i in mutation_idx]
        len_inter_dummy = len(np.intersect1d(dummy_id, mutation_value))

        if len_inter_basic == 1 and len_inter_dummy == 1:
            mutation_idx = np.random.randint(0, cost_matrix.shape[0], size=[2])
        else:
            break

    new_child2 = child2.copy()
    new_child2[mutation_idx[0]] = child2[mutation_idx[1]]
    new_child2[mutation_idx[1]] = child2[mutation_idx[0]]

    fitness2 = cal_fitness(new_child2, cost_matrix)

    child.append(new_child1)
    child.append(new_child2)
    child_fitness.append(fitness1)
    child_fitness.append(fitness2)
    
    return child, child_fitness


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


def ga():
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

    basic_id_list = []
    for i, c in enumerate(classes_list):
        if basic_dict[c] == '1':
            basic_id_list.append(i)
    print(basic_id_list)

    cost_matrix = np.zeros((num_classes, num_teachers))

    for c in range(num_classes):
        for t in range(num_teachers):
            c_id = classes_id_list[c]
            t_id = teachers_id_list[t]
            cost_matrix[c, t] = priority_matrix[c_id, t_id]

    if num_teachers >= num_classes:
        # Make sure each class is assigned with a teacher
        num_dummy_class = num_teachers - num_classes
        dummy_id = []
        dummy_rows = np.zeros((num_dummy_class, num_teachers))
        cost_matrix = np.concatenate((cost_matrix, dummy_rows), axis=0)

    elif num_teachers < num_classes:
        # Make sure each teacher has a class
        # Add dummy teachers
        num_dummy_teacher = num_classes - num_teachers
        dummy_id = np.arange(num_teachers, num_classes)
        dummy_cols = np.zeros((num_classes, num_dummy_teacher))
        # Add cols in cost matrix
        cost_matrix = np.concatenate((cost_matrix, dummy_cols), axis=1)

    rs, cs = np.where(cost_matrix == 0)
    cost_matrix[rs, cs] = INF

    populasi, fitness = create_population(
        50, cost_matrix, basic_id_list, dummy_id)
    parent, parent_fitness = selection(populasi, fitness)

    stop_child = 100
    min_child_fitness = np.inf

    while True:
        child, child_fitness = crossover(
            parent, cost_matrix, basic_id_list, dummy_id)
        if child is None:
            parent, parent_fitness = selection(populasi, fitness)
            continue

        if bestfitness(parent_fitness) < bestfitness(child_fitness):
            child = parent
            child_fitness = parent_fitness
            parent, parent_fitness = selection(populasi, fitness)
        else:
            populasi, fitness = regeneration(
                child, child_fitness, populasi, fitness)
            parent, parent_fitness = selection(populasi, fitness)

        print(bestfitness(child_fitness), min_child_fitness)

        if bestfitness(child_fitness) == min_child_fitness:
            min_child_fitness = bestfitness(child_fitness)

            if stop_child == 0:
                min_idx = np.argmin(child_fitness)
                final_child = child[min_idx]

                # print result
                sum_priority = 0
                count_assign = 0

                for c_id, t_id in enumerate(final_child):
                    priority = int(cost_matrix[c_id, t_id])
                    class_name = 'n/a' if c_id >= len(
                        classes_list) else classes_list[c_id]
                    teacher_name = 'n/a' if t_id >= len(
                        teachers_list) else teachers_list[t_id]
                    if class_name != 'n/a' and teacher_name != 'n/a':
                        count_assign += 1
                    if priority != INF:
                        priority = priority if priority <= max_priority else priority - max_priority
                        sum_priority += priority

                    print('{}\t{}\t{}\t{}'.format(c_id + 1, class_name, teacher_name,
                                                  int(priority) if priority != INF else 'n/a'))
                end_time = time.time()
                print("count_assign:", count_assign)
                print("sum_priority:", sum_priority)
                print("time(s):{:.3f}".format(end_time-start_time))
                break

            stop_child -= 1

        elif bestfitness(child_fitness) < min_child_fitness:
            min_child_fitness = bestfitness(child_fitness)

if __name__ == '__main__':
    ga()
