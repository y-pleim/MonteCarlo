"""A Python package for simulating an N-spin system."""

# Add imports here
from .SpinConfiguration import *
from .Hamiltonian import *
from .SpinConfigurationSystem import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
