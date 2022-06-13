import math


class CheckEntropy:
    """
    class which is dedicated to check the basic entropies from the usage
    """
    def __init__(self, message:str='', k:int=1) -> None:
        self.message = message
        self.name_count = {}
        self.k = k

    def calculate_dict_count(self, used_str:str='', used_bool:bool=False) -> None:
        """
        Method which is dedicated to calculate the countings
        Input:  used_str = used string
                used_bool = True if to return values False to set as self variable
        Output: we developed the dictionary to the count
        """
        if not used_str or not isinstance(used_str, str):
            used_str = self.message
        if not used_str:
            return {}
        if used_bool:
            return {
                i: used_str.count(i) / len(used_str)
                for i in set(list(used_str))
            }
        else:
            self.name_count = {
                i: used_str.count(i) / len(used_str)
                for i in set(list(used_str))
            }

    def calculate_entropy(self, used_dict:dict={}, used_str:str='', used_k:int=0) -> int:
        """
        Method which is dedicated to calculate entropy from the 
        Input:  used_dict = dictionary value for the 
                used_str = string which we could use further
        Output: int value for the entropy values
        """
        if not used_dict and not used_str:
            self.calculate_dict_count()
            e = -sum(math.log2(j) for j in self.name_count.values())
        elif not used_dict and used_str:
            e = -sum(math.log2(j) for j in self.calculate_dict_count(used_str, True).values())
        elif used_dict and not used_str:
            e = -sum(math.log2(j) for j in used_dict.values())
        if not used_k:
            used_k = self.k
        return used_k * round(e, 3)

if __name__ == '__main__':
    a = CheckEntropy(input())
    a.calculate_dict_count()
    entropy = a.calculate_entropy()
    print(entropy)