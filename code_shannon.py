import math
import struct


class CodeShannon:
    """
    class which is dedicated to develop the shannon codes for the string
    """
    def __init__(self, message:str='') -> None:
        self.message = message

    @staticmethod
    def develop_entropy(p:float) -> float:
        """
        Static method which is dedicated to develop entropy value of selected values
        Input:  p = probability of selected number
        Output: float with calculated entropy
        """
        return abs(p*math.log2(p))

    @staticmethod
    def develop_bin(b:float) -> str:
        """
        Static method which is dedicated to calculated bin from values
        Input:  b = b number after the calculation
        Output: we developed the binary values
        """
        return ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', b))

    @staticmethod
    def develop_l(b:float) -> int:
        """
        Static method which is dedicated to create l value from it
        Input:  b = value of the used value
        Output: we developed the in value for it
        """
        for i in range(-1, -10000000000000000000000000, -1):
            if 2**i <= b:
                return -i

    def develop_alphabet(self) -> dict:
        """
        Method which is dedicated to provide the alphabet values to the
        Input:  None
        Output: we created the dictionary of the used values
        """
        return {
            i: round(self.message.count(i)/len(self.message), 2)
            for i in set(self.message) 
        }

    def develop_encode_basic(self) -> str:
        """
        Method which is dedicated to develop basic encoded values
        Input:  None
        Output: string with the getting values encoded
        """
        value_dict = self.develop_alphabet()
        value_used = sorted(
            [(k, v) for k, v in value_dict.items()], 
            key=lambda x:x[1], 
            reverse=True
        )
        value_b = [
            [k, sum(v for _, v in value_used[:i])] 
            if i > 0 else [k, 0] 
            for i, (k, _) in enumerate(value_used)
        ]
        value_bin = {
            k:self.develop_bin(b)
            for k, b in value_b
        }
        value_i = {
            k:self.develop_l(u)
            for k, u in value_used
        }
        return value_bin


if __name__ == '__main__':
    a = CodeShannon('fddsfdsafisofdpgfdjiodfgopbvnmisjewqpoi')
    a.develop_encode_basic()