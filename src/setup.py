from setuptools import setup

setup(
    name='nylo',
    version='0.1.0',
    packages=['nylo', 'nylo.lexers', 'nylo.lexers.struct', 'nylo.lexers.values',
              'nylo.objects', 'nylo.objects.interfaces', 'nylo.objects.struct',
              'nylo.objects.values'],
    url='https://github.com/pyTeens/nylo',
    license='GNU GENERAL PUBLIC LICENSE',
    author='pyTeens',
    author_email='',
    description='A cool programming language',
    entry_points = {
        'console_scripts': ['nylo=nylo.__main__:main'],
    }
)
