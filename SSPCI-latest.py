import cmd
import os
import platform
import hashlib  # This can fuck off honestly
import shutil


# Currently on Version 0.4.1-alpha
# This is the SSPCI, Super Simple Python Command Interpreter, made in... well... Python
# Should be supported on (almost) everything. As it uses common libraries.
# I should at some point add error handling. Because I don't have that currently.
# But I'm working on error handling now! :)
# I also need to put more comments everywhere, I barely use them.
class SSPCI(cmd.Cmd):
    intro = "This is the SSPCI Shell, type help or ? to list current supported commands.\n"
    prompt = "sspci> "
    file = None
    CurrDir = os.getcwd()
    print("SSPCI version 0.4.1-alpha running on " + platform.system() + " " + platform.release())
    if platform.system == "Linux":
        if os.access("/root", os.R_OK):  # Probably the most unusable, unnecessary way to check if we're running as root
            print("WARNING!! You might be running SSPCI as root! THIS CAN CAUSE IRREPARABLE DAMAGE!! USE AT YOUR OWN RISK!")
        else:
            pass
    elif platform.system == "Darwin":  # You think I have a Mac or something?!?
        print("You are running an unsupported operating system (Probably macOS). This should cause no harm, but if there are any bugs, I don't think I can help.")
    else:
        pass

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
                if os.access(listedDir, os.R_OK):  # Because for some reason there are permissions involved,
                    FilesInDir = os.listdir(listedDir)  # An issue with this method is that everything is printed on one
                    print(str(FilesInDir))  # line.  So if your directory is really full, your line can be very, very long
                    # But it works, and that's what matters.
                else:
                    print("Cannot list directory " + listedDir + ". Make sure you have permissions to access this directory.")
            else:
                print(listedDir + ": No such directory.")
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
                if os.access(directory, os.R_OK):  # Checks if we have access to a directory (Because sometimes we don't)
                    os.chdir(directory)  # Switching directories!
                    CurrDir = os.getcwd()  # I know it's ugly, but it sorta works.
                    print("Switched working directory to: " + CurrDir)
                else:
                    print("Cannot enter directory " + directory + ". Make sure you have permissions to access this directory.")
            else:
                print(directory + ": No such directory")

        else:
            CurrDir = os.getcwd()  # If no new directory was specified, we say what directory we're currently in.
            print("The current working directory is: " + CurrDir)

    def do_mkdir(self, directory):
        """
        Creates a directory. Type the whole location of the directory.
        On Windows: mkdir d:/example/example
        On Linux: mkdir /home/example/example
        """
        if directory:  # Still have no way of checking if the parent directory exists. Meh, I'll come around to it someday.
            os.mkdir(directory)
            print("Operation complete.")
        else:
            print("No directory specified.")

    def do_rmdir(self, directory):
        """Removes a directory. Type the whole location of the directory. Only works if directory is empty
        On Windows: rmdir d:/example/example
        On Linux: rmdir /home/example/example"""
        if directory:
            if os.path.isdir(directory):  # Checks if the directory the user entered does exist.
                os.rmdir(directory)  # And removes it if it does exist.
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
            if os.path.isdir(directory):  # Checks if the directory the user entered does exist.
                shutil.rmtree(directory)  # And creates it if it exists.
                print("Operation complete.")
            else:
                print("Directory doesn't exist or other error.")
        else:
            print("No directory specified.")

    def do_createfile(self, filename):
        """Creates a file in the working directory. Usage: createfile amazingFileName.txt"""
        if filename:
            fileToCreate = open(filename, "x")  # Creates a file using the open() function, the "x" stands for create.
            print("Operation complete.")
        else:
            print("No filename specified.")

    # If you did a contest to see what the most unreadable piece of code was,
    # I think this might win! Don't worry though, I'll add comments (to ease the pain).
    # It's like I want to deprecate all other ways of file handling!
    # I haven't added checks for permissions and whatever to the old clunky way of handling files (and probably won't). 

    def do_file(self, option):  # I HATE POSITIONAL ARGUMENTS!
        """Is the default command for file handling, has options as: read, write, create. Usage: file create.
           Still highly experimental, that's why the old options still remain."""
        if option:
            if option == "read":  # This is maybe the most ugliest code I've ever seen! And this is just the "read" option!
                filename = input("Enter location of the file to read:\n")
                if os.path.isfile(filename):
                    if os.access(filename, os.R_OK):  # I made a release version that didn't even work because of this.
                        fileToRead = open(filename, "r")
                        print(fileToRead.read())
                        fileToRead.close()
                    else:
                        print("You don't have permissions to access this file.")
                else:
                    print("No such file.")
            elif option == "write":
                filename = input("Enter location of the file to write to:\n")
                if os.path.isfile(filename):
                    if os.access(filename, os.W_OK):
                        textToWrite = input("Enter text to be written to file:\n")
                        if textToWrite:
                            fileToOpen = open(filename, "a")
                            fileToOpen.write(textToWrite)
                            fileToOpen.close()
                            print("Operation complete.")
                        else:
                            print("No text specified for writing to file.")
                    else:
                        print("You don't have the permissions to access this file.")
                else:
                    fileCreateQ = input("No such file. Do you want to create it? [y/n] ")
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
            elif option == "overwrite":
                filename = input("Enter location of the file to overwrite:\n")
                if os.path.isfile(filename):
                    if os.access(filename, os.W_OK):
                        textToWrite = input("Enter text to be written to file:\n")
                        if textToWrite:
                            fileToOpen = open(filename, "w")
                            fileToOpen.write(textToWrite)
                            fileToOpen.close()
                            print("Operation complete.")
                        else:
                            print("No text specified for writing to file.")
                    else:
                        print("No such file.")
            elif option == "create":
                filename = input("Enter name of the file to create:\n")
                if filename:
                    fileToCreate = open(filename, "x")
                    print("Operation complete.")
                else:
                    print("No filename specified.")
        else:
            print("No option specified.")


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
                fileCreateQ = input("No such file. Do you want to create it? [y/n] ")
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
                print("No such file.")
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
                print("No such file.")
        else:
            print("No source file specified.")

    # As if someone ever needs hashing.
    # And of all things does it with this garbage python code.
    # So removing is in order, although I will keep one algorithm.
    # So as to not lose the feature entirely.
    # I won't be updating it anymore though, so if anything breaks it, oh well.
    # But, if you use this program for hashing only, I'm sorry, but you're stupid.
    # There are business solutions, and it's even built-in the Linux terminal!
    # So, as update 0.5.0-alpha rolls around I will remove this garbage thing.
    # And yes, to make it harder to use, I've only implemented SHA-224 >:D

    def do_hash(self, hashenc):
        """Hashes what you enter in desired format. Usage: hash amazing-example"""
        if hashenc:
            hashenc = hashenc.encode()  # Encoding the string because otherwise the hasher doesn't work.
            hashResult = hashlib.sha224(hashenc).hexdigest()  # Hashing in SHA-224 and saving the result in hashResult
            print(hashResult)  # And then printing it, otherwise nothing would happen
        else:
            print("Nothing to hash.")

    def do_ver(self, none):  # Adding none was necessary for positional arguments reasons.
        """Prints the current version of SSPCI."""
        print("SSPCI Version 0.4.1-alpha")
        print("Made by NovaCow")

    def do_exit(self, none):  # Adding that none was necessary, I hate it.
        """
        Ends the current SSPCI session.
        """
        print("Ending current SSPCI Session...")
        print("Thank you for using SSPCI!")
        return True

    def do_end(self, none):  # Adding that none was necessary, I hate it. Should have deprecated this ages ago
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
