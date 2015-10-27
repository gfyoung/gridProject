"""
Runs basic checkstyle on the entire codebase using the PEP8.
Note that this file is self-reflective, so checkstyle will
also be run on the checkstyle.py file itself!
"""

from fabric.api import hide, local
from os import getcwd
from sys import exit

try:
    import pep8
except ImportError:
    print "\nFAILURE: Cannot run Python checkstyle! Missing library pep8"
    print "Please run '(sudo) pip install pep8' to install\n"
    exit(-1)

errorsFound = False

currentDir = getcwd()
excludedPy = ['.svn', 'CVS', '.bzr', '.hg', '.git',
              '__pycache__', '.tox', 'tmpFile*']
pythonErrorFile = "pythonStyleErrors.txt"

print "\nPerforming Python checkstyle..."

try:
    with hide('aborts', 'running'):
        local("pep8 {projDir} --exclude={excludedPy} > {errFile}"
              .format(projDir=currentDir,
                      excludedPy=','.join(excludedPy),
                      errFile=pythonErrorFile))
        print "SUCCESS: Python checkstyle passed!"
except:
    errorsFound = True
    print "FAILURE: Python checkstyle errors were found!\n" \
          "Please look at {projDir}/styleErrors.txt for " \
          "more information".format(projDir=currentDir)

print "\nOverall result of checkstyle is:"

if errorsFound:
    print "FAILURE: Checkstyle complete, but errors were found!\n"
else:
    print "SUCCESS: Checkstyle complete, and no errors were found!\n"
