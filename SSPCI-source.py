import cmd
import os
import hashlib


# Currently on Version 0.2-alpha-source
# The source version is basically the same as the release version, but will have more frequent and unstable
# updates, so keep that in mind.
# This is the SSPCI, Super Simple Python Command Interpreter, made in... well... Python
# Should be supported on (almost) everything. As it uses common libraries.
# I should at some point add error handling. Because I don't have that currently.
class SSPCI(cmd.Cmd):
    intro = "This is the SSPCI Shell, type help or ? to list current supported commands.\n"
    prompt = "sspci> "
    file = None
    CurrDir = os.getcwd()

    print("The current working directory is: " + str(CurrDir))

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

    def do_filecreate(self, filename):
        """Creates a file in the working directory. Usage: filecreate amazingFileName.txt"""
        if filename:
            fileToCreate = open(filename, "x")
            print("Operation complete.")
        else:
            print("No filename specified.")


    def do_filewrite(self, filename):
        """Writes (appends) to a file. Usage: filewrite amazingFileName.txt I'm writing to a file"""
        if filename:
            textToWrite = input("Enter text to be written to file:\n")
            if textToWrite:
                fileToOpen = open(filename, "a")
                fileToOpen.write(textToWrite)
                fileToOpen.close()
                print("Operation complete.")
            else:
                print("No text specified for writing to file.")
        else:
            print("No file specified or other error.")

    def do_fileoverwrite(self, filename):
        """Overwrites a file. Usage: fileoverwrite amazingFileName.txt Overwriting this file!!
        WARNING!! THIS WILL OVERWRITE ANY FILE IT HAS PERMISSIONS TO!! MAKE SURE YOU'RE CHOOSING THE CORRECT FILE!!"""
        if filename:
            textToWrite = input("Enter text to be written to file:\n")
            if textToWrite:
                fileToOpen = open(filename, "w")
                fileToOpen.write(textToWrite)
                fileToOpen.close()
                print("Operation complete.")
            else:
                print("No text specified for writing to file.")
        else:
            print("No file specified or other error.")

    def do_fileread(self, filename):
        """Reads from a file. Usage: fileread amazingFileName.txt"""
        if filename:
            fileToOpen = open(filename, "r")
            print(fileToOpen.read())
        else:
            print("No file specified or other error.")

    def do_telltime(self, time):
        """TEST COMMAND"""
        if time:
            print("Telling time...")
            print("Everything seems to be fine.")
        else:
            print("No time :(")

    def do_hashmd5(self, hashenc):
        """Hashes what you enter in MD5 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.md5(hashenc).hexdigest()  # Hashing in MD5 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_hashsha1(self, hashenc):
        """Hashes what you enter in SHA-1 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha1(hashenc).hexdigest()  # Hashing in SHA-1 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_hashsha256(self, hashenc):
        """Hashes what you enter in SHA-256 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha256(hashenc).hexdigest()  # Hashing in SHA-384 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_hashsha384(self, hashenc):
        """Hashes what you enter in SHA-384 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha384(hashenc).hexdigest()  # Hashing in SHA-384 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_hashsha512(self, hashenc):
        """Hashes what you enter in SHA-512 format. Usage: hashmd5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha512(hashenc).hexdigest()  # Hashing in SHA-512 and saving the result in hashResult
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

    def do_ver(self, none):  # Adding none was necessary for positional arguments reasons.
        """Prints the current version of SSPCI."""
        print("SSPCI Version 0.2-alpha-source")
        print("Made by NovaCow")

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
