"""
coeai - Python client for COE AI LLM inference API

A professional client library for interacting with high-capacity multimodal
Large Language Models hosted on the COE AI GPU cluster.
"""

__version__ = "4.1.0"
__author__ = "Konal Puri, Sawai Pratap Khatri"

from .infer import LLMinfer

__all__ = ["LLMinfer", "__version__"]
