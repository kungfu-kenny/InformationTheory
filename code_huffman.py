

class CodeHuffman:
    """
    class which is dedicated to work with Huffman encoding/decoding
    """
    def __init__(self, message:str) -> None:
        self.message = message

    def develop_dict_count(self) -> dict:
        """
        Method which is dedicated to create the count values to it
        Input:  None
        Output: we developed the dictionary to the selected
        """
        return {
            l: self.message.count(l)
            for l in set(self.message)
        }

    @staticmethod
    def develop_letter_popular(value_dict:dict, reverse:bool=False) -> list:
        """
        Static method which is dedicated to develop the most popular letters
        Input:  value_dict = dictionary with the selected letters
        Output: we developed list of the letter and count sorted
        """
        return sorted(
            ([k, v] for k, v in value_dict.items()), 
            key=lambda x:x[1], 
            reverse=reverse
        )

    @staticmethod
    def find_smallest_elements(value_list:list) -> set:
        """
        Static method which is dedicated to develop the smallest elements from the list
        Input:  value_list = list of the selected values
        Output: set of the selected values to it
        """
        if len(value_list) < 1:
            return 0, 0, False
        index_min = [f[1] for f in value_list].index(min((f[1] for f in value_list)))
        prev, next = index_min - 1, index_min + 1 
        prev = prev % len(value_list) if prev > -1 else (len(value_list) + prev) % len(value_list)
        next = next % len(value_list) if next > -1 else (len(value_list) + next) % len(value_list)
        if next == prev:
            return 0, 0, False
        elif value_list[next][1] >= value_list[prev][1]:
            return index_min, prev, True
        return index_min, next, True

    def produce_tree_basic(self, value_list:list) -> dict:
        """
        Method which is dedicated to produce the basic tree of the smallest values
        Input:  value_list = value list of the selected 
        Output: we created the values of the selected 
        """
        min_use, min_next, value_continue = self.find_smallest_elements(value_list)
        if not value_continue:
            if len(value_list) == 1:
                print('We are here!!!!')
                return value_list[0]
            left, right = value_list
            if left[1] >= right[1]:
                return {
                    '1': right[0],
                    '0': left[0]
                }
            return {
                '1': left[0],
                '0': right[0]
            }
        if min_next > min_use:
            zero = value_list.pop(min_next)
            one = value_list.pop(min_use)
        else:
            one = value_list.pop(min_use)
            zero = value_list.pop(min_next)
        value_list.insert(
            min(min_use, min_next),
            [
                {
                    '1':one[0],
                    '0':zero[0]
                },
                zero[1] + one[1]
            ]
        )
        return self.produce_tree_basic(value_list)

    def produce_tree_reconstruction(self, value_dict:dict, value_list:list=[], value_return:dict={}) -> dict:
        """
        Method which is dedicated to create the selected
        Input:  value_dict = dictionary of the calculated
                value_list = list of the selected numbers
                value_return = dictionary with letter and its code
        Output: dictionary to the letters
        """
        for k, v in value_dict.items():
            if not isinstance(v, dict):
                value_return.update({v: ''.join(value_list + [k])})
            else:
                self.produce_tree_reconstruction(v, value_list + [k], value_return)
        return value_return

    def produce_encoding_basic(self) -> set:
        """
        Method which is dedicated to use the basic encode values
        Input:  None
        Output: string encoded message and the dictionary of keys
        """
        value_dict = self.develop_dict_count()
        value_list = self.develop_letter_popular(value_dict)
        value_dict = self.produce_tree_basic(value_list)
        value_dict = self.produce_tree_reconstruction(value_dict)
        value_return = self.message
        for k, v in value_dict.items():
            value_return = value_return.replace(k, f'{v} ')
        return value_return, value_dict

    def produce_decoding_basic(self, encoded:str, value_dict:dict) -> str:
        """
        Method which is dedicated to use the basic decode of the values
        Input:  encoded = string which was previously used to this algorythm
                value_dict = dictionary of the used previously values
        Output: string of the decoded values
        """
        value_return = encoded
        for k, v in sorted(([k, v] for k, v in value_dict.items()), key=lambda x: len(x[1]), reverse=True):
            value_return = value_return.replace(f'{v} ', k)
        return value_return

if __name__ == '__main__':
    tst = input()
    a = CodeHuffman(tst)
    encoded, encoded_dict = a.produce_encoding_basic()
    tst_check = a.produce_decoding_basic(encoded, encoded_dict)
    