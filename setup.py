from setuptools import setup, find_packages
from pathlib import Path

# Safely read the README content
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="coeai",
    version="4.0.0",  # Major version bump for breaking changes
    author="Konal Puri, Sawai Pratap Khatri",
    author_email="purikonal23@gmail.com",
    description="Professional Python client for COE AI LLM inference API with text and vision support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkonal23/COE-AI-HPC-Project",
    project_urls={
        "Bug Reports": "https://github.com/pkonal23/COE-AI-HPC-Project/issues",
        "Source": "https://github.com/pkonal23/COE-AI-HPC-Project",
        "API Server": "http://10.9.6.165:8000",
        "Get API Key": "https://coeai.ddn.upes.ac.in",
    },
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="llm inference coeai ollama ai-client multimodal vision deepseek llama",
)
