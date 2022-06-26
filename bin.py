import glob
import os
import utils


class RecycleBin:

    def __init__(self, path):
        self.path = path

        if not self._recycle_bin_exists():
            self.create_bin_directories('')

    def check_file(self, filepath):
        filename = os.path.basename(filepath)
        path = os.path.dirname(filepath)
        file_path_in_bin = self._calculate_path_inside_bin(path)

        file_in_bin = glob.glob(os.path.join(file_path_in_bin, '*_%s' % filename))

        return len(file_in_bin) > 0

    def get_latest_file_version(self, filepath):
        filename = os.path.basename(filepath)
        filepath = os.path.dirname(filepath)
        binpath = self._calculate_path_inside_bin(filepath)

        regex = os.path.join(binpath, '*_%s' % filename)

        files = [os.path.basename(f) for f in glob.glob(regex)]
        versions = [int(f.split('_')[0]) for f in files]

        return 0 if len(versions) == 0 else max(versions)

    def delete(self, filepath):
        filepath = utils.get_abs_path(filepath)
        filename = os.path.basename(filepath)
        path = os.path.dirname(filepath)
        path_inside_bin = self._calculate_path_inside_bin(path)

        self._create_bin_directories(path)

        next_version = self.get_latest_file_version(filepath) + 1
        filename_inside_bin = '%d_%s' % (next_version, filename)

        os.rename(filepath, os.path.join(path_inside_bin, filename_inside_bin))

        return next_version

    def list(self, path):
        binpath = self._calculate_path_inside_bin(path)
        found_files = {}

        for f in os.listdir(binpath):
            if os.path.isfile(os.path.join(binpath, f)):
                filename = f[f.find('_')+1:]
                found_files[filename] = self.get_latest_file_version(os.path.join(path, filename))

        return found_files

    def undelete(self, filepath):
        path = os.path.dirname(filepath)
        file_path_in_bin = self._calculate_path_inside_bin(path)
        latest_version = self.get_latest_file_version(filepath)

        file_with_version = '%d_%s' % (latest_version, os.path.basename(filepath))
        file_in_bin_with_version = os.path.join(file_path_in_bin, file_with_version)

        os.rename(file_in_bin_with_version, filepath)

    def remove(self, filename):
        abs_path = os.path.abspath(filename)
        path = os.path.dirname(abs_path)
        check_if_file_exists = self.check_file(abs_path)
        if check_if_file_exists == False:
            raise ValueError('File doesnt exist')
        path_in_bin = self._calculate_path_inside_bin(path)
        latest_version = self.get_latest_file_version(abs_path)
        file_with_version = '%d_%s' % (latest_version, filename)
        file_in_bin_with_version = os.path.join(path_in_bin, file_with_version)

        os.remove(file_in_bin_with_version)

    def empty(self):
        path = self._calculate_path_inside_bin(os.getcwd())
        for filename in os.listdir(path):
            path_in_bin = os.path.join(path, filename)
            os.remove(path_in_bin)


    def _recycle_bin_exists(self):
        return os.path.exists(self.path)

    def _create_bin_directories(self, dirpath):
        binpath = self._calculate_path_inside_bin(dirpath)

        if not os.path.exists(binpath):
            os.makedirs(binpath)

    def _calculate_path_inside_bin(self, path):
        if path.startswith('/'):
            path = path[1:]

        return os.path.join(self.path, path)
