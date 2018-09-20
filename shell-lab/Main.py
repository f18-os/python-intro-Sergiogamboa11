from cmd import Cmd
import sys, os, time, re, glob, time, stat, pty, subprocess

class MyPrompt(Cmd):

    prompt = "$ "
    intro = "Welcome to Sergio's shell!\nType help for list of commands."
    temp = ""
    file = False
    out = 1

    # If a command is not found, "Command not found" is printed
    # If there is a pipe, we call the pipe method
    def default(self, line):
        if "|" in line:
            pipe()
        else:
            print("Command not found")

    # If empty line is input, nothing happens
    def emptyline(self):
        pass

    # Shell exits with exit command
    def do_exit(self, inp):
        '''Exit the app'''
        return True

    # Shell exits when EOF is reached
    def do_EOF(self, line):
        '''Exit the app when EOF is reached'''
        return True

    # Anything after 'echo' is printed back out
    def do_echo(self, line):
        '''Echo!'''
        self.temp = line.split(" ")
        for i in range(len(self.temp)):
            sys.stdout.write(self.temp[i] + " ")
        print()

    def do_wc(self, line):
        wc(line)

    # Prints out list of current files, can be redirected
    def do_ls(self, line):
        '''Lists all files in the directory'''
        if ">" in line:
            ls(line)
        else:
            files = os.listdir()
            for i in range(len(files)):
                print(files[i])

    # Changes current directory
    def do_cd(self, line):
        '''Changes directory'''
        if(os.path.exists(line)):
            os.chdir(line)
        else:
            print("Directory not found")
        print(os.getcwd())

    # Prints out current directory, can be redirected
    def do_pwd(self, line):
        '''Prints out the current directory'''
        if ">" in line:
            pwd(line)
        else:
            print(os.getcwd())

    def do_exec(self, line):
        exec()

    def do_copy(self, line):
        copy(line)

# This method calls fork() after a 5 second delay
def saferfork():
    time.sleep(5)
    fork()


# This method performs the basic fork command
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


# This method performs the wait command
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


# This method redirects the ls command in a separate process
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


# This method redirects the pwd command in a separate process
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


# An attempt to implement the pipe functionality to the shell (not working)
def pipe():
    read, write = os.pipe()
    os.set_inheritable(read, True)
    os.set_inheritable(write, True)
    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif rc == 0:  # child
        os.close(write)
        os.dup2(read, 0)
        #execve()
        os.close(0)
        sys.exit(1)
    else:  # parent
        os.close(read)
        os.dup2(write, 1)
        os.close(write)
        #execve()


MyPrompt().cmdloop()