import os


def getFilePaths(path, key=None):
    # read a folder, return the complete path
    ret = []
    if os.path.isdir(path):
        # Reading from a path...
        for root, dirs, files in os.walk(path):
            for filespath in files:
                ret.append(os.path.join(root, filespath))
        sorted(ret, key=key)
        return ret
    else:
        # Reading a single file...
        ret.append(path)
        return ret


def getSubDirs(path):
    subdirs = [x[0] for x in os.walk(path)]
    subdirs.sort()
    subdirs = subdirs[1:]
    return subdirs
