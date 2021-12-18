import os
from clause import Clause

INPUT_DIR = './input'
OUTPUT_DIR = './output'


def read_input(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines() # Doc file

    alpha = Clause(lines[0]) # Tao clause alpha tu dong dau tien
    clauses = [] # Cac clause trong KB
    for line in lines[2:]: # Tao clause tu cac dong 3 tro di
        clauses.append(Clause(line))

    return alpha, clauses


def PL_Resolution(clauses, filename):
    f = open(os.path.join(OUTPUT_DIR, filename), 'w')
    clause_set = set(clauses)
    new_set = set()
    flag = False

    while True:
        clauses = list(clause_set)
        lines = [] # Cac clause ghi vao output

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = Clause.resolve(clauses[i], clauses[j]) # Hop giai
                if resolvent is None:
                    continue
                if resolvent.is_empty():
                    flag = True
                new_set.add(resolvent)
                lines.append(resolvent.to_string())

        f.write(str(len(lines)) + '\n')
        for line in lines:
            f.write(line + '\n')
        if flag:
            f.write('YES')
            f.close()
            return
        if new_set.issubset(clause_set):
            f.write('NO')
            f.close()
            return
        clause_set = clause_set.union(new_set)


def main():
    for filename in os.listdir(INPUT_DIR):
        alpha, clauses = read_input(os.path.join(INPUT_DIR, filename))
        clauses.extend(Clause.NOT(alpha))

        PL_Resolution(clauses, filename)


if __name__ == '__main__':
    main()