import ast
import os
import re

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'laituri', '__init__.py')) as infp:
    version = ast.literal_eval(re.search('__version__ = (.+?)$', infp.read(), re.M).group(1))

with open('README.md') as fp:
    long_description = fp.read()

if __name__ == '__main__':
    setuptools.setup(
        name='laituri',
        description='Docker Toolkit for Python',
        long_description=long_description,
        long_description_content_type='text/markdown',
        version=version,
        author='Valohai',
        author_email='hait@valohai.com',
        maintainer='Ruksi Laine',
        maintainer_email='me@ruk.si',
        url='https://github.com/valohai/laituri',
        include_package_data=True,
        license='MIT',
        python_requires='>=3.6',
        packages=setuptools.find_packages('.', exclude=('laituri_tests', 'laituri_tests.*',)),
        install_requires=['requests>=2.23,<3'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
