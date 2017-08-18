from setuptools import setup, find_packages

setup(name='polyjuice',
    version='0.1.0',
    description='Anonymize dicom files.',
    url='https://github.com/ctsit/polyjuice',
    author='Naomi Braun and Ajantha Ramineni',
    author_email='naomi.d.braun@gmail.com, ajantha.5779@gmail.com',
    license='Apache 2.0',
    packages=find_packages(),
    entry_points={
          'console_scripts': [
              'polyjuice = polyjuice.__main__:main',
          ],
      },
    install_requires=['docopt', 'pydicom', 'PyYaml'])
