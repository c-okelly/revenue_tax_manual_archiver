from setuptools import setup, find_packages

setup(name='tax_manual_archiver',
      version='0.1',
      description='',
      author='Conor OKelly',
      author_email='okellyconor@gmail.com',
      url='https://github.com/c-okelly/revenue_tax_manual_archiver',
      python_requires='>3.3',
      install_requires=['bs4', 'requests'],
    #   tests_require=['responses', 'nose', 'coverage'],
      test_suite="nose.collector",
      packages=find_packages(),
      include_package_data=True,
    #   entry_points={
    #       'console_scripts': [
    #           'org_to_anki = org_to_anki.main:parseAndUploadOrgFile',
    #           'ankiq = org_to_anki.quickNote:quickNote'
    #       ]
    #   }
      )
