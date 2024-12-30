"""Setup configuration for GEX Tracker package."""

from setuptools import setup, find_packages

# Read version from package
with open('src/gex_tracker/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'").strip('"')
            break

# Read README for long description
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='gex-tracker',
    version=version,
    author='Batu Cam',
    author_email='batuhan.camlica@gmail.com',
    description='A tool for analyzing Gamma Exposure in options markets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/batucam/gex-tracker',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    python_requires='>=3.8',
    install_requires=[
        'pandas>=2.0.0',
        'requests>=2.31.0',
        'matplotlib>=3.7.0',
        'numpy>=1.24.0',
        'python-dotenv>=1.0.0',
        'aiohttp>=3.9.0',
        'plotly>=5.18.0',
        'seaborn>=0.12.0',
        'polygon-api-client>=1.12.0'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'isort>=5.0.0',
            'mypy>=1.0.0',
            'flake8>=6.0.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'gex-tracker=gex_tracker.main:main',
            'gex-tracker-rt=gex_tracker.realtime_cli:main'
        ]
    }
) 