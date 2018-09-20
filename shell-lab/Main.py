from cmd import Cmd
import sys, os, time, re, glob, time, stat, pty, subprocess

class MyPrompt(Cmd):
    prompt = "$ "
    intro = "Welcome to Sergio's shell!\nType help for list of commands."
    temp = ""
    file = False
    out = 1
    oldstdout = sys.stdout

    def precmd(self, line):
        return line

    def default(self, line):
        if (self.file == True):
            if (line != "EOF"):
                self.temp = line.split(" ")
                print(line + "")
            else:
                prompt = "$ "
                file = False
        if "|" in line:
            pipe()
        else:
            print("Command not found")

    def emptyline(self):
        pass

    def do_exit(self, inp):
        '''Exit the app'''
        return True

    def do_EOF(self, line):
        '''Exit the app when EOF is reached'''
        if (self.file == True):
            self.prompt = "$ "
            self.file = False
            sys.stdout = self.oldstdout
        else:
            pass

    def do_echo(self, line):
        '''Echo!'''
        for i in range(1, len(self.temp)):
            sys.stdout.write(self.temp[i] + " ")
        print()

    def do_wc(self, line):
        wc(line)

    def do_ls(self, line):
        if ">" in line:
            ls(line)
        else:
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
        if ">" in line:
            pwd(line)
        else:
            print(os.getcwd())

    def do_exec(self, line):
        exec()

    def do_copy(self, line):
        copy(line)


def saferfork():
    time.sleep(5)
    fork()


def fork():
    pid = os.getpid()
    os.write(1, ("About to fork (pid:%d)\n" % pid).encode())
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.write(1, ("I am child.  My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
    else:  # parent
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
        sys.exit(0)
    else:  # parent (forked ok)
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())


def ls(line):
    line = line.strip(" ")
    line = line.strip(">")
    pid = os.getpid()
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:  # child
        time.sleep(1)  # block for 1 second
        fdout = os.open(line, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU)
        os.dup2(fdout, pty.STDOUT_FILENO)
        files = os.listdir()
        for i in range(len(files)):
            print(files[i])
        os.close(fdout)
        sys.exit(0)
    else:  # parent (forked ok)
        childPidCode = os.wait()

def pwd(line):
    line = line.strip(" ")
    line = line.strip(">")
    pid = os.getpid()
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:  # child
        time.sleep(1)  # block for 1 second
        fdout = os.open(line, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRWXU)
        os.dup2(fdout, pty.STDOUT_FILENO)
        print(os.getcwd())
        os.close(fdout)
        sys.exit(0)
    else:  # parent (forked ok)
        childPidCode = os.wait()


def wc(line):

    line = line.split(" ")
    pid = os.getpid()
    rc = os.fork()

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


def exec():
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.close(sys.stdout.fileno())
        open("output5.txt", "w+")
        myPath = os.path.abspath("wordCount.py")
        cmd = ["long file.txt", "output5.txt"]
        os.execve(sys.executable, [sys.executable] + [myPath] + cmd, os.environ)
    else:  # parent (forked ok)
        wc = os.wait()


def copy(line):
    rc = os.fork()
    line = line.split(" ")
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc == 0:  # child
        os.close(sys.stdout.fileno())
        myPath = os.path.abspath("copy.py")
        os.execve(sys.executable, [sys.executable] + [myPath] + line, os.environ)
    else:  # parent (forked ok)
        wc = os.wait()


def pipe():
    #pid = os.getpid()
    read, write = os.pipe()
    rc = os.fork()
    if rc < 0:
        sys.exit(1)
    elif rc == 0:  # child
        os.close(write)
        os.dup2(read, 0)
        #exec()
        os.close(0)
        sys.exit(1)
    else:  # parent
        os.close(read)
        os.dup2(write, 1)
        os.close(write)
        #exec()


MyPrompt().cmdloop()