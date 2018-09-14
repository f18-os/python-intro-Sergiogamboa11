from cmd import Cmd
import sys


class MyPrompt(Cmd):
    prompt = "$ "
    intro = "Welcome to Sergio's shell!\nType help for list of commands."
    temp = ""
    def do_exit(self, inp):
        '''Exit the app'''
        return True

    def do_EOF(self, line):
        '''Exit the app when EOF is reached'''
        return True

    def do_echo(self, line):
        '''Echo!'''
        for i in range(len(self.temp)):
            sys.stdout.write(self.temp[i] + " ")
        print()

    def precmd(self, line):
        self.temp = line.split(" ")
        return line

MyPrompt().cmdloop()

print("Closing")