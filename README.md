# License Header Pre-commit Hook

A Python-based pre-commit hook that automatically adds or updates license headers in source code files.

## Features

- **Automatic Detection**: Detects existing license headers and updates them
- **Multi-language Support**: Built-in support for Python, JavaScript, Java, C/C++, Go, Rust, and more
- **Configurable**: Uses template files and CLI options for customization
- **File Filtering**: Include/exclude patterns to control which files are processed
- **Year Updates**: Automatically uses current year in license headers

## Installation

### As a pre-commit hook

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/KelvinChung2000/license-header-pre-commit
    hooks:
      - id: license-header
        ref:
        name: License Header
        entry: python license_header_hook.py
        language: python
        files: \.(py|js|ts|java|c|cpp|h|hpp|go|rs)$
        args: [
          "--template", "license-header.txt",
          "--copyright-holder", "Your Company LLC"
        ]
```

### Standalone usage

```bash
python license_header_hook.py --template license-header.txt --copyright-holder "Your Company LLC" file1.py file2.js
```

## Configuration

### Template File

Create a `license-header.txt` file with your license template:

```
Copyright (c) {year} {copyright_holder}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

The template supports these placeholders:
- `{year}`: Current year
- `{copyright_holder}`: Copyright holder from CLI argument

### Command Line Options

- `--template, -t`: Path to license header template file (required)
- `--copyright-holder, -c`: Copyright holder name (required)
- `--include, -i`: File patterns to include (can be used multiple times)
- `--exclude, -e`: File patterns to exclude (can be used multiple times)

### Supported File Types

The hook includes built-in support for:

- **Python**: `.py`, `.pyx`
- **JavaScript/TypeScript**: `.js`, `.ts`, `.jsx`, `.tsx`
- **Java**: `.java`
- **C/C++**: `.c`, `.cpp`, `.cc`, `.h`, `.hpp`
- **Go**: `.go`
- **Rust**: `.rs`
- **Shell**: `.sh`, `.bash`
- **CSS**: `.css`, `.scss`
- **HTML/XML**: `.html`, `.xml`
- **YAML**: `.yml`, `.yaml`

## Examples

### Basic usage
```bash
python license_header_hook.py --template license-header.txt --copyright-holder "Acme Corp" src/main.py
```

### With file filtering
```bash
python license_header_hook.py \
  --template license-header.txt \
  --copyright-holder "Acme Corp" \
  --include "src/**/*.py" \
  --exclude "tests/**" \
  src/main.py src/utils.py
```

### Pre-commit integration
```bash
pre-commit install
pre-commit run license-header --all-files
```

## How it Works

1. **Detection**: Scans files for existing license headers at the top (after shebang if present)
2. **Removal**: Removes old headers if found
3. **Insertion**: Adds new header with current year and specified copyright holder
4. **Comment Style**: Automatically uses appropriate comment syntax based on file extension

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
