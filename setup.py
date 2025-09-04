from setuptools import setup, find_packages
from pathlib import Path

# Safely read the README content
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="coeai",
    version="2.3.1",  # Bump version before re-upload
    author="Konal Puri",
    author_email="purikonal23@gmail.com",
    description="Client to interact with COE AI-hosted LLM models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pkonal/coeai",  
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",  # ✅
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    keywords="llm inference coeai ollama ai-client",
)
