import filecmp
import sys
import os
import shutil
import datetime
import time

def listdirs(rootdir):          #this function is used to extract all paths of the subdirectories
    list_of_directories = []
    for file in os.listdir(rootdir):
        d = rootdir + "\\" + file
        if os.path.isdir(d):
            list_of_directories.append(d)
            list_of_directories.extend(listdirs(d))
    return list_of_directories

def check_deleted(dir_backup, dir_src, back,log_path): #check which files or folders are in the backup directory and are not in the main directory, and delete them
    for i in range(len(dir_backup)):
        if not dir_backup[i] in dir_src:
            path = back+ "\\" + dir_backup[i]
            if os.path.isfile(path):
                os.remove(path)
                ct = datetime.datetime.now()
                msj = str(ct) + ":" + str(path) + " was deleted"
                f = open(log_path, "a")
                f.write(msj)
                f.write("\n")
                f.close()
                print(msj)
            else:
                shutil.rmtree(path)
                ct = datetime.datetime.now()
                msj = str(ct) + ":" + str(path) + " was deleted"
                f = open(log_path, "a",)
                f.write(msj)
                f.write("\n")
                f.close()
                print(msj)

def check_content(dir_backup,dir_src,source,back,log_path ):
    backup_directories = []
    for i in range(len(dir_src)):
        #print(dir_src[i])
        #print(dir_backup)
        if dir_src[i] not in dir_backup:          #check which files or folders are in the main directory and are not in the backup directory and add them to the backup
            full_src = source + "\\" + dir_src[i]
            path = back + "\\" + dir_src[i]
            if os.path.isfile(full_src):
                shutil.copy(full_src, back)
                ct = datetime.datetime.now()
                msj = str(ct) + ":" + str(path) + " was added"
                f = open(log_path, "a")
                f.write(msj)
                f.write("\n")
                f.close()
                print(msj)
            else:
                os.mkdir(path)
                shutil.copytree(full_src, path,dirs_exist_ok=True)
                backup_directories.append(full_src)
                ct = datetime.datetime.now()
                msj = str(ct) + ":" + str(path) + " was added"
                f = open(log_path, "a")
                f.write(msj)
                f.write("\n")
                f.close()
                print(msj)
        else:
                full_src = source + "\\" + dir_src[i]   #if the file is present in both directories, it will check the source variant and backup variant, and if they are different, will copy from source to backup
                if not full_src in backup_directories:
                    path = back + "\\" + dir_src[i]
                    if os.path.isfile(full_src):
                        #print("##############")
                        if filecmp.cmp(full_src, path) == False:
                            os.remove(path)
                            shutil.copy(full_src, back)
                            ct = datetime.datetime.now()
                            msj = str(ct) + ":" + str(path) + " was updated"
                            f = open(log_path, "a")
                            f.write(msj)
                            f.write("\n")
                            f.close()
                            print(msj)

while True:

    src = sys.argv[1]
    backup = sys.argv[2]
    timer = float(sys.argv[3])
    file_log_path = sys.argv[4]
    backup_files = os.listdir(backup)

    if len(backup_files) == 0: #check if backup file is empty, and if it is, copy entire source folder

        shutil.copytree(src, backup, dirs_exist_ok=True)

    else:

        all_paths = listdirs(src)
        all_paths.insert(0, src) #add maine path to the list of subdirectories
        #print(all_paths)

        for i in range(len(all_paths)):
            src_path = all_paths[i]
            dir_list_src = [file for file in os.listdir(src_path) if not file.startswith('.')] #extract name of files without hidden files
            var = src_path.replace(src, "")
            new_backup = backup+var
            dir_list_backup = [file for file in os.listdir(new_backup) if not file.startswith('.')]

            check_deleted(dir_list_backup,dir_list_src,new_backup,file_log_path)
            check_content(dir_list_backup,dir_list_src,src_path,new_backup,file_log_path)

    time.sleep(timer * 60)

#send argumetns in order: py main.py source_path backup_path time_minutes log_file_path (create the backup directory before run the script)
