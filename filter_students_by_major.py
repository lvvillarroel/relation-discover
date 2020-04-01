import pandas as pd
from functions import students_selection, relation, define_relations_array, get_all_rel_by_rel, create_graph

# Dataframe con las notas por cursos
data = pd.read_excel('notas_alumnos.xlsx', index_col=None, dtype={'ID': int, 'AÑO ADMISIÓN': int, 'MAJOR SELECCIONADO': str,
                                                                  'SIGLA': str, 'NOMBRE CURSO': str, 'NOTA FINAL': float,
                                                                  'AÑO': int, 'SEMESTRE': int, 'PPA GLOBAL': float})

# filtrar y eliminar columnas que no sirven
df = data[['ID', 'SIGLA', 'NOTA FINAL', 'AÑO', 'SEMESTRE', 'PPA GLOBAL']]

# Agrupar los datos por alumno y agregar una columna que indica el número de semestre de la carrera
stg = df.groupby('ID')
sem_array = []
for student, group in stg:
    sem = 0
    year = 0
    path = 0
    for row in group.itertuples():
        if row.AÑO > year or row.SEMESTRE > sem:
            year = row.AÑO
            sem = row.SEMESTRE
            path += 1
        sem_array.append(path)

df.insert(4, 'DURACIÓN', sem_array, True)

# CURSOS INVESTIGACIÓN OPERATIVA
#                   opti,      micro,   estocast,   métodos,    conta,      orga,    casptone   (ICS2526 o EYP2114)
io_all_courses = ['ICS1113', 'ICS2523', 'ICS2123', 'ICS2121',
                  'ICS2613', 'ICS2813', 'ICS2122', 'EYP2114', 'ICS2562']
io_courses = ['ICS1113', 'ICS2523', 'ICS2123',
              'ICS2121', 'ICS2613', 'ICS2813', 'ICS2122']
options = ['EYP2114', 'ICS2562']


# Filtrar a alumnos que han aprobado los cursos del major de IO
df_base = df.loc[df['SIGLA'].isin(io_all_courses)]
df_aprov = df_base[df_base['NOTA FINAL'] >= 4]
student_groups = df_aprov.groupby(['ID'])

# Filtrar por alumnos que hayan completado el major (realizar todos los cursos)
io_students = students_selection(student_groups, io_courses, options)
df_io = df_aprov.loc[df_base['ID'].isin(io_students)]

# Seleccionar solo las relaciones representativas. Se genera un diccionario con la info
relations = ['and', 'xor', 'suc 1', 'suc 2', 'successor', 'predecessor']
mat_rel = get_all_rel_by_rel(io_all_courses, relations, df_io, 0.2)
create_graph(io_all_courses, mat_rel, 'suc 2')
