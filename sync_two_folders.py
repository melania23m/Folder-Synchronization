import os
import filecmp
import shutil
import threading
import time


class Sync:
    """ This class represents a synchronization object """

    def __init__(self, name=''):
        self.name = name
        self.directory_list = []
        self.file_copied_count = 0
        self.folder_copied_count = 0
        self.file_remove_count = 0
        self.folder_removed_count = 0

    def add_directory(self, director):
        self.directory_list.append(director)

    def compare_directory(self):

        """ This method takes the directors in the directory_list and compares them """

        for director in self.directory_list:

            if self.directory_list.index(director) < len(self.directory_list) - 1:
                director2 = self.directory_list[self.directory_list.index(director) + 1]
                print('\nComparing Souce Directory and Replica Directory :')

                self.comparing_directories(director.root_path, director2.root_path)

    def comparing_directories(self, left, right):
        """ This method compares directories. If there is a common directory, the
            algorithm must compare what is inside of the directory by calling this
            recursively.
        """
        comparison = filecmp.dircmp(left, right)
        if comparison.common_dirs:
            for d in comparison.common_dirs:
                self.comparing_directories(os.path.join(left, d), os.path.join(right, d))
        if comparison.left_only:
            self.copy_files(comparison.left_only, left, right)
        if comparison.right_only:
            self.remove_files(comparison.right_only, right, left)
        left_newer = []
        if comparison.diff_files:
            for d in comparison.diff_files:
                l_modified = os.stat(os.path.join(left, d)).st_mtime
                r_modified = os.stat(os.path.join(right, d)).st_mtime
                if l_modified > r_modified:
                    left_newer.append(d)
        self.copy_files(left_newer, left, right)

    def copy_files(self, file_list, src, dest):

        """ This method copies a list of files from a source node to a destination node """

        for f in file_list:
            source = os.path.join(src, os.path.basename(f))
            if os.path.isdir(source):
                shutil.copytree(source, os.path.join(dest, os.path.basename(f)))
                self.folder_copied_count = self.folder_copied_count + 1
                print('Copied directory \"' + os.path.basename(source) + '\" from \"' + os.path.dirname(
                    source) + '\" to \"' + dest + '\"')
            else:
                shutil.copy2(source, dest)
                self.file_copied_count = self.file_copied_count + 1
                print('Copied \"' + os.path.basename(source) + '\" from \"' + os.path.dirname(
                    source) + '\" to \"' + dest + '\"')

    def remove_files(self, file_list, src, dest):

        """ This method removes a list of files from a source node to a destination node """

        for f in file_list:
            source = os.path.join(src, os.path.basename(f))
            if os.path.isdir(source):
                os.rmdir(source)
                self.folder_removed_count = self.folder_removed_count + 1
                print('Removed directory \"' + os.path.basename(source) + '\" from \"' + os.path.dirname(
                    source) + '\" to \"' + dest + '\"')
            else:
                os.remove(source)
                self.file_remove_count = self.file_remove_count + 1
                print('Removed \"' + os.path.basename(source) + '\" from \"' + os.path.dirname(
                    source) + '\" to \"' + dest + '\"')


class Director:

    def __init__(self, path, name=''):
        self.name = name
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)


def foo():
    print(time.ctime())
    if __name__ == "__main__":
        my_sync = Sync('aaron')
        director1 = Director('SourceDirectory', 'node1')
        director2 = Director('ReplicaDirectory', 'node2')
        my_sync.add_directory(director1)
        my_sync.add_directory(director2)
        my_sync.compare_directory()
        print('Total files copied ' + str(my_sync.file_copied_count))
        print('Total folders copied ' + str(my_sync.folder_copied_count))
        print('Total files removed ' + str(my_sync.file_remove_count))
        print('Total folders removed ' + str(my_sync.folder_removed_count))


WAIT_TIME_SECONDS = 60

ticker = threading.Event()
while not ticker.wait(WAIT_TIME_SECONDS):
    foo()
