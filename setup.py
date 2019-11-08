import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.AirtableLMMDocGenerator',
      version='0.0.1',
      description=('A docassemble extension.'),
      long_description=u"This is a document generation utility for the Airtable Legal Matter Management base. \r\nThe original template is here (free): https://airtable.com/templates/legal/expSOFU7KC5yav5TR/legal-matter-management \r\nI've modified the template for purposes of this package, \r\nand you can get that version here: https://airtable.com/shrUfrmYivppjGXuf \r\n\r\nNote that the modified version has a 'Document types' table, so that DA can draw from \r\nit to list the types of documents you can create. Based on what document type you choose, \r\nDA loads the required template and gets the required interview file. So far I have \r\nadded Letter and Contract as internal options to DA with templates. \r\n\r\nYou will need to write both the interview files and the templates for the other \r\ndocument types yourself. You can do it, I believe in you.\r\n\r\nIf you want to add a new document type please be aware you will need to add it \r\nboth in Airtable and DA. \r\n\r\nI haven't fully tested the file upload functionality, since Airtable requires a URL \r\nfrom which to download the file into the table and I'm working locally (AT can't get \r\na URL beginning with 'localhost'). \r\n\r\nEnjoy responsibly.",
      long_description_content_type='text/markdown',
      author='System Administrator',
      author_email='admin@admin.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=['airtable', 'airtable-python-wrapper', 'requests'],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/AirtableLMMDocGenerator/', package='docassemble.AirtableLMMDocGenerator'),
     )

