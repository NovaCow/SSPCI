import cmd
import os
import hashlib
import shutil

# Currently on Version 0.3.2-alpha-latest
# Based on release: f30cee8
# This is a "latest" release, therefore it's not very extremely stable and may be ridden with bugs.
# This is the SSPCI, Super Simple Python Command Interpreter, made in... well... Python
# Should be supported on (almost) everything. As it uses common libraries.
# I should at some point add error handling. Because I don't have that currently.
# But I'm working on error handling now! :)
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
            if os.path.isdir(listedDir):
                FilesInDir = os.listdir(listedDir)  # An issue with this method is that everything is printed on one
                print(str(FilesInDir))  # line.  So if your directory is really full, your line can be very, very long
                # But it works, and that's what matters.
            else:
                print("Directory doesn't exist.")
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
            if os.path.isdir(directory):
                os.chdir(directory)  # Switching directories!
                CurrDir = os.getcwd()  # I know it's ugly, but it sorta works.
                print("Switched working directory to: " + CurrDir)
            else:
                print("Cannot enter directory " + directory + ". Check if you spelled its name correctly.")

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
        """Removes a directory. Type the whole location of the directory. Only works if directory is empty
        On Windows: rmdir d:/example/example
        On Linux: rmdir /home/example/example"""
        if directory:
            if os.path.isdir(directory):
                os.rmdir(directory)
                print("Operation complete.")
            else:
                print("Directory doesn't exist or other error.")
        else:
            print("No directory specified.")

    def do_forcermdir(self, directory):
        """Removes a directory and all its content. Type the whole location of the directory.
        On Windows: rmdir d:/example/example
        On Linux: rmdir /home/example/example"""
        if directory:
            if os.path.isdir(directory):
                shutil.rmtree(directory)
                print("Operation complete.")
            else:
                print("Directory doesn't exist or other error.")
        else:
            print("No directory specified.")


    def do_createfile(self, filename):
        """Creates a file in the working directory. Usage: createfile amazingFileName.txt"""
        if filename:
            fileToCreate = open(filename, "x")
            print("Operation complete.")
        else:
            print("No filename specified.")


    def do_write(self, filename):
        """Writes (appends) to a file. Usage: write amazingFileName.txt I'm writing to a file"""
        if filename:
            if os.path.isfile(filename):
                textToWrite = input("Enter text to be written to file:\n")
                if textToWrite:
                    fileToOpen = open(filename, "a")
                    fileToOpen.write(textToWrite)
                    fileToOpen.close()
                    print("Operation complete.")
                else:
                    print("No text specified for writing to file.")
            else:
                fileCreateQ = input("File doesn't exist. Do you want to create it? [y/n] ")
                if fileCreateQ == "y":
                    fileToCreate = open(filename, "x")
                    textToWrite = input("Enter text to be written to file:\n")
                    if textToWrite:
                        fileToOpen = open(filename, "a")
                        fileToOpen.write(textToWrite)
                        fileToOpen.close()
                        print("Operation complete.")
                    else:
                        print("No text specified for writing to file.")
                elif fileCreateQ == "Y":
                    fileToCreate = open(filename, "x")
                    textToWrite = input("Enter text to be written to file:\n")
                    if textToWrite:
                        fileToOpen = open(filename, "a")
                        fileToOpen.write(textToWrite)
                        fileToOpen.close()
                        print("Operation complete.")
                    else:
                        print("No text specified for writing to file.")
                elif fileCreateQ == "n":
                    print("Aborted.")
                elif fileCreateQ == "N":
                    print("Aborted.")
                else:
                    print("No selection made, aborting...")


        else:
            print("No file specified or other error.")

    def do_overwrite(self, filename):
        """Overwrites a file. Usage: overwrite amazingFileName.txt Overwriting this file!!
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

    def do_read(self, filename):
        """Reads from a file. Usage: read amazingFileName.txt"""
        if filename:
            if os.path.isfile(filename):
                fileToOpen = open(filename, "r")
                print(fileToOpen.read())
            else:
                print("File doesn't exist.")
        else:
            print("No file specified or other error.")

    def do_copy(self, filename):
        """Copies a file. Usage: copy amazingFileName.txt"""
        if filename:
            if os.path.isfile(filename):
                desName = input("Where do you want to copy this file to?\n")
                shutil.copyfile(filename, desName)
                print("Operation complete.")
            else:
                print("Source file doesn't exist.")
        else:
            print("No source file specified.")

    def do_md5(self, hashenc):
        """Hashes what you enter in MD5 format. Usage: md5 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.md5(hashenc).hexdigest()  # Hashing in MD5 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_sha1(self, hashenc):
        """Hashes what you enter in SHA-1 format. Usage: sha1 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha1(hashenc).hexdigest()  # Hashing in SHA-1 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_sha256(self, hashenc):
        """Hashes what you enter in SHA-256 format. Usage: sha256 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha256(hashenc).hexdigest()  # Hashing in SHA-384 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_sha384(self, hashenc):
        """Hashes what you enter in SHA-384 format. Usage: sha384 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha384(hashenc).hexdigest()  # Hashing in SHA-384 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_sha512(self, hashenc):
        """Hashes what you enter in SHA-512 format. Usage: sha512 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha512(hashenc).hexdigest()  # Hashing in SHA-512 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_sha224(self, hashenc):
        """Hashes what you enter in SHA-224 format. Usage: sha224 amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha224(hashenc).hexdigest()  # Hashing in SHA-224 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_ver(self, none):  # Adding none was necessary for positional arguments reasons.
        """Prints the current version of SSPCI."""
        print("SSPCI Version 0.3.2-alpha-latest")
        print("Made by NovaCow")

    def do_exit(self, none):  # Adding that none was necessary, I hate it.
        """
        Ends the current SSPCI session.
        """
        print("Ending current SSPCI Session...")
        print("Thank you for using SSPCI!")
        return True

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
