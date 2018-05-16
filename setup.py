from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='cashflows',
      version='0.0.4',
      description='Investment modeling and advanced engineering economics using Python',
      long_description='Investment modeling and advanced engineering economics using Python',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Office/Business :: Financial',
      ],
      keywords='cashflow investments bonds depreciation loan irr',
      url='http://github.com/jdvelasq/cashflows',
      author='Juan D. Velasquez & Ibeth K. Vergara',
      author_email='jdvelasq@unal.edu.co',
      license='MIT',
      packages=['cashflows'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
