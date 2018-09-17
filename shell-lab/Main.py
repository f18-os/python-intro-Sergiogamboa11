from cmd import Cmd
import sys, os, time, re

class MyPrompt(Cmd):
    prompt = "$ "
    intro = "Welcome to Sergio's shell!\nType help for list of commands."
    temp = ""

    def precmd(self, line):
        #self.temp = line.split(" ")
        #wait()
        return line

    def default(self, line):
        print("Command not found")

    def emptyline(self):
        pass

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

    def do_tokenize(self, line):
        tokenize(line)

    def do_ls(self, line):
        files = os.listdir()
        for i in range(len(files)):
            print(files[i])

    def do_cd(self, line):
        if(os.path.exists(line)):
            os.chdir(line)
        else:
            print("Directory not found")
        print(os.getcwd())

    def do_pwd(self, line):
        print(os.getcwd())


def fork():
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    else:  # parent (forked ok)
        os.write(1, ("I am parent.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())


def wait():
    pid = os.getpid()

    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())
        time.sleep(1)  # block for 1 second
        os.write(1, "Child   ....terminating now with exit code 0\n".encode())
        sys.exit(0)
    else:  # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())


def tokenize(line):

    line = line.split(" ")
    pid = os.getpid()
    rc = os.fork() #or fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        print(sys.argv[0])
        myPath = os.path.abspath("wordCount.py")
        cmd = ["input.txt", "output.txt"]
        os.execve(sys.executable, [sys.executable] + [myPath] + line, os.environ)
    else:  # parent (forked ok)
        wc = os.wait()  #or just wait?
        os.write(1, ("I am parent.  My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())

MyPrompt().cmdloop()

print("Closing")