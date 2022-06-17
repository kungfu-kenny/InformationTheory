import os
import json
from pprint import pprint


class CodeHuffman:
    """
    class which is dedicated to work with Huffman encoding/decoding
    """
    def __init__(self, message:str, file_path:str='') -> None:
        self.message = message
        self.file_path = file_path

    @staticmethod
    def check_previous_usage(path) -> None:
        """
        Static method which is dedicated to create folders if neccessary
        Input:  path = path to the selected files
        Output: folder on the an
        """
        os.path.exists(path) or os.mkdir(path)

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
                return value_list[0]
            left, right = value_list
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
    
    @staticmethod
    def produce_binary_normalizing(value_dict:dict) -> set:
        """
        Static method which is dedicated to develop the binary with the normilized size of it
        Input:  value_dict = dictionary with the selected calculations
        Output: set with selected values of the dictionary and its own size of the 8
        """
        def develop_range(len_max:int) -> set:
            for i in range(1, 10000000000000000000000):
                if 8*i > len_max:
                    return 8*i
        len_max = max(len(f) for f in value_dict.values())
        bit_size = develop_range(len_max)
        value_dict = {
            k: (bit_size - len(v))*"1" + v 
            for k, v in value_dict.items() 
        }
        ret = {
            k: bin(int(v, 2))
            for k, v in value_dict.items()
        }
        ret.update({
            "size": bit_size + 2
        })
        return ret

    def produce_encoding_file(self) -> None:
        """
        Method which is dedicated to produce the basic encoding files to the binary file of it
        Input:  None
        Output: we developed the text file to the simple binary file
        """
        # self.check_previous_usage(os.path.join(os.getcwd(), 'storage'))
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r') as file_read:
            self.message = file_read.read()
        value_dict = self.develop_dict_count()
        value_list = self.develop_letter_popular(value_dict)
        value_dict = self.produce_tree_basic(value_list)
        value_dict = self.produce_tree_reconstruction(value_dict)
        value_dict = self.produce_binary_normalizing(value_dict)
        value_bytes = ''.join(
            value_dict.get(l, '0')
            for l in self.message
        )
        value_bytes = value_bytes.encode()
        with open(f"{self.file_path}.bin", 'wb') as file_write:
            file_write.write(value_bytes)
        with open(f"{self.file_path}.json", 'w') as json_write:
            json.dump(
                value_dict, 
                json_write, 
                indent=4
            ) 

    def produce_decoding_file(self) -> None:
        """
        Method which is dedicated to produce the basic decoding of the file
        Input:  None
        Output: we developed the decoded file from it
        """
        value_path = f"{self.file_path}.bin"
        value_path_json = f"{self.file_path}.json"
        if not os.path.exists(value_path) or not os.path.exists(value_path_json):
            print('Files not present')
            return
        with open(value_path, 'rb') as file_read, open(value_path_json, 'r')  as json_read:
            used = file_read.read().decode()
            value_dict = json.load(json_read)
            value_dict = {v:k for k, v in value_dict.items()}
        used = ''.join(value_dict.get(f"0b{f}") for f in used.split('0b')[1:])
        with open(os.path.join(os.getcwd(), 'storage', 'new.txt'), 'w') as file_new:
            file_new.write(used)
        #TODO complete the mistake
        # for f, k in zip(used, self.message):
        #     print(f, k, f==k)
        #     print('-----------------------')
        
if __name__ == '__main__':
    tst = input()
    file = os.path.join(os.getcwd(), 'storage', 'tst.txt')
    a = CodeHuffman(tst, file)
    encoded, encoded_dict = a.produce_encoding_basic()
    tst_check = a.produce_decoding_basic(encoded, encoded_dict)
    a.produce_encoding_file()
    a.produce_decoding_file()