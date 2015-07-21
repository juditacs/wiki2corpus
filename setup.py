from setuptools import setup

setup(
    author='Judit Acs',
    author_email='judit@sch.bme.hu',
    name='wiki2corpus',
    provides=['wiki2corpus'],
    url='https://github.com/juditacs/wiki2corpus',
    packages=['wiki2corpus'],
    package_dir={'': '.'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['wikipedia', 'nltk', 'requests[security]'],
    scripts=['wiki2corpus/wiki2corpus.py'],
)
