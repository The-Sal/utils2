"""
    Allows manipulating paths.
    Access to custom objects such as Container, Path, etc...
    More universal functions for removing, copying, etc... of files and directories.
"""
import os
import random
import shutil
from os import path as _path


def _decoder(string_path: str) -> str:
    """Decodes \ encoded strings from CLI"""
    if string_path.startswith('~'):
        string_path = join(os.path.expanduser('~'), string_path.split('~', 1)[1])

    if not string_path.__contains__('\\'):
        return string_path

    string_path = string_path.replace('\\', '')

    if os.path.exists(string_path):
        if not string_path.startswith('/'):
            string_path = _path.join(os.getcwd(), string_path)
        elif string_path.startswith('.'):
            string_path = _path.join(os.getcwd(), string_path.split('.', 1)[1])

        return string_path

    return string_path


def join(*args, absolute=True):
    """Join paths. Supports relative and absolute paths. OSX support only."""
    completePath = str()
    for arg in args:
        if arg.startswith('/'):
            completePath += arg
        else:
            completePath = _path.join(completePath, arg)
    if absolute:
        completePath = _path.abspath(completePath)

    return completePath


def isAbsolute(path):
    """Check if path is absolute."""
    return path.startswith('/')


def isRelative(path):
    """Check if path is relative."""
    return not isAbsolute(path)


def isFile(path):
    """Check if path is a file."""
    return _path.isfile(path)


def isDir(path):
    """Check if path is a directory."""
    return _path.isdir(path)


def fileExists(path):
    """Check if file exists."""
    return _path.exists(path)


def fileExtension(path):
    """Return file type."""
    return _path.splitext(path)[1]


def fileName(path):
    """Return file name from a path."""
    return _path.basename(path)


def fileNameWithoutExtension(path):
    """Return file name without extension."""
    return _path.splitext(path)[0]


def dirName(path):
    """Return directory name."""
    return _path.dirname(path)


def copy(src, dst, *args, **kwargs):
    """Copy a file or directory."""
    if isDir(src):
        if dst.endswith('/'):
            dst = dst + dirName(src)
        elif not dst.endswith('/'):
            dst = dst + '/' + dirName(src)
        return shutil.copytree(src=src, dst=dst, *args, **kwargs)
    else:
        return shutil.copy(src=src, dst=dst, *args, **kwargs)


def remove(path):
    """Remove a file or directory."""
    if isDir(path):
        return shutil.rmtree(path)
    else:
        return os.remove(path)


class Path:
    def __init__(self, path):
        # The path attribute shouldn't be modified ever!
        self._path = join(_decoder(path), absolute=True)
        self.cwd = None

    def append(self, path2):
        """Appends a path, and returns the new path in the form on a path Object"""
        return Path(join(self._path, path2))


    def base(self) -> str:
        """Returns the base path."""
        lastPart = fileName(self._path)
        return Path(self._path.split(lastPart)[0]).path

    def exists(self):
        return fileExists(self._path)


    def files(self, absolute=False) -> list:
        """Lists all files in directory, to a relative path unless absolute is True"""
        if not absolute:
            return os.listdir(self._path)
        else:
            absPaths = []
            for file in os.listdir(self._path):
                absPaths.append(self.append(file).path)

            return absPaths


    def rename(self, name):
        os.rename(src=self._path, dst=join(self.base(), name))

    # @pathsExceptionWrapper
    def addFile(self, filePath):
        """src is filePath and dst is the path set at initialisation"""
        if isinstance(filePath, Path):
            filePath = filePath.path

        if isDir(self._path):
            copy(src=filePath, dst=self._path)
        else:
            raise IsADirectoryError('Invalid init path')

    # Properties

    @property
    def fileName(self) -> str:
        """file name + extension"""
        return fileName(self._path)

    @property
    def extension(self):
        """file extension"""
        return fileExtension(self._path)

    @property
    def path(self):
        """Returns absolute path."""
        return self._path

    # internal attributes

    def __enter__(self):
        """Change directory into the folder"""
        self.cwd = os.getcwd()
        os.chdir(self._path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Change back to the cwd after contex exits"""
        os.chdir(self.cwd)

    def __bool__(self):
        return self.exists()

    def __str__(self):
        return self._path

    def __len__(self):
        return len(self.files())

    def __iter__(self):
        return iter(self.files())

    def __add__(self, other):
        if isDir(self._path):
            if isinstance(other, Path):
                self.addFile(filePath=other.path)
            else:
                raise TypeError('Invalid type, Expected Path')
        else:
            raise IsADirectoryError('Invalid init path')

    def __sub__(self, other):
        if isDir(self.path):
            if isinstance(other, Path):
                for file in self:
                    if fileExists(file) == fileName(other.path):
                        remove(file)
                        break

                raise FileNotFoundError(
                    'The file {} was not found in the folder {}'.format(fileName(other.path), self._path))

            else:
                raise TypeError('Invalid type, Expected Path')
        else:
            raise IsADirectoryError('Invalid init path')


class Container:
    """Container class."""

    def __init__(self):
        """
            A container is a directory that is created and removed automatically.
            It is only available inside the context manager, once the context is exited, the container directory
            is removed and all the files inside it. It also changes the current working directory to the container and
            back to the original after the context is exited. The original CWD is saved at the
            time of initialization, it can be accessed through the cwd property. All containers
            will have the same naming system "cwd/temp-container-<random_number>".
        """

        self.cwd = os.getcwd()
        self.container = join(self.cwd, 'temp-container-' + random.random().__str__())
        self.containerPath = Path(self.container)

    def __enter__(self):
        """
            Create the container directory and change the current working directory to it.
            return's Path Object.
         """
        os.mkdir(self.container)
        os.chdir(self.container)
        return self.containerPath

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.cwd)
        remove(self.container)

