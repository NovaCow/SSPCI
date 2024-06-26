import cmd
import os
import platform
import shutil
import importlib
from typing import List


# Currently on Version 0.6.0-unstable
# This is the SSPCI, Super Simple Python Command Interpreter, made in... well... Python
# Should be supported on (almost) everything. As it uses common libraries.
# I should at some point add error handling. Because I don't have that currently.
# But I'm working on error handling now! :)
# I also need to put more comments everywhere, I barely use them.
# I have a todo list that I want to complete before version 1.0.0:
# -Add scripting (Goal is before 0.8.0)
# -Add FTP support (Goal is before 0.7.0)
# -Add some kind of ping or http command [IN PROGRESS] (Goal is to finish before v0.5.2)
# -Somehow make a package manager. [IN PROGRESS] (Goal is to finish before v0.6.0)
# -Add support for running older versions within the shell. (Goal is before v0.7.0)
# Now I'm mimicking the Linux prompt. Or at least the one that comes with bash.
# Lots of pre-shell config.


class SSPCI(cmd.Cmd):
    global envi
    global enviVar
    global pkg
    splitWD = os.getcwd()
    cwd = splitWD.rsplit("/", 1)
    promptcwd = cwd[1]
    pkg = []
    intro = "This is the SSPCI Shell, type help or ? to list current supported commands.\n"
    prompt = "[sspci@" + platform.system() + " " + promptcwd + "]$ "
    file = None
    print("SSPCI version 0.6.0-unstable running on " + platform.system() + " " + platform.release())

    # The structure for the 'envi' variable is: OS/PATHTYPE. Examples: Linux/POSIX, Windows/WinNT
    # It mostly defines how SSPCI should handle paths and commands.
    # You can use a different OS, such as Haiku or FreeBSD, the structure would be:
    # Haiku/POSIX, FreeBSD/POSIX
    # Since I don't have either of those, I don't know if FreeBSD gets recognized as Linux.
    # I want to add native support for FreeBSD and other BSD-based systems. So I might discard Linux and switch to Unix-like.
    if platform.system() == "Linux":
        if os.access("/root", os.R_OK):  # Probably the most unusable, unnecessary way to check if we're running as root.
            print("WARNING!! You might be running SSPCI as root! THIS CAN CAUSE IRREPARABLE DAMAGE!! USE AT YOUR OWN RISK!")
        envi = "Linux/POSIX"
    elif platform.system() == "Darwin":
        print("You are running an unsupported operating system (Probably macOS). This should cause no harm.")
        envi = "Darwin/POSIX"
    elif platform.system() == "Windows":
        envi = "Windows/WinNT"
        pass
    else:
        envi = "Unknown/UNKNOWN"
        print("SSPCI couldn't determine what type of system you are using.")
        enviCheck = input("Please enter pathtype: (WinNT (Windows NT), POSIX (Linux, UNIX), POSIX-MAC (macOS), POSIX-BSD (BSD-Based systems)) ")
        if enviCheck == "POSIX":
            envi = "Linux/POSIX"
        elif enviCheck == "POSIX-MAC":
            envi = "Darwin/POSIX"
        elif enviCheck == "WinNT":
            envi = "Windows/WinNT"
        else:
            print("SSPCI couldn't determine what type of system you are using.")
            print("Fatal error! E00, SSPCI failed to determine type of system!")
            ErrIgnore = input("If you're ABSOLUTELY sure you can run SSPCI, type continue to continue or press enter to exit. ")
            if ErrIgnore == "continue":
                envi = input("Input environment like such: Linux/POSIX (OS/PATHTYPE): ")
            else:
                exit()

    enviVar = envi.split("/", -1)

    print("The current working directory is: " + os.getcwd())

    def do_echo(self, echo):  # TODO: Think if I need this.
        """
        A command that echoes what you input.
        """
        if echo:
            print(echo)  # Who would in their right mind use this?!?  # Once scripting comes it's pretty handy.
        else:
            print(" ")

    def do_ls(self, listedDir):  # It's like dir, but with a different name.
        """Lists current files in the entered directory.
        On Windows: ls d:/example/example
        On Linux: ls /home/example/example"""
        if listedDir:
            if os.path.isdir(listedDir):
                if os.access(listedDir, os.R_OK):  # An ugly way to check for perms,os.R_OK stands for Read_OK
                    FilesInDir = os.listdir(listedDir)  # An issue with this method is that everything is printed on one
                    print(str(FilesInDir))  # line.  So if your directory is really full, your line can be very, very long
                    # But it works, and that's what matters.
                else:
                    print("Cannot list directory " + listedDir + ". Make sure you have permissions to access this directory.")
            else:
                print(listedDir + ": No such directory.")
        else:
            FilesInDir = os.listdir(os.getcwd())  # Now if you don't enter a directory you don't get an error!
            print(str(FilesInDir))  # But the same issue persists as with a directory.
            # But it works, and that's what matters.

    def do_synk(self, package):
        """A package manager, somehow. Usage: synk -I <package>. For help: synk -? or --help"""
        #pkg = []  # Only here to test, won't be here in main release of 0.6.0
        global pkg
        listOption = package.split(" ", -1)
        try:
            pkg
        except UnboundLocalError:
            print("Fatal error! synk can't access variable for storing package! Aborting any action!")
            print("Exact error: SSPCI.module.synk encountered an UnboundLocalError for variable pkg.")
            return False
        except NameError:
            print("Fatal error! synk can't access variable for storing package! Aborting any action!")
            print("Exact error: SSPCI.module.synk encountered a NameError for variable pkg.")
            return False
        except:
            print("Fatal error! An unknown error occurred accessing variable for storing packages! Aborting any action!")
            print("No exact error information found.")
            return False
        if listOption[0] == "-I":
            if 2 > len(listOption):
                print("synk version 0.0.2")
                print("No package specified. Try synk --help for help")
            elif 2 < len(listOption):
                print("synk version 0.0.2")
                print("Too many targets specified. Try synk --help for help.")
            else:
                print("synk version 0.0.2")
                print("As of now synk can only import Python libraries.")
                if len("a") == 3:
                    #print("Cannot install more than 3 packages. Cannot continue.")
                    pass
                else:
                    #pkg.append(importlib.import_module(listOption[1]))  # Meant for testing.
                    try:
                        print("Installing package " + listOption[1] + "...")
                        pkg.append(importlib.import_module(listOption[1]))
                        print("Installation successful!")
                    except ModuleNotFoundError:
                        print("Installation failed. Package " + str(listOption[1]) + " doesn't exist.")
                    except UnboundLocalError:
                        print("Installation failed. Can't save package to non-existent location.")
                        print("Warning! This error may mean Python can't access the variable used to store packages!")
                        print("Please file a bug report if this error continues to happen, even after a reboot.")
                    except:
                        print("An unknown error occurred. Please try again.")
        elif listOption[0] == "-L":
            print("You have installed " + str(len(pkg)) + " package(s) via synk")
        elif listOption[0] == "-R":
            print("WARNING! This will remove ALL packages!")
            confirm = input("Do you wish to continue? [y/n] ")
            while confirm != "y" and confirm != "Y" and confirm != "n" and confirm != "N":
                print("Invalid answer. Try again.")
                confirm = input("Do you wish to continue? [y/n] ")
            if confirm == "y" or confirm == "Y":
                pkg = []
            else:
                print("Aborted.")


    def do_synklist(self, none):
        """Prints the amount of packages installed via synk. Usage: synklist"""
        global pkg
        print("You have installed " + str(len(pkg)) + " package(s) via synk")

    def do_test(self, module):  # Was a proof-of-concept. Will be removed before release.
        """Allows you to test an installed module via synk. Usage: test random"""
        global pkg
        if module == "random":
            pkgList = input("Where is package 'random' stored? ")
            pkgList = int(pkgList)
            if pkgList == 2:
                try:
                    a = pkg[2].randint(0,10)
                    print(a)
                    print("Module random tested successfully")
                except IndexError:
                    print("No package in place 2! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            elif pkgList == 1:
                try:
                    a = pkg[1].randint(0,10)
                    print(a)
                    print("Module random tested successfully")
                except IndexError:
                    print("No package in place 1! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            elif pkgList == 0:
                try:
                    a = pkg[0].randint(0,10)
                    print(a)
                    print("Module random tested successfully")
                except IndexError:
                    print("No package in place 0! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            else:
                pass
        elif module == "math":
            pkgList = input("Where is package 'math' stored? ")
            pkgList = int(pkgList)
            if pkgList == 2:
                try:
                    a = pkg[2].sqrt(10)
                    print(a)
                    print("Module math tested successfully")
                except IndexError:
                    print("No package in place 2! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            elif pkgList == 1:
                try:
                    a = pkg[1].sqrt(10)
                    print(a)
                    print("Module math tested successfully")
                except IndexError:
                    print("No package in place 1! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            elif pkgList == 0:
                try:
                    a = pkg[0].sqrt(10)
                    print(a)
                    print("Module math tested successfully")
                except IndexError:
                    print("No package in place 0! Please install a package with synk!")
                except:
                    print("Cannot verify module integrity, please install with synk -I random")
            else:
                pass
        else:
            pass
    def do_dir(self, listedDir):  # The same as ls, but for Windows users.
        """Lists current files in the entered directory.
        On Windows: dir d:/example/example
        On Linux: dir /home/example/example"""
        if listedDir:
            if os.path.isdir(listedDir):
                if os.access(listedDir, os.R_OK):  # An ugly way to check for perms, os.R_OK stands for Read_OK
                    FilesInDir = os.listdir(listedDir)  # An issue with this method is that everything is printed on one
                    print(str(FilesInDir))  # line.  So if your directory is really full, your line can be very, very long
                    # But it works, and that's what matters.
                else:
                    print("Cannot list directory " + listedDir + ". Make sure you have permissions to access this directory.")
            else:
                print(listedDir + ": No such directory.")
        else:
            FilesInDir = os.listdir(os.getcwd())  # Now if you don't enter a directory you don't get an error!
            print(str(FilesInDir))  # But the same issue persists as with a directory.
            # But it works, and that's what matters.

    def do_cd(self, directory):
        """Navigates to a certain directory. Type the whole location of the directory
        On Windows: cd d:/example/example
        On Linux: cd /home/example/example"""
        if directory:
            if os.path.isdir(directory):
                if os.access(directory, os.R_OK):  # Checks if we have access to a directory
                    os.chdir(directory)  # Switching directories!
                    print("Switched working directory to: " + os.getcwd())  # Way nicer now!
                    splitWD = os.getcwd()
                    if os.getcwd() == "/":  # An easy way to avoid checking indexes
                        SSPCI.prompt = "[sspci@" + platform.system() + " " + os.getcwd() + "]$ "
                    elif os.getcwd() == "C:\\" or os.getcwd() == "\\":  # Although I haven't really thought of Windows users.
                        SSPCI.prompt = "[sspci@" + platform.system() + " " + os.getcwd() + "]$ "
                    else:
                        cwd = splitWD.rsplit("/", 1)
                        SSPCI.prompt = "[sspci@" + platform.system() + " " + cwd[1] + "]$ "
                else:
                    print("Cannot enter directory " + directory + ". Make sure you have permissions to access this directory.")
            else:
                print(directory + ": No such directory")

        else:  # If no new directory was specified, we say what directory we're currently in.
            print("The current working directory is: " + os.getcwd())

    def do_mkdir(self, directory):
        """Creates a directory. Type the whole location of the directory.
        On Windows: mkdir d:/example/example
        On Linux: mkdir /home/example/example
        """
        if directory:
            splitDir = directory.rsplit("/", 1)
            if os.path.isdir(splitDir[0]):
                if os.access(splitDir[0], os.X_OK):
                    os.mkdir(directory)
                    print("Operation complete.")
                else:
                    print("Insufficient permissions to create directory at location.")
            else:
                print("Parent directory doesn't exist.")
        else:
            print("No directory specified.")

    def do_rmdir(self, directory):
        """Removes a directory. Only works if directory is empty
        On Windows: rmdir d:/example/example
        On Linux: rmdir /home/example/example"""
        if os.path.isdir(directory):  # Checks if the directory the user entered does exist.
            if os.access(directory, os.W_OK):
                if len(os.listdir(directory)) == 0:
                    os.rmdir(directory)  # And removes it if it does exist.
                    print("Operation complete.")
                else:
                    DelTree = input("Directory is not empty, do you want to delete it anyway? [y/n] ")
                    if DelTree == "Y" or DelTree == "y" or DelTree == "N" or DelTree == "n":  # I can't get a while to work
                        answerCorrect = True
                    else:
                        answerCorrect = False
                    while answerCorrect is False:
                        DelTree = input("Directory is not empty, do you want to delete it anyway? [y/n] ")  # So I've stopped caring.
                        if DelTree == "Y" or DelTree == "y" or DelTree == "N" or DelTree == "n":
                            answerCorrect = True
                        else:
                            answerCorrect = False
                    if DelTree == "y" or DelTree == "Y":
                        shutil.rmtree(directory)
                        print("Operation complete.")
                    else:
                        print("Aborted.")
            else:
                print("Insufficient permissions to remove directory.")
        else:
            print("Directory doesn't exist or other error.")

    def do_createfile(self, filename):
        """Creates a file in the working directory. Usage: createfile amazingFileName.txt"""
        if filename:
            fileToCreate = open(filename, "x")  # Creates a file using the open() function, the "x" stands for create.
            print("Operation complete.")
        else:
            print("Usage: createfile filename.txt")

    def do_clear(self, none):
        """Clears the screen"""
        if enviVar[1] == "POSIX":
            os.system("clear")
        elif enviVar[1] == "WinNT":
            os.system("cls")
        else:
            print("SSPCI couldn't determine what type of system you are using.")
            clearCmd = input("Please enter system type: (WinNT (Windows NT), UNIX (Linux, UNIX and macOS)) ")
            if clearCmd == "UNIX":
                os.system("clear")
            elif clearCmd == "WinNT":
                os.system("cls")
            else:
                print("SSPCI couldn't determine what type of system you are using.")
                SelfCmd = input("Enter command to clear terminal window: ")
                os.system(str(SelfCmd))

    def do_bash(self, cmd):  # For some reason Python defaults to sh and not bash. Annoying.
        """Tries to start bash if installed. Usage: bash <cmd>. If you want to start a bash terminal, type bash start."""
        if enviVar[0] != "Linux" and enviVar[0] != "Darwin":  # Does macOS have bash?
            print("You don't seem to be running Linux or macOS, bash might therefore not be installed.")
            print("Falling back to standard python command interpreter.")
            if cmd:
                os.system(str(cmd))  # str() is for if any goofball decides to pass an int.
            else:
                cmd = input("Enter command to pass to your command interpreter: ")
                os.system(str(cmd))
        elif os.path.isfile("/bin/bash"):
            if cmd:
                if cmd == "start" or cmd == "START":
                    print("You are now being dropped in a bash shell, type exit to exit.")
                    os.system("bash")
                else:
                    os.system(str(cmd))  # str() is for if any goofball decides to pass an int.
            else:
                cmd = input("Enter command to pass to bash: ")
                os.system(str(cmd))
        else:
            print("Can't find bash on this system.")
            print("Falling back to standard python command interpreter.")
            if cmd:
                os.system(str(cmd))  # str() is for if any goofball decides to pass an int.
            else:
                cmd = input("Enter command to pass to your command interpreter: ")
                os.system(str(cmd))

    def do_sysinfo(self, debug):
        """Prints info about the system"""
        uname = platform.uname()
        if platform.processor() == "":
            print("Unable to get processor information.")
            processor = "Unable to get processor information."
        else:
            processor = platform.processor()
        print("You are running SSPCI version 0.6.0 on Python " + platform.python_version())
        print("OS: " + platform.system() + " " + platform.release())
        print("Pathtype: " + str(enviVar[1]))
        print("SEV: " + str(envi))
        print(f"Architechure: {uname.machine}")
        print("Processor: " + processor)
        print("Working directory: " + os.getcwd())
        if platform.system() == "Linux" or platform.system() == "Darwin":
            if os.access("/root", os.R_OK):
                print("Root: TRUE")
            else:
                print("Root: FALSE")
        else:
            pass

    def do_ping(self, ip):
        """Pings an IP-address. Usage: ping 192.168.178.1"""
        os.system("ping " + str(ip))  # A very lazy way to ping.

    # If you did a contest to see what the most unreadable piece of code was,
    # I think this might win! Don't worry though, I'll add comments (to ease the pain). (I'm coping holy hell.)
    # I haven't added checks for permissions and whatever to the old clunky way of handling files (and probably won't).
    # Reusablity, readability, portability?? What's that??

    def do_file(self, option):
        """Is the default command for file handling, has options as: read, write, create. Usage: file -?.
           Still highly experimental, that's why the old options still remain."""
        if option:
            splitOption = option.split(" ", -1)
            if splitOption[0] == "-r" or splitOption[0] == "--read":
                if 1 < len(splitOption):  # No more index out of range errors!
                    filename = str(splitOption[1])
                    if os.path.isfile(filename):  # Checks if the file even exists.
                        if os.access(filename, os.R_OK):
                            fileToRead = open(filename, "r")  # Reads from the file.
                            print(fileToRead.read())
                            fileToRead.close()
                        else:
                            print("You don't have permissions to access this file.")
                    else:
                        print("No such file.")
                else:
                    print("No file specified.")
            elif splitOption[0] == "-w" or splitOption[0] == "--write":
                filename = str(splitOption[1])
                if os.path.isfile(filename):
                    if os.access(filename, os.W_OK):
                        textToWrite = input("Enter text to be written to file:\n")  # TODO: Make this part of the main command.
                        if textToWrite:
                            fileToOpen = open(filename, "a")
                            fileToOpen.write(textToWrite)
                            fileToOpen.close()
                            print("Operation complete.")
                        else:
                            print("No text specified for writing to file.")
                    else:
                        print("You don't have the permissions to access this file.")
                else:  # TODO: Add permissions to this garbage code.
                    fileCreateQ = input("No such file. Do you want to create it? [y/n] ")
                    if fileCreateQ == "y" or fileCreateQ == "Y":
                        fileToCreate = open(filename, "x")
                        textToWrite = input("Enter text to be written to file:\n")
                        if textToWrite:
                            fileToOpen = open(filename, "a")
                            fileToOpen.write(textToWrite)
                            fileToOpen.close()
                            print("Operation complete.")
                        else:
                            print("No text specified for writing to file.")
                    elif fileCreateQ == "n" or fileCreateQ == "N":
                        print("Aborted.")
                    else:
                        print("No selection made, aborting...")  # TODO: Should allow to try again though.
            elif splitOption[0] == "-W" or splitOption[0] == "--overwrite":
                filename = str(splitOption[1])
                if os.path.isfile(filename):
                    if os.access(filename, os.W_OK):
                        textToWrite = input("Enter text to be written to file:\n")  # TODO: Again, make this part of the main command.
                        if textToWrite:
                            fileToOpen = open(filename, "w")
                            fileToOpen.write(textToWrite)
                            fileToOpen.close()
                            print("Operation complete.")
                        else:
                            print("No text specified for writing to file.")
                    else:
                        print("Insufficient permissions to access file.")
                else:
                    print("No such file.")
            elif splitOption[0] == "--create" or splitOption[0] == "-c":
                filename = str(splitOption[1])
                if filename:
                    splitFilename = filename.rsplit("/", 1)
                    if 1 < len(splitFilename):  # No more random errors!
                        if os.access(str(splitFilename[0]), os.W_OK):
                            fileToCreate = open(filename, "x")
                            fileToCreate.close()
                            print("Operation complete.")
                        else:
                            print("Cannot access " + str(splitFilename[0]) + " due to insufficient permissions.")
                    else:
                        fileToCreate = open(filename, "x")
                        fileToCreate.close()
                        print("Operation complete.")
                else:
                    print("No filename specified.")
            elif splitOption[0] == "-?" or splitOption[0] == "--help":
                print("Usage: file -c amazingFile.txt")
                print("Parameters are:\n-c or --create: creates a file\n-w or --write: Writes to a file")
                print("-W or --overwrite: Overwrites a file\n-r or --read: Reads from a file")
                print("-cp or --copy: Copies a file")
                print("For -cp or --copy usage is different. You must select a source file and destination file.")
                print("To do this, usage is: file --copy amazingFile.txt /home/example/exampleFolder/exampleDocument.txt")
            elif splitOption[0] == "-cp" or splitOption[0] == "--copy":
                filename = str(splitOption[1])
                desName = str(splitOption[2])
                splitDesName = desName.rsplit("/", 1)
                if os.path.isfile(filename):
                    if os.access(filename, os.R_OK):
                        if os.access(splitDesName[0], os.W_OK):
                            shutil.copy(filename, desName)
                            print("Operation complete.")
                        else:  # else else else else else else
                            print("Insufficient permissions to write to destination file or file might not exist.")
                    else:
                        print("Insufficient permissions to access source file.")
                else:
                    print("No such file.")
            else:
                print(splitOption[0] +  ": incorrect parameter")
                print("Usage: file -c amazingFile.txt")
                print("Parameters are:\n-c or --create: creates a file\n-w or --write: Writes to a file")
                print("-W or --overwrite: Overwrites a file\n-r or --read: Reads from a file")
                print("-cp or --copy: Copies a file")
                print("For -cp or --copy usage is different. You must select a source file and destination file.")
                print("To do this, usage is: file --copy amazingFile.txt /home/example/exampleFolder/exampleDocument.txt")
        else:
            print("Usage: file -c amazingFile.txt")
            print("Parameters are:\n-c or --create: creates a file\n-w or --write: Writes to a file")
            print("-W or --overwrite: Overwrites a file\n-r or --read: Reads from a file")
            print("-cp or --copy: Copies a file")
            print("For -cp or --copy usage is different. You must select a source file and destination file.")
            print("To do this, usage is: file --copy amazingFile.txt /home/example/exampleFolder/exampleDocument.txt")



    # TODO: Maybe update this garbage?!? Meh, don't feel like it.
    def do_write(self, filename):  # The same as file -w, but for reasons it's still here.
        """Writes (appends) to a file. Usage: write amazingFileName.txt"""
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
                    open(filename, "x")
                    textToWrite = input("Enter text to be written to file:\n")
                    if textToWrite:
                        fileToOpen = open(filename, "a")
                        fileToOpen.write(textToWrite)
                        fileToOpen.close()
                        print("Operation complete.")
                    else:
                        print("No text specified for writing to file.")
                elif fileCreateQ == "Y":
                    open(filename, "x")
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
            print("Usage: write amazingFile.txt")

    def do_scl(self, param):
        split_param = param.split(" ", -1)
        profilename = split_param[1]


    def do_xtnd(self, extension):
        """Extension manager for SSPCI, not the same as synk, although xtnd will be implemented in synk later"""



    def do_overwrite(self, filename):
        """Overwrites a file. Usage: overwrite amazingFileName.txt
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
            print("Usage overwrite filename.txt")

    def do_read(self, filename):
        """Reads from a file. Usage: read amazingFileName.txt"""
        if filename:
            if os.path.isfile(filename):
                fileToOpen = open(filename, "r")
                print(fileToOpen.read())
            else:
                print("No such file.")
        else:
            print("Usage: read wow cool")  # TODO: What the fuck is this example file?!?

    def do_copy(self, filename):  # It copies a file.
        """Copies a file. Usage: copy amazingFileName.txt"""
        if filename:
            if os.path.isfile(filename):
                desName = input("Where do you want to copy this file to?\n")
                shutil.copyfile(filename, desName)
                print("Operation complete.")
            else:
                print("No such file.")
        else:
            print("No source file specified.")  # TODO: Completely unnecessary.

    def do_ver(self, none):  # It prints whatever version you're running.
        """Prints the current version of SSPCI."""
        print("SSPCI Version 0.6.0-unstable")
        print("Made by NovaCow")

    def do_exit(self, none):  # It ends, what more do you want?
        """
        Ends the current SSPCI session.
        """
        print("Ending current SSPCI Session...")
        print("Thank you for using SSPCI!")
        return True

    def do_end(self, none):  # Two (2) methods of ending, amazing.
        """
        Ends the current SSPCI session.
        """
        print("Ending current SSPCI Session...")
        print("Thank you for using SSPCI!")
        return True

    def postloop(self):  # The postloop, it does nothing but the moment it's removed nothing works.
        pass


if __name__ == '__main__':
    SSPCI().cmdloop()
