from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(here, 'nameko_mongoengine', 'version.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='nameko_mongoengine',
        description='Mongoengine dependency provider for Nameko microservice framework',
        keywords=['nameko', 'mongoengine', 'mongodb', 'database', 'nosql', 'gridfs'],
        version=about['__version__'],
        author='Ketan Goyal',
        author_email='ketangoyal1988@gmail.com',
        license="Apache 2.0 license",
        url='https://github.com/ketgo/nameko-mongoengine',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['nameko_mongoengine'],
        python_requires='>=3.4',
        install_requires=[
            'nameko',
            'pymongo',
            'mongoengine',
        ],
        extras_require={
            'dev': [
                'pytest~=4.0',
                'pytest-cov~=2.6',
                'pytest-mock~=1.12',
                'pylint~=1.0',
                'mongomock~=3.18'
            ]
        },
        packages=find_packages(exclude=('tests', 'benchmarks')),
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries :: Python Modules",
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
    )
