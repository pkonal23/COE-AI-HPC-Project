# Changelog

All notable changes to the `coeai` package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.0] - 2026-02-07

### Added
- **New Parameter**: `context_window` (defaults to 2048) in `generate()` method.
- Pass `num_ctx` to Ollama backend to support larger context windows (e.g., for `deepseek-r1:70b`).

## [4.0.0] - 2026-02-07

### Breaking Changes
- **Fixed default port** from `8001` to `8000` (IP address unchanged: `http://10.9.6.165:8000`)
- **API Key Generation**: Use web dashboard at https://coeai.ddn.upes.ac.in
- **Network Requirement**: API is only accessible from UPES's internal network (UPESNET)
- **Minimum Python version** increased to 3.7 (was 3.6)

### Added
- New `list_models()` method to programmatically discover available models
- Custom exception classes: `COEAIError`, `AuthenticationError`, `ModelNotFoundError`, `InferenceError`
- Debug logging support via Python's `logging` module
- `__version__` attribute for programmatic version checking
- Comprehensive error messages with actionable guidance
- File path validation before sending requests
- Support for more vision models (not just `llama4:16x17b`)
- UPESNET requirement notices throughout documentation

### Fixed
- **Critical**: File handle leaks in image upload - now properly closes all file handles
- **Critical**: Corrected default port from 8001 to 8000
- Updated model list in documentation to match current server offerings
- Improved error handling with specific HTTP status code handling

### Changed
- Relaxed vision model restriction - now allows any model that supports images
- Enhanced docstrings with detailed parameter descriptions and examples
- Improved package metadata in `setup.py` with project URLs
- Updated README with migration guide, troubleshooting section, and current models
- API key dashboard URL: https://coeai.ddn.upes.ac.in

### Removed
- Removed Python 3.6 support

---

## [2.3.0] - 2024

### Added
- Production release with stable API
- Text-to-text inference support
- Image-to-text inference support
- Streaming response capability
- Multiple image processing
- Custom conversation messages support
- Comprehensive documentation

### Features
- Support for multiple LLM models
- Vision model support with `llama4:16x17b`
- Parameter control (temperature, top_p, max_tokens)
- FastAPI backend integration

---

## [1.0.0] - Initial Release

### Added
- Basic LLM inference client
- Text generation support
- API key authentication
