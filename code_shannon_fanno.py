

class CodeShannonFanno:
    """
    class which is dedicated to work with the coding of the information
    """
    def __init__(self, message:str='') -> None:
        self.message = message

    def develop_alphabet(self) -> dict:
        """
        Method which is dedicated to develop values
        Input:  None
        Output: we developed the alphabet values
        """
        return {
            f:self.message.count(f)
            for f in set(list(self.message))
        }
        
    @staticmethod
    def develop_division_value(value_list:list) -> int:
        """
        Static method which is dedicated to develop the division index from the list
        Input:  value_list = list of the selected values
        Output: we developed the index to split list into two
        """
        return sorted(
            [
                [
                    ind, 
                    abs(
                        sum(f[1] for f in value_list[:ind]) - sum(f[1] for f in value_list[ind:])
                    )
                ]
                for ind, _ in enumerate(value_list)
            ], key=lambda x: x[1]
        )[0][0]

    def develop_code_tree(self, value_list:list) -> dict:
        """
        Method which is dedicated to develop the coding tree of the symbol
        Input:  value_list = list of the selected letters
        Output: we created the tree of the letters to change
        """
        index = self.develop_division_value(value_list)
        value_one = value_list[:index]
        value_zero = value_list[index:]
        value_dict = {
            '1': self.develop_code_tree(value_one) if len(value_one) > 1 else value_one,
            '0': self.develop_code_tree(value_zero) if len(value_zero) > 1 else value_zero
        }
        return value_dict

    def develop_tree_symbols(self, value_dict:dict, value_list:list=[], value_return:dict={}) -> dict:
        """
        Method which is dedicated to develop the tree to the symbolic values of them
        Input:  value_dict = dictionary to work with
                value_list = list of the indexes of used
                value_return = calculated values of the alphabet
        Output: we created the tree for the selected symbols
        """
        for k, v in value_dict.items():
            if not isinstance(v, dict):
                value_return.update({v[0][0]: ''.join(value_list + [k])})
            else:
                self.develop_tree_symbols(v, value_list + [k], value_return)
        return value_return

    def develop_tree(self) -> dict:
        """
        Method which is dedicated to create basic tree values
        Input:  None
        Output: we developed dictionary to make the next tree values
        """
        alphabet = self.develop_alphabet()
        value_calc = sorted(((k, v) for k, v in alphabet.items()), key=lambda x:x[1], reverse=True)
        value_diff = self.develop_division_value(value_calc)
        value_dict = {
            '1': value_calc[:value_diff],
            '0': value_calc[value_diff:],
        }
        value_dict = self.develop_code_tree(value_calc)
        return self.develop_tree_symbols(value_dict)
        
    def develop_encode_basic(self) -> set:
        """
        Method which is dedicated to create the basic entropy by the shannon fanno
        Input:  input string
        Output: string with the codes and the dict with the map of the code
        """
        value_map = self.develop_tree()
        value_change = [[k, v] for k, v in value_map.items()]
        value_return = self.message
        for letter, code in value_change:
            value_return = value_return.replace(letter, f'{code} ')
        return value_return, value_map

    def develop_decode_basic(self, value_encoded:str, value_dict:dict) -> str:
        """
        Method which is dedicated to decode the basic string for the decoding
        Input:  value_code = encoded string by the algorythm
                value_dict = dictionary values for the getting cyphers used
        Output: we created the string to decode it
        """
        value_change = ([k, v] for k, v in value_dict.items())
        value_change = sorted(value_change, key=lambda x: len(x[1]), reverse=True)
        value_return = value_encoded
        for letter, code in value_change:
            if code in value_return:
                value_return = value_return.replace(f"{code} ", letter)
        return value_return


if __name__ == '__main__':
    check = input()
    a = CodeShannonFanno(check)
    encoded, dict = a.develop_encode_basic()
    decoded = a.develop_decode_basic(encoded, dict)
    print(decoded==check)