class Clause:
    def __init__(self, string='', **kwargs):
        """
        self.literal 
            La mot dict() voi key la cac ky tu 'A'..'Z'.
            Moi ky tu dai dien cho mot literal, co value thuoc {-1, 0, 1} chi trang thai:
              -1: Co trong clause, co dau NOT phia truoc
               0: Khong co trong clause
               1: Co trong clause, khong co dau NOT phia truoc
        """
        self.literal = {}

        for i in range(ord('A'), ord('Z') + 1):
            ch = chr(i)
            self.literal[ch] = 0
        
        for raw_lit in string.split('OR'):
            lit = raw_lit.replace(' ', '').replace('\n', '') # Loai bo ky tu space va xuong dong
            if len(lit) == 0:
                continue
            ch = lit[-1]
            if len(lit) == 1:
                self.literal[ch] = 1
            else:
                self.literal[ch] = -1

        # Cho phep truyen literal vao constructor de khoi tao nhanh. VD: Clause(A=1, C=-1) ~ "A OR -C"
        for key, val in kwargs.items():
            self.literal[key] = val


    # Override __hash__ va __eq__ de dung set() cua python
    # Assert: Hai clause giong nhau thi chuyen sang hai string giong nhau
    def __hash__(self):
        return hash(self.to_string())


    def __eq__(self, other):
        return self.to_string() == other.to_string()


    @staticmethod
    def NOT(clause):
        """
        Tra ve ket qua phep NOT(clause), la mot List chua cac clauses
        VD: NOT(A OR B) = NOT(A) AND NOT(B) --> Tra ve [Clause('-A'), Clause('-B')]
        """
        res = []
        for ch, value in clause.literal.items():
            if value != 0:
                kwargs = {ch : value * -1}
                res.append(Clause(**kwargs))
        return res


    @staticmethod
    def resolve(clause_1, clause_2):
        """
        Ham hop giai 2 clauses:
            + Tra ve None neu menh de ket qua la True (khong can thiet)
            + Tra ve None neu khong co cap literal trai dau
            + Nguoc lai, tra ve clause ket qua
        """
        flag = False
        kwargs = {}
        for i in range(ord('A'), ord('Z') + 1):
            ch = chr(i)
            if clause_1.literal[ch] * clause_2.literal[ch] == -1: # Cap trai dau (1 vs -1)
                if flag:
                    # Truoc do da co cap trai dau --> Ket qua luon la True 
                    return None
                flag = True
                kwargs[ch] = 0
            elif clause_1.literal[ch] != clause_2.literal[ch]: # co mot value 0
                kwargs[ch] = clause_1.literal[ch] + clause_2.literal[ch]
            else: # cap value bang nhau
                kwargs[ch] = clause_1.literal[ch]
        if not flag:
            return None
        # Tra ve clause ket qua
        return Clause(**kwargs)


    def to_string(self):
        """
        Ham tra ve clause o dang string (Rong: "{}")
        """
        literals = []
        for ch, value in self.literal.items():
            if value == 1:
                literals.append(ch)
            elif value == -1:
                literals.append('-' + ch)
        string = ' OR '.join(literals)
        if string == '':
            return '{}'
        return string


    def is_empty(self):
        """
        Kiem tra clause co empty?
        """
        return self.to_string() == '{}'


