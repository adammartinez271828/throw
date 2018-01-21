"""A setuptools based setup module.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='throw-dice',  # Required
    version='0.1.0',  # Required
    description='Die Roll Probability Calculator',  # Required
    long_description=LONG_DESCRIPTION,  # Optional
    url='https://github.com/adammartinez271828/throw',  # Optional
    author='Adam Martinez',  # Optional
    author_email='adam.paul.martinez@gmail.com',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='dice probability throw roll',  # Optional

    packages=find_packages(
        exclude=[
            'contrib',
            'cover',
            'docs',
            'tests',
        ]
    ),  # Required
    # install_requires=[],  # Optional
    extras_require={  # Optional
        # 'dev': ['check-manifest'],
        'test': ['nose', 'tox'],
    },
    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],  # Optional

    # entry_points={  # Optional
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
