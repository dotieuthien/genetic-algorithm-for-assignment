import numpy as np
from scipy.optimize import linear_sum_assignment
from data import case_info, select_case_data

INF = 999
TEST_CASE = 5  # 1-based indexing
courses_catalog, teachers_catalog, courses_teachers_priorities = select_case_data(
    TEST_CASE-1)
case_info(courses_catalog, teachers_catalog, courses_teachers_priorities)

teachers = {k: int(v) for k, v in teachers_catalog}
classes = {k: int(v) for k, _, v in courses_catalog}
basic = [b for _, b, _ in courses_catalog]

print(teachers)
print(classes)
print(basic)

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

print(priority_matrix)


def solve():
    # setup inputs
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
    print("classes_list:", classes_list)
    print("classes_id_list:", classes_id_list)
    print("teachers_list:", teachers_list)
    print("teachers_id_list:", teachers_id_list)

    # build cost matrix
    cost_matrix = np.zeros((num_classes, num_teachers))
    for c in range(num_classes):
        for t in range(num_teachers):
            c_id = classes_id_list[c]
            t_id = teachers_id_list[t]
            cost_matrix[c, t] = priority_matrix[c_id, t_id]

    # pad the cost matrix
    if num_teachers > num_classes:
        # Make sure each class is assigned with a teacher
        num_dummy_class = num_teachers - num_classes
        dummy_rows = np.zeros((num_dummy_class, num_teachers))
        cost_matrix = np.concatenate((cost_matrix, dummy_rows), axis=0)
    elif num_teachers < num_classes:
        # None basic course

        # Make sure each teacher is assigned with maximum number of classes
        num_dummy_teacher = num_classes - num_teachers
        dummy_cols = np.zeros((num_classes, num_dummy_teacher))
        cost_matrix = np.concatenate((cost_matrix, dummy_cols), axis=1)

    # zero priority ~ INF cost
    rs, cs = np.where(cost_matrix == 0)
    cost_matrix[rs, cs] = INF

    # run assignment
    c_ids, t_ids = linear_sum_assignment(cost_matrix)
    print("c_ids:", c_ids)
    print("t_ids:", t_ids)

    # print result
    sum_priority = 0
    count_assign = 0
    pairs = np.vstack((c_ids, t_ids)).T
    for no, (c_id, t_id) in enumerate(pairs):
        priority = int(cost_matrix[c_id, t_id])
        class_name = 'n/a' if c_id >= len(
            classes_list) else classes_list[c_id]
        teacher_name = 'n/a' if t_id >= len(
            teachers_list) else teachers_list[t_id]
        if class_name != 'n/a' and teacher_name  != 'n/a':
            count_assign += 1
        if priority != INF:
            priority = priority if priority <= max_priority else priority - max_priority
            sum_priority += priority

        print('{}\t{}\t{}\t{}'.format(no + 1, class_name, teacher_name,
                                      int(priority) if priority != INF else 'n/a'))
    print("count_assign:", count_assign)
    print("sum_priority:", sum_priority)


solve()
