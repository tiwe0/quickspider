#!/usr/bin/env python3

from distutils.core import setup

with open("./README.md", "rt") as f:
    long_description = f.read()

setup(
        name='quickspider',
        version='0.1.0',
        description='help you build a small spider quickly.',
        long_description=long_description,
        author='Ivory',
        author_email='zheng@stu.xmu.edu.cn',
        url='https://github.com/tiwe0/quickspider.git',
        packages=['quickspider', 'quickspider.core', 'quickspider.template'],
        package_dir={'quickspider': 'quickspider'},
        package_data={'quickspider': ['template/*.toml']},
        scripts=['quickspider/bin/quickspider']
        )
