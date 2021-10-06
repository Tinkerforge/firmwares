#!/usr/bin/python3 -u

import os
import stat
import re
import shutil

def main():
    base_dir = os.path.dirname(os.path.realpath(__file__))

    for category in ['brick', 'bricklet', 'extension']:
        start_dir = os.path.join(base_dir, category + 's')

        for root, dirs, files in os.walk(start_dir):
            if root == start_dir:
                continue

            names = set()
            versions = []
            extensions = set()

            for file_ in files:
                path = os.path.join(root, file_)
                s = os.stat(path)

                if stat.S_IMODE(s.st_mode) != 0o644:
                    print('WARNING: unexpected mode:', path, oct(s.st_mode))

                if re.match(r'^{0}_.*_firmware_latest.z?bin$'.format(category), file_) != None:
                    continue

                m = re.match(r'^{0}_(.*)_firmware_(\d+)_(\d+)_(\d+)\.(z?bin)$'.format(category), file_)

                if m == None:
                    print('WARNING: unexpected filename:', file_, path)
                    continue

                names.add(m.group(1))
                versions.append((int(m.group(2)), int(m.group(3)), int(m.group(4))))
                extensions.add(m.group(5))

            if len(names) == 0:
                print('ERROR: no names:', root)
                continue

            if len(names) > 1:
                print('ERROR: mixed names:', root)
                continue

            if len(extensions) > 1:
                print('ERROR: mixed extensions:', root)
                continue

            name = names.pop()
            latest_version = sorted(versions)[-1]
            extension = extensions.pop()
            source = '{0}_{1}_firmware_{2}_{3}_{4}.{5}'.format(category, name, *latest_version, extension)
            target = '{0}_{1}_firmware_latest.{2}'.format(category, name, extension)

            os.remove(os.path.join(root, target))
            os.symlink(source, os.path.join(root, target))

if __name__ == '__main__':
    main()
