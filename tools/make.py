#!/usr/bin/env python3
import sys
import os
import argparse
import shutil
import stat
import subprocess
import tempfile
import glob

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

## https://stackoverflow.com/a/22331852
def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    shutil.copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass # lchmod not available
    elif os.path.isdir(s):
      copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)

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

            copytree(common_mission_files, assembly_path)
            copytree(mission, assembly_path)

            subprocess.call('armake2 build "{}" "{}.pbo"'.format(assembly_path, os.path.join(outputFolder, new_mission_name)), shell=True)

            print("Completed assembly of {}.".format(new_mission_name))

    
    for debugFile in glob.glob(os.path.join(outputFolder, '*')):
        print("DEBUG:   ", debugFile, os.path.getsize(debugFile))

    archive_name = os.path.splitext(new_mission_name)[0]
    build_archive(archive_name)

if __name__ == "__main__":
    sys.exit(main())
