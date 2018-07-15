import ciphers
import inspect
import sys

class Menu:

    options = {"Exit Program":["q", "quit", "escape"],
               "Encrypt a String":["e", "encrypt"],
               "Decrypt a String":["d", "decrypt"]}

    def __init__(self):
        pass

    def run(self):
        self._display_options()


    def _display_options(self):
        for option, command in self.options.items():
            print("Select {} to {}".format(command, option))

    def _get_user_request(self):
        try:
            selection = input("So which option will it be?")
            if selection.lower() in self.options.get("Exit Program"):
                sys.exit("Thanks for playing!")
            elif selection.lower() in self.options.get("Encrypt a String"):
                self.run_encyption()

        except:
            print("I am sorry.  That it not a valid option.  Please choose from these options")
            self._display_options()
            self._get_user_request()


    def run_encyption(self):
        pass

    def run_decryption(self):
        pass

    def _get_cipher_from_user(self):
        try:
            cipher_choice = input("Select which cipher you would like to run:")
        except:
            pass

    @classmethod
    def get_available_ciphers(self):
        return [klass for klass in dir(ciphers) if isinstance(klass.__class__(), type(ciphers.Cipher()))]





clsmembers = inspect.getmembers(sys.modules["ciphers"], inspect.isclass)
print(clsmembers)