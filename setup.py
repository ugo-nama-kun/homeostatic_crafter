import setuptools
import pathlib


setuptools.setup(
    name='homeostatic_crafter',
    version='1.1.2',
    description='Open world survival game for reinforcement learning.',
    url='https://github.com/ugo-nama-kun/homeostatic_crafter',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['homeostatic_crafter'],
    package_data={'homeostatic_crafter': ['data.yaml', 'assets/*']},
    entry_points={'console_scripts': ['homeostatic_crafter=homeostatic_crafter.run_gui:main']},
    install_requires=[
        'numpy', 'imageio', 'pillow', 'opensimplex', 'ruamel.yaml',
    ],
    extras_require={'gui': ['pygame']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
