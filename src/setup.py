import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='chariot',
    version='0.1.0',
    author='Chariot Dev',
	author_email='chariot@drexel.edu',
    description='A configurable, scalable distributed data collection system for the IoT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chariot-dev/chariot',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'flask',
        'mysql',
        'pymongo',
        'requests',
        'sllurp',
        'twisted',
        'websockets',
    ],
    setup_requires=['wheel'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['pytest', 'tox'],
    },
    project_urls={
            'Documentation': 'https://github.com/chariot-dev/chariot',
            'Source Code': 'https://github.com/chariot-dev/chariot',
            'Bug Tracker': 'https://github.com/chariot-dev/chariot/issues',
    },
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
