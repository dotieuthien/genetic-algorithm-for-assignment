import numpy as np

# cid, basic, no_of_c
courses_catalog_cases = [
    #1 classes == teachers
    np.array([
        ['C01', 1, 3],
        ['C02', 0, 2],
        ['C03', 1, 2],
        ['C04', 0, 4],
    ]),
    #2 classes < teachers
    np.array([
        ['C01', 1, 3],
        ['C02', 0, 2],
        ['C03', 1, 2],
        ['C04', 0, 4],
    ]),
    #3 classes > teachers
    np.array([
        ['C01', 1, 3],
        ['C02', 0, 2],
        ['C03', 1, 2],
        ['C04', 0, 4],
        ['C05', 1, 4],
    ]),
    #4 classes = teachers
    np.array([
        ['C01', 1, 3],
        ['C02', 0, 2],
        ['C03', 1, 2],
        ['C04', 0, 4],
        ['C05', 1, 3],
    ]),
    #5 classes > teachers
    np.array([
        ['C01', 1, 0],
        ['C02', 1, 0],
        ['C03', 1, 1],
        ['C04', 1, 2],
        ['C05', 1, 3],
        ['C06', 0, 2],
        ['C07', 0, 1],
        ['C08', 0, 0],
        ['C09', 0, 0],
        ['C10', 0, 0],
    ]),
    #6 basic but no one prefer
    np.array([
        ['C01', 1, 0],
        ['C02', 1, 0],
        ['C03', 1, 1],
        ['C04', 1, 2],
        ['C05', 1, 3],
        ['C06', 0, 2],
        ['C07', 0, 1],
        ['C08', 0, 0],
        ['C09', 0, 0],
        ['C10', 0, 0],
    ]),
    #7 final test
    np.array([
        ['C01', 1, 2],
        ['C02', 1, 2],
        ['C03', 1, 2],
        ['C04', 1, 1],
        ['C05', 1, 3],
        ['C06', 1, 2],
        ['C07', 1, 1],
        ['C08', 1, 4],
        ['C09', 1, 1],
        ['C10', 1, 3],
        ['C11', 1, 4],
        ['C12', 1, 2],
        ['C13', 0, 2],
        ['C14', 0, 2],
        ['C15', 0, 2],
        ['C16', 0, 2],
        ['C17', 0, 2],
        ['C18', 0, 2],
        ['C19', 0, 2],
        ['C20', 0, 2],
    ])
]

# tid, mc
teachers_catalog_cases = [
    #1 classes == teachers
    np.array([
        ['T01', 3],
        ['T02', 2],
        ['T03', 2],
        ['T04', 3],
        ['T05', 1],
    ]),
    # classes < teachers
    np.array([
        ['T01', 3],
        ['T02', 2],
        ['T03', 2],
        ['T04', 3],
        ['T05', 1],
        ['T06', 3],
    ]),
    # classes > teachers
    np.array([
        ['T01', 3],
        ['T02', 2],
        ['T03', 2],
        ['T04', 3],
        ['T05', 1],
        ['T06', 1],
    ]),
    #4 classes = teachers
    np.array([
        ['T01', 3],
        ['T02', 2],
        ['T03', 2],
        ['T04', 3],
        ['T05', 1],
        ['T06', 3],
    ]),
    #5 classes > teachers
    np.array([
        ['T01', 2],
        ['T02', 3],
        ['T03', 2],
        ['T04', 0],
        ['T05', 1],
    ]),
    #6 basic but no one prefer
    np.array([
        ['T01', 2],
        ['T02', 3],
        ['T03', 2],
        ['T04', 0],
        ['T05', 1],
    ]),
    #7 final test
    np.array([
        ['T01', 2],
        ['T02', 3],
        ['T03', 3],
        ['T04', 4],
        ['T05', 2],
        ['T06', 4],
        ['T07', 6],
        ['T08', 6],
        ['T09', 6],
        ['T10', 6],
        ['T11', 6],
        ['T12', 6],
    ])
]

# cid_index, [priority_of_tid_index]
courses_teachers_priorities_cases = [
    #1 classes = teachers
    np.array([
        [1, 3, 1, 0, 2],
        [2, 2, 2, 3, 3],
        [3, 1, 3, 2, 0],
        [4, 0, 0, 1, 1],
    ]),
    #2 classes < teachers
    np.array([
        [1, 3, 1, 0, 2, 1],
        [2, 2, 2, 3, 3, 0],
        [3, 1, 3, 2, 0, 0],
        [4, 0, 0, 1, 1, 0],
    ]),
    #3 classes > teachers
    np.array([
        [1, 3, 1, 0, 2, 1],
        [2, 2, 2, 3, 3, 0],
        [3, 1, 3, 2, 0, 0],
        [4, 0, 0, 1, 1, 0],
        [0, 4, 0, 4, 0, 2],
    ]),
    #4 classes = teachers
    np.array([
        [1, 3, 1, 0, 2, 1],
        [2, 2, 2, 3, 3, 0],
        [3, 1, 4, 2, 0, 0],
        [4, 0, 0, 1, 1, 0],
        [0, 0, 3, 1, 4, 2],
    ]),
    #5 classes > teachers
    np.array([
        [1, 0, 0, 0, 3],
        [2, 0, 0, 0, 4],
        [3, 1, 0, 0, 0],
        [4, 2, 0, 0, 0],
        [0, 3, 1, 0, 0],
        [0, 4, 2, 0, 0],
        [0, 0, 3, 1, 0],
        [0, 0, 4, 2, 0],
        [0, 0, 0, 3, 1],
        [0, 0, 0, 4, 2],
    ]),
    #6 basic but no one prefer
    np.array([
        [1, 0, 0, 0, 3],
        [2, 0, 0, 0, 4],
        [3, 1, 0, 0, 0],
        [4, 2, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 4, 2, 0, 0],
        [0, 0, 3, 1, 0],
        [0, 0, 4, 2, 0],
        [0, 0, 0, 3, 1],
        [0, 0, 0, 4, 2],
    ]),
    #7 final test
    np.array([
        [1, 0, 0, 0, 3, 2, 0, 0, 0, 2, 4, 5],
        [2, 0, 0, 0, 4, 3, 0, 0, 0, 3, 0, 0],
        [3, 1, 0, 0, 0, 1, 5, 0, 0, 1, 1, 0],
        [4, 2, 0, 0, 0, 4, 6, 0, 0, 4, 2, 0],
        [0, 3, 1, 0, 0, 0, 7, 8, 0, 0, 7, 9],
        [0, 4, 2, 0, 0, 0, 8, 7, 0, 0, 8, 8],
        [0, 0, 3, 1, 0, 0, 0, 6, 5, 0, 0, 7],
        [0, 0, 4, 2, 0, 0, 0, 5, 6, 0, 3, 6],
        [0, 0, 0, 3, 1, 0, 0, 0, 4, 0, 0, 0],
        [5, 0, 0, 0, 5, 7, 0, 0, 0, 9, 0, 0],
        [6, 0, 0, 0, 6, 8, 0, 0, 0, 8, 0, 0],
        [7, 0, 0, 0, 0, 9, 1, 0, 0, 10, 10, 0],
        [8, 0, 0, 0, 0, 10, 2, 0, 0, 11, 9, 0],
        [0, 0, 5, 0, 0, 0, 3, 1, 0, 0, 6, 1],
        [0, 0, 6, 0, 0, 0, 4, 2, 0, 0, 5, 2],
        [0, 0, 7, 4, 0, 0, 0, 3, 3, 7, 0, 3],
        [0, 0, 8, 5, 0, 0, 0, 4, 2, 0, 0, 4],
        [0, 0, 0, 6, 2, 0, 0, 0, 1, 0, 0, 0],
        [9, 0, 0, 0, 7, 5, 0, 0, 0, 5, 0, 0],
        [10, 0, 0, 0, 8, 6, 0, 0, 0, 6, 0, 0],
    ])
]


def select_case_data(case_i):
    return courses_catalog_cases[case_i], teachers_catalog_cases[case_i], courses_teachers_priorities_cases[case_i]


def case_info(courses_catalog, teachers_catalog, courses_teachers_priorities):
    total_course_instances = np.sum(courses_catalog[:, 2].astype(int))
    print(f'total_course_instances={total_course_instances}')

    total_teacher_instances = np.sum(teachers_catalog[:, 1].astype(int))
    print(f'total_teacher_instances={total_teacher_instances}')

    assigned_matrix = courses_teachers_priorities[courses_teachers_priorities != 0]
    ub_cost = np.max(assigned_matrix, axis=0)*total_course_instances
    lb_cost = np.min(assigned_matrix, axis=0)*total_course_instances
    print(f'UB_cost={ub_cost}, LB_cost={lb_cost}')
    return total_course_instances, total_teacher_instances, ub_cost, lb_cost, np.max(courses_teachers_priorities)
