#!/usr/bin/env bash
# This script should be called from the root directory as `bash scripts/make_docs.sh`.

# In order for sphinx to register the tests package as a package, __init__.py needs to be present in the folder.
touch tests/__init__.py

# Make the documentation, remembering to clean the build directory first.
(
  cd docs
  make clean && make html
)

# We cannot do this anymore as travisci won't collect coverage without __init__ in tests.
# Remove the __init__.py file so directory no longer registers as package.
#rm -rf tests/__init__.py