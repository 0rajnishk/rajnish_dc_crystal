## 📦 Package Maintenance

### How to Update and Release a New Version

1. **Make your code changes**
   - Implement new features or fix bugs in the codebase
   - Update tests if necessary
   - Update documentation (including this README) if needed

2. **Update the version number**
   - Open `pyproject.toml`
   - Update the version number in the `[project]` section:
     ```toml
     [project]
     name = "rajnish-dc-crystal"
     version = "X.Y.Z"  # Update this version number
     ```
   - Follow [Semantic Versioning](https://semver.org/):
     - MAJOR version for incompatible API changes
     - MINOR version for added functionality in a backward-compatible manner
     - PATCH version for backward-compatible bug fixes

3. **Build the package**
   ```bash
   # Make sure you have the latest build tools
   pip install --upgrade build twine
   
   # Build the package
   python -m build
   ```

4. **Verify the build**
   - Check the `dist/` directory for the new package files
   - Test the built package locally:
     ```bash
     pip install dist/rajnish_dc_crystal-X.Y.Z-py3-none-any.whl --force-reinstall
     ```

5. **Upload to PyPI**
   ```bash
   # Upload to TestPyPI first (recommended for testing)
   twine upload --repository testpypi dist/*
   
   # If everything looks good, upload to the real PyPI
   twine upload dist/*
   ```
   - You'll need to enter your PyPI credentials
   - For token authentication, use:
     ```bash
     export TWINE_USERNAME='__token__'
     export TWINE_PASSWORD='your-api-token-here'
     ```

6. **Create a GitHub Release**
   - Tag the release in git:
     ```bash
     git tag -a vX.Y.Z -m "Version X.Y.Z"
     git push origin vX.Y.Z
     ```
   - Go to GitHub Releases and create a new release with the tag
   - Include release notes with the changes in this version

7. **Update Dependencies** (if needed)
   - Update `requirements.txt` or `pyproject.toml` with any new dependencies
   - Test the installation with the updated dependencies
