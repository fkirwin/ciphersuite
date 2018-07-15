import ciphers
import sys


class Menu:
    """
    This class will handle all IO with the user.
    """
    def __init__(self):
        self.options = {"Exit Program": ["q", "quit", "escape"],
                        "Encrypt a String": ["e", "encrypt"],
                        "Decrypt a String": ["d", "decrypt"]}

    def run(self):
        while True:
            self._get_user_request()
            try_again = input("Type y to keep ciphering.")
            if try_again.lower() == 'y':
                continue
            else:
                break

    def _get_user_request(self):
        self._display_options()
        selection = input("So which option will it be?")
        if selection.lower() in self.options.get("Exit Program"):
            sys.exit("Thanks for playing!")
        elif selection.lower() in self.options.get("Encrypt a String"):
            print(self._get_available_ciphers())
            try:
                cipher_selection = self._get_cipher_from_user()
                self._run_encyption(cipher_selection)
            except (TypeError, ValueError, Exception):
                print("That entry is not valid.  Please select an option from the menu.")
                self._get_user_request()
        elif selection.lower() in self.options.get("Decrypt a String"):
            print(self._get_available_ciphers())
            try:
                cipher_selection = self._get_cipher_from_user()
                self._run_decryption(cipher_selection)
            except (TypeError, ValueError, Exception):
                print("That entry is not valid.  Please select an option from the menu.")
                self._get_user_request()
        else:
            print("I am sorry. That selection is invalid...")
            self._get_user_request()

    def _run_encyption(self, cipher_string):
        try:
            cipher = getattr(ciphers, cipher_string)
            print(cipher.__doc__)
            user_args = cipher.prompt()
            klass = cipher(*user_args)
            print(klass.encrypt())
        except (TypeError, ValueError):
            print("A valid parameter must be passed in according to your cipher's instructions.")

    def _run_decryption(self, cipher_string):
        try:
            cipher = getattr(ciphers, cipher_string)
            print(cipher.__doc__)
            user_args = cipher.prompt()
            klass = cipher(*user_args)
            print(klass.decrypt())
        except (TypeError, ValueError, Exception):
            print("A valid parameter must be passed in according to your cipher's instructions.")

    def _get_cipher_from_user(self):
        try:
            cipher_choice = input("Select which cipher you would like to run:")
            return cipher_choice
        except (TypeError, ValueError, Exception):
            print("Please enter a valid cipher.  A specific string just as you see here.")
            self._get_available_ciphers()

    def _get_available_ciphers(self):
        return [klass.__name__ for klass in ciphers.Cipher.__subclasses__()]

    def _display_options(self):
        print("Welcome to ciphersuite.")
        for option, command in self.options.items():
            print("Select {} to {}".format(command, option))
