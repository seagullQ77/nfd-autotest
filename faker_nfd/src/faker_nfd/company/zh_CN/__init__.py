from faker.providers.company.zh_CN import Provider as FackerProvider

class Provider(FackerProvider):

    def corporate_code(cls):
        return cls.numerify("###############")

    def organization_code(cls):
        org = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
               "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
               "U", "V", "W", "X", "Y", "Z"]
        base = ""
        for i in range(8):
            base += cls.random_element(org)
        count = 0
        weight = [3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        mp_value = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "I": 18, "J": 19,
                    "K": 20, "L": 21, "M": 22, "N": 23, "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29,
                    "U": 30, "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35}
        for i in range(0, len(base)):
            count = count + mp_value[base[i]] * weight[i]
        base += '-' + str(11 - count % 11)  # 算出校验码
        return base
