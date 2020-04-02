import networkx as nx
import matplotlib.pyplot as plt
import netgraph

# Seleccionar los alumnos que completaron el major (realizar los cursos mínimos)


def students_selection(stgroups, courses, options=[]):
    students = []
    for student, group in stgroups:
        done = group["SIGLA"].tolist()
        valid = False
        if len(options) > 0:
            for course in options:
                if course in done:
                    done.remove(course)
                    valid = True
        else:
            valid = True
        if set(courses) == set(done) and valid:
            students.append(student)
    return students

# Calcular las relaciones entre los cursos


def relation(course1, course2, df):
    g = df.groupby(['ID'])
    concurrency = 0
    xor = 0
    succ_1 = 0
    succ_2 = 0
    succ = 0
    predecessor = 0
    length = 0
    for student, group in g:
        j = None
        a = group[group['SIGLA'] == course1]
        b = group[group['SIGLA'] == course2]
        if a.empty or b.empty:
            xor += 1
        else:
            a = a.iloc[0]['DURACIÓN']
            b = b.iloc[0]['DURACIÓN']
            if a == b:
                concurrency += 1
            elif a == b + 1:
                succ_1 += 1
            elif a == b + 2:
                succ_2 += 1
            elif a > b+2:
                succ += 1
            else:
                predecessor += 1
        length += 1
    return [concurrency/length, xor/length, succ_1/length, succ_2/length, succ/length, predecessor/length]

# Crea matriz con todos los cursos


def all_relations(courses, df):
    matrix = []
    for course1 in courses:
        for course2 in courses:
            rel_list = [course2]
            if course1 != course2:
                rel = relation(course1, course2, df)
                rel_list.extend(rel)
            matrix.append(rel_list)
    return matrix

# Dado una lista de relaciones, seleccionar las que son más representativas.


def define_relations_dict(rel, cota):
    relations = rel[:]
    r = ['and', 'xor', 'suc 1', 'suc 2', 'successor', 'predecessor']
    m = max(relations)
    i = relations.index(m)
    res = {}
    res[r[i]] = m
    if m >= 0.7:
        return res
    else:
        while True:
            del relations[i]
            del r[i]
            if len(relations) > 0:
                new_m = max(relations)
                if m - new_m > cota:
                    break
                else:
                    i = relations.index(new_m)
                    res[r[i]] = new_m
            else:
                break
        return res

# Dado una lista de relaciones, seleccionar las que son más representativas.


def define_relations_array(relations, cota):
    rel_names = ['and', 'xor', 'suc 1', 'suc 2', 'successor', 'predecessor']
    res = []
    for r in rel_names:
        res.append(0)
    rel_dict = define_relations_dict(relations, cota)
    for key in rel_dict:
        i = rel_names.index(key)
        res[i] = rel_dict[key]
    return res

# Unir en un único diccionario todas las relaciones representativas


def strong_rel(courses, df, cota):
    info_dict = {}
    for course1 in courses:
        info_dict[course1] = {}
        for course2 in courses:
            def_rel = None
            if course1 != course2:
                rel = relation(course1, course2, df)
                def_rel = define_relations_dict(rel, cota)
            info_dict[course1][course2] = def_rel
    return info_dict

# Define un diccionario con las relaciones como key y el value es una matriz con el valor de las relaciones.
# Se marcaron como 0 las rel no significativas en la matriz, para ver todas eliminar el filter_rel y cambiarlo en el append


def get_all_rel_by_rel(courses, relations, df, cota):
    result = {}
    for rel in relations:
        result[rel] = []
        for c in courses:
            result[rel].append([])
    count = 0
    for course1 in courses:
        for course2 in courses:
            if course1 != course2:
                rel_by_course = relation(course1, course2, df)
                filter_rel = define_relations_array(rel_by_course, cota)
                for i in range(0, len(rel_by_course)):
                    result[relations[i]][count].append(filter_rel[i])
            else:
                for key in result:
                    result[key][count].append(0)
        count += 1
    return result

# Crea grafo direccionado por arcos con peso


def create_graph(courses, relation_mat, rel):
    G = nx.DiGraph()
    for course in courses:
        G.add_node(course)
    c1 = 0
    for course1 in courses:
        c2 = 0
        for course2 in courses:
            if course1 != course2:
                if relation_mat[rel][c1][c2] > 0:
                    G.add_weighted_edges_from(
                        [(course1, course2, float(relation_mat[rel][c1][c2]))])
            c2 += 1
        c1 += 1
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    return G
