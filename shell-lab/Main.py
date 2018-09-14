from cmd import Cmd
import tokenize


class MyPrompt(Cmd):
    prompt = "$ "
    intro = "Welcome to Sergio's shell!\nType help for list of commands."

    def do_exit(self, inp):
        '''Exit the app'''
        return True

    def do_EOF(self, line):
        '''Exit the app when EOF is reached'''
        return True

MyPrompt().cmdloop()

print("Closing")