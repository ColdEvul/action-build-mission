#!/usr/bin/env python3
import sys
import os
import argparse
import shutil
import subprocess
import tempfile
import glob

from distutils.dir_util import copy_tree
from pathlib import Path

__version__ = 1.0

WORK_DIR = 'tmp'

scriptPath  = os.path.realpath(__file__)
scriptRoot  = os.path.dirname(scriptPath)
ProjectRoot = os.path.dirname(os.path.dirname(scriptPath))
os.chdir(ProjectRoot)


parser = argparse.ArgumentParser(
    prog='make',
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument('--version',
    default='0.0.0',
    help="Add a additional tag to a to the build"
)
parser.add_argument('--release',
    default='release',
    help="Store generated release missions in this dir"
)
parser.add_argument('--missions',
    default='Maps',
    help="Compile missions from this dir"
)
parser.add_argument('--common',
    default='CommonBase',
    help="common sqf"
)
args = parser.parse_args()

Path(WORK_DIR).mkdir(parents=True, exist_ok=True)
outputFolder = os.path.join(ProjectRoot, WORK_DIR)

releaseFolder = os.path.join(ProjectRoot, args.release)


def mkDirectory(path):
    try:
        os.mkdir(path)
    except OSError:
        pass
    else:
        pass

def checkObjectType(obj):
    if os.path.isfile(obj):
        return "file"
    if os.path.isdir(obj):
        return "dir"

def build_archive(archive_name='release', archive_type='zip', archive_input=outputFolder):
    print('Archiving files...')
    archive_output = os.path.join(releaseFolder, archive_name)
    shutil.make_archive(archive_output, archive_type, archive_input)
    print('Release archive created...')


def main():
    global tmpFolder
    tmpFolder = tempfile.mkdtemp()

    for mission_files in glob.glob(os.path.join(ProjectRoot, args.missions, '*')):
        for mission in glob.glob(mission_files):
            mission_name = os.path.basename(mission)
            new_mission_name = mission_name.replace('DEVBUILD', args.version)

            assembly_path = os.path.join(tmpFolder, new_mission_name)
            common_mission_files = os.path.join(os.path.join(ProjectRoot, args.common))

            print("Assembling '{}'...".format(new_mission_name))

            copytree(common_mission_files, assembly_path, dirs_exist_ok=True)
            copytree(mission, assembly_path, dirs_exist_ok=True)

            subprocess.call('armake2 build "{}" "{}.pbo"'.format(assembly_path, os.path.join(outputFolder, new_mission_name)), shell=True)

            print("Completed assembly of {}.".format(new_mission_name))

    
    for debugFile in glob.glob(os.path.join(outputFolder, '*')):
        print("DEBUG:   ", debugFile, os.path.getsize(debugFile))

    archive_name = os.path.splitext(new_mission_name)[0]
    build_archive(archive_name)

if __name__ == "__main__":
    sys.exit(main())

def copytree(src, dst, symlinks=False, ignore=None):
    """Recursively copy a directory tree using copy2().

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.

    XXX Consider this example code rather than the ultimate tool.

    """
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    _mkdir(dst) # XXX
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error), why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error, err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass

