import random
import string

class Cipher:
    """
    Base class inherited by the project.
    """

    def __init__(self, target_string=None):
        try:
            self.target_string = str(target_string).lower()
        except Exception as e:
            raise e

    def encrypt(self) -> object:
        raise NotImplementedError()

    def decrypt(self):
        raise NotImplementedError()

    @staticmethod
    def prompt():
        raise NotImplementedError()


class Affine(Cipher):
    """
    Affine cipher is defined as one where a letter is mapped to its numeric equivalent,
    encrypted using a simple mathematical function, and converted back to a letter.
    TO USE: To encrypt or decrypt a string simply enter a valid ALPHABETICAL character (no numbers/non ascii).
    """

    def __init__(self, target_string=None):
        super().__init__(target_string)
        self.english_dict_alphakey = generate_english_dictionary(True)
        self.english_dict_numkey = generate_english_dictionary(False)
        self.affine_dict_numkey = {(5 * number + 8) % 26: letter for letter, number in self.english_dict_alphakey.items()}
        self.affine_dict_alphakey = {letter: (5 * number + 8) % 26 for letter, number in self.english_dict_alphakey.items()}

    def encrypt(self) -> object:
        non_encrpyted_chars_numbers = [self.english_dict_alphakey[letter] for letter in self.target_string]
        encrypted_chars = [self.affine_dict_numkey[number] for number in non_encrpyted_chars_numbers]
        return "".join(encrypted_chars)

    def decrypt(self):
        encrpyted_chars_number = [self.affine_dict_alphakey[letter] for letter in self.target_string]
        non_encrypted_chars = [self.english_dict_numkey[number] for number in encrpyted_chars_number]
        return "".join(non_encrypted_chars)

    @staticmethod
    def prompt():
        args = [input("Enter your text to encrypt or decrypt:  ")]
        return [args[0]]


class PolybusSquare(Cipher):
    """
    A cipher which uses a matrix to obfuscate the text entered.
    In this case we are using a virtual matrix in the form of a dictionary.
    TO USE ENCRYPT: To encrypt a string simply enter a valid ALPHABETICAL character (no numbers/non ascii).
    TO USE DECRYPT: Pass in a valid string of numbers.  No letters or non-ascii.
    """

    def __init__(self, target_string=None):
        super().__init__(target_string)
        self.letters_per_block = 6
        self.letters = list(generate_english_dictionary(True).keys())
        self.polybus_dict_alpha, self.polybus_dict_num = self.__generate_keys()

    def encrypt(self) -> object:
        encrpyted_chars = [self.polybus_dict_alpha[letter] for letter in self.target_string]
        return "".join(encrpyted_chars)

    def decrypt(self):
        tmp = iter(self.target_string)
        encrypted_chars = []
        for letter in tmp:
            encrypted_chars.append(str(letter) + str(next(tmp)))
        decrpyted_chars = [self.polybus_dict_num[letter] for letter in encrypted_chars]
        return "".join(decrpyted_chars)

    def __generate_keys(self):
        matrix_dict_alpha = {}
        matrix_dict_num = {}
        inner_index = 0
        outter_index = 0

        for letter in self.letters:
            if inner_index < self.letters_per_block:
                matrix_dict_alpha[letter] = str(outter_index) + str(inner_index)
                matrix_dict_num[str(outter_index) + str(inner_index)] = letter
                inner_index += 1
            else:
                matrix_dict_alpha[letter] = str(outter_index) + str(inner_index)
                matrix_dict_num[str(outter_index) + str(inner_index)] = letter
                inner_index = 0
                outter_index += 1
        return matrix_dict_alpha, matrix_dict_num

    @staticmethod
    def prompt():
        args = [input("Enter your text to encrypt or your numerical representation decrypt:  ")]
        return [args[0]]


class Keyword(Cipher):
    """
    A cipher which uses takes some a keyword to conceal the true identity of characters in a string.
    TO USE: Enter a valid ALPHABETICAL character (no numbers/non ascii).  Then enter your keyword.
    """
    def __init__(self, *args):
        super().__init__(args[0])
        if not args[1]:
            raise ValueError("Please enter a valid STRING!")
        else:
            self.alpha_keyword = args[1]
        self.letters = list(generate_english_dictionary(True).keys())
        self.keyword_dict_encrypt, self.keyword_dict_decrypt = self.__generate_keys()

    def encrypt(self) -> object:
        encrpyted_chars = [self.keyword_dict_encrypt[letter] for letter in self.target_string]
        return "".join(encrpyted_chars)

    def decrypt(self):
        decrpyted_chars = [self.keyword_dict_decrypt[letter] for letter in self.target_string]
        return "".join(decrpyted_chars)

    def __generate_keys(self):
        encrypt_dict = {}
        decrypt_dict = {}
        temp_letters = self.letters.copy()

        for each in self.alpha_keyword:
            temp_letters.remove(each)
            temp_letters.insert(0, each)

        for num in range(0, len(temp_letters)):
            encrypt_dict[self.letters[num]] = temp_letters[num]
            decrypt_dict[temp_letters[num]] = self.letters[num]
        return encrypt_dict, decrypt_dict

    @staticmethod
    def prompt():
        args = [input("Enter your text to encrypt or decrypt:  "), input("Now enter your keyword:  ")]
        return [args[0], args[1]]


def generate_english_dictionary(key_alpha=True):
    """
    Two choices for the method: alpha ordering or numerical ordering.
    Set keys to be alphabetical chars by setting true.  Otherwise it will use integer position in alphabet.
    """
    if key_alpha:
        return {letter: number for number, letter in enumerate(string.ascii_lowercase)}
    else:
        return {number: letter for number, letter in enumerate(string.ascii_lowercase)}
