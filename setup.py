from setuptools import setup
setup(name='bink',
    version='0.1',
    description='bink test',
    py_modules=['bink'],
    url='tbd',
    author='martin barnard',
    author_email='barnard.martin@gmail.com',
    license='Public Domain',
    packages=['bink'],
    entry_points='''
    [console_scripts]
    bink=bink.bink:run
    '''

)
