import os
from clause import Clause

INPUT_DIR = './input'
OUTPUT_DIR = './output'
DETAIL_DIR = './detail' # Ghi chi tiet tung buoc de them vao report
INPUT_PREFIX = 'input'
OUTPUT_PREFIX = 'output'


def read_input(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines() # Doc file

    alpha = Clause(lines[0]) # Tao clause alpha tu dong dau tien
    n = int(lines[1])
    clauses = [] # Cac clause trong KB
    for line in lines[2:2+n]: # Tao clause tu cac dong 3 tro di
        clauses.append(Clause(line))

    return alpha, clauses


def PL_Resolution(clauses, filename):
    f1 = open(os.path.join(OUTPUT_DIR, filename), 'w') # File output chuan theo yeu cau
    f2 = open(os.path.join(DETAIL_DIR, filename), 'w') # File detail ghi chi tiet tung buoc

    clause_set = set(clauses)
    new_set = set()
    flag = False

    while True:
        clauses = list(clause_set)
        lines = set() # Cac clause ghi vao output
        
        # Ghi danh sach clauses ra file detail
        f2.write('-' * 20)
        f2.write('\nClauses:\n')
        for clause in clauses:
            f2.write('\t' + clause.to_string() + '\n')
        f2.write('Resolutions:\n')

        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = Clause.resolve(clauses[i], clauses[j]) # Hop giai
                if resolvent is None or resolvent in new_set or resolvent in clause_set:
                    continue # Bo qua khi resolvent == None hoac resolvent da ton tai
                # Ghi thong tin thao tac resolve vao file detail
                f2.write('\t' + clauses[i].to_string() + '\n')
                f2.write('\t' + clauses[j].to_string() + '\n')
                f2.write('\t' + resolvent.to_string() + '\n\n')
                if resolvent.is_empty(): 
                    flag = True # Khi hop giai tra ve rong, danh dau flag de return khi ket thuc vong lap
                new_set.add(resolvent)
                lines.add(resolvent.to_string())

        # Ghi ket qua vong lap vao file output
        f1.write(str(len(lines)) + '\n')
        for line in lines:
            f1.write(line + '\n')

        # Neu flag duoc bat (tim ra resolvent rong) --> Ket luan la YES (KB entails alpha)
        if flag:
            f1.write('YES')
            f1.close()
            return

        # Neu khong tim duoc clause moi --> Ket luan la NO (KB not entails alpha)
        if new_set.issubset(clause_set):
            f1.write('NO')
            f1.close()
            return

        # Hop nhat hai set
        clause_set = clause_set.union(new_set)


def main():
    for filename in os.listdir(INPUT_DIR):
        alpha, clauses = read_input(os.path.join(INPUT_DIR, filename))

        # not_alpha la mot list chua cac clause cua NOT(alpha)
        # VD: alpha = "A OR -B"  -->  NOT(alpha) = "-A AND B"  -->  ["-A", "B"]
        not_alpha = Clause.NOT(alpha)
        clauses.extend(not_alpha) # Them cac clause trong not_alpha vao danh sach

        PL_Resolution(clauses, filename.replace(INPUT_PREFIX, OUTPUT_PREFIX))


if __name__ == '__main__':
    main()