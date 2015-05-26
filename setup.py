#!/usr/bin/env python
"""
Copyright (c) 2014 Pimoroni

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
import os
from setuptools import setup


METADATA_FILENAME = 'explorerhat/package_metadata.json'


def readme():
    """
    Return the contents of the README file
    :return:
    """
    data = ''
    for filename in ['README.rst', 'README.md', 'README.txt']:
        if os.path.exists(filename):
            with open(filename) as file_handle:
                data = file_handle.read()
                break
    return data


setup_arguments = {
    'name': 'ExplorerHAT',
    'version': '0.1.1',
    'author': 'Philip Howard',
    'author_email': 'phil@pimoroni.com',
    'description': 'A module to control the Explorer HAT Raspberry Pi Addon Board',
    'long_description': readme(),
    'license': 'MIT',
    'keywords': 'Raspberry Pi Explorer HAT',
    'url': 'http://shop.pimoroni.com',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: System :: Hardware'
    ],
    'py_modules': ['explorerhat'],
    'install_requires': ['rpi.gpio >= 0.5.10'],
    'package_data': {
        'explorerhat': ['package_metadata.json']
    },
    'include_package_data': True,
}


class Git(object):
    """
    Simple wrapper class to the git command line tools
    """
    version_list = ['0', '7', '0']

    def __init__(self, version=None):
        if version:
            self.version_list = version.split('.')

    @property
    def version(self):
        """
        Generate a Unique version value from the git information
        :return:
        """
        git_rev = len(os.popen('git rev-list HEAD').readlines())
        if git_rev != 0:
            self.version_list[-1] = '%d' % git_rev
        version = '.'.join(self.version_list)
        return version

    @property
    def branch(self):
        """
        Get the current git branch
        :return:
        """
        return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    @property
    def hash(self):
        """
        Return the git hash for the current build
        :return:
        """
        return os.popen('git rev-parse HEAD').read().strip()

    @property
    def origin(self):
        """
        Return the fetch url for the git origin
        :return:
        """
        for item in os.popen('git remote -v'):
            split_item = item.strip().split()
            if split_item[0] == 'origin' and split_item[-1] == '(push)':
                return split_item[1]


def add_scripts_to_package():
    """
    Update the "scripts" parameter of the setup_arguments with any scripts
    found in the "scripts" directory.
    :return:
    """
    global setup_arguments

    if os.path.isdir('scripts'):
        setup_arguments['scripts'] = [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]


def get_and_update_package_metadata():
    """
    Update the package metadata for this package if we are building the package.
    :return:metadata - Dictionary of metadata information
    """
    global setup_arguments
    global METADATA_FILENAME

    if not os.path.exists('.git') and os.path.exists(METADATA_FILENAME):
        with open(METADATA_FILENAME) as fh:
            metadata = json.load(fh)
    else:
        git = Git(version=setup_arguments['version'])
        metadata = {
            'version': git.version,
            'long_description': 'A ping like tool for network services',
            'git_hash': git.hash,
            'git_origin': git.origin,
            'git_branch': git.branch
        }
        for readme_file in ['README.rst', 'README.md', 'README.txt']:
            if os.path.exists(readme_file):
                with open(readme_file) as file_handle:
                    metadata['long_description'] = file_handle.read()
                break
        with open(METADATA_FILENAME, 'w') as fh:
            json.dump(metadata, fh)
    return metadata


if __name__ == '__main__':
    metadata = get_and_update_package_metadata()
    setup_arguments['version'] = metadata['version']
    setup_arguments['long_description'] = metadata['long_description']
    add_scripts_to_package()
    setup(**setup_arguments)
