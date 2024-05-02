from setuptools import setup, find_packages

setup(
    name='python_benchmarking_suite',
    version='0.1',
    license='BSD 3-Clause License',
    license_files=("LICENSE",),
    description="Python Benchmarking Suite",
    author='Niklas Roemer',
    author_email='nroemer@ethz.ch',
    url='https://github.com/nrmer/Benchmark_Suite',
    python_requires=">=3.8",
    install_requires=[],
    packages=find_packages(),
)
