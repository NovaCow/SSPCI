import cmd
import os
import hashlib


# Currently on Version 0.1
# This is the SSPCI, Super Simple Python Command Interpreter, made in... well... Python
# Should be supported on (almost) everything. As it uses common libraries.
# I should at some point add error handling.
class SSPCI(cmd.Cmd):
    intro = "This is the SSPCI Shell, type help or ? to list current supported commands.\n"
    prompt = "sspci> "
    file = None
    CurrDir = os.getcwd()

    print("The current working directory is: " + str(CurrDir))

    def do_math(self, expression):
        """
        A simple math command, does math.
        """
        if expression:
            print(expression)  # Not yet figured this one out...
        else:
            print("Expression may not be a float or other error.")

    def do_echo(self, echo):
        """
        A command that echoes what you input.
        """
        if echo:
            print(echo)
        else:
            print("Empty echo statement or other error.")

    def do_ls(self, listedDir):
        """Lists current files in the entered directory.
        On Windows: ls d:/example/example
        On Linux: ls /home/example/example"""
        if listedDir:
            FilesInDir = os.listdir(listedDir)  # An issue with this method is that everything is printed on one line.
            print(str(FilesInDir))  # So if your directory is really full, your line can be 200 chars or longer
            # But it works, and that's what matters.
        else:
            listedDir = os.getcwd()
            print("The current directory is " + listedDir)  # Only said if no directory was specified.
            FilesInDir = os.listdir(listedDir)  # Now if you don't enter a directory you don't get an error!
            print(str(FilesInDir))  # But the same issue persists as with a directory.
            # But it works, and that's what matters.

    def do_cd(self, directory):
        """Navigates to a certain directory. Type the whole location of the directory
        On Windows: cd d:/example/example
        On Linux: cd /home/example/example"""
        if directory:
            os.chdir(directory)  # Switching directories!
            CurrDir = os.getcwd()  # I know it's ugly, but it sorta works.
            print("Switched working directory to: " + CurrDir)
        else:
            CurrDir = os.getcwd()  # If no new directory was specified, we say what directory we're currently in.
            print("The current working directory is: " + CurrDir)

    def do_mkdir(self, directory):
        """
        Creates a directory. Type the whole location of the directory.
        On Windows: mkdir d:/example/example
        On Linux: mkdir /home/example/example
        """
        if directory:
            os.mkdir(directory)
            print("Operation complete.")
        else:
            print("No directory specified.")

    def do_rmdir(self, directory):
        """Removes a directory. Type the whole location of the directory.
        On Windows: rmdir d:/example/example
        On Linux: rmdir /home/example/example"""
        if directory:
            os.rmdir(directory)
            print("Operation complete.")
        else:
            print("No directory specified.")

    def do_hashmd5(self, hashenc):  # Currently using MD5 and SHA-224, but I'll add SHA-1 and SHA-256 later
        """Hashes what you enter in MD5 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.md5(hashenc).hexdigest()  # Hashing in MD5 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_hashsha224(self, hashenc):
        """Hashes what you enter in SHA-224 format. Usage: hashsha224 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha224(hashenc).hexdigest()  # Hashing in SHA-224 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_end(self, none):  # Adding that none was necessary, I hate it.
        """
        Ends the current SSPCI session.
        """
        print("Ending current SSPCI Session...")
        print("Thank you for using SSPCI!")
        return True

    def postloop(self):
        pass


if __name__ == '__main__':
    SSPCI().cmdloop()
