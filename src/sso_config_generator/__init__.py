"""SSO Config Generator - Generate AWS SSO configuration and directory structures."""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0"

from .core import SSOConfigGenerator

__all__ = ["SSOConfigGenerator", "__version__"]
