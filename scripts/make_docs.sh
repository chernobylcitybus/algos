#!/usr/bin/env bash
# This script should be called from the root directory as `bash scripts/make_docs.sh`.

# In order for sphinx to register the tests package as a package, __init__.py needs to be present in the folder.
# However, the tests package should not be treated like a package otherwise. So we create __init__.py, make the
# docs and then remove it.
touch tests/__init__.py

# Make the documentation, remembering to clean the build directory first.
(
  cd docs
  make clean && make html
)

# Remove the __init__.py file so directory no longer registers as package.
rm -rf tests/__init__.py