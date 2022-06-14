import os
import math
from pprint import pprint


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
        
    def develop_tree(self) -> dict:
        """
        Method which is dedicated to create basic tree
        """
        value_dict = self.develop_alphabet()
        # pprint(value_dict)
        # print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')



if __name__ == '__main__':
    a = CodeShannonFanno('rewityuwrrwetyuiryituerwytuierytiurewytvvcxtfyguiasdxcszuiolkfdhngibgudfgysfdugyrtwyurei')
    a.develop_tree()