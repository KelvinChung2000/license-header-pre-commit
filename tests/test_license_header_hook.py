"""Tests for license_header_hook module."""

import os
import tempfile
from unittest.mock import patch

import pytest

from license_header_hook import (
    CommentRegistry,
    LicenseHeaderManager,
    main,
    should_process_file,
)


class TestCommentRegistry:
    """Test CommentRegistry functionality."""

    def test_default_mappings(self):
        """Test that default mappings are loaded correctly."""
        registry = CommentRegistry()

        # Test Python
        python_style = registry.get_comment_style("test.py")
        assert python_style == {"start": "#", "middle": "#", "end": "#"}

        # Test JavaScript
        js_style = registry.get_comment_style("test.js")
        assert js_style == {"start": "/*", "middle": " *", "end": " */"}

        # Test unknown extension
        unknown_style = registry.get_comment_style("test.unknown")
        assert unknown_style is None

    def test_custom_mappings(self):
        """Test custom mappings override defaults."""
        custom = {".custom": {"start": "//", "middle": "//", "end": "//"}}
        registry = CommentRegistry(custom)

        custom_style = registry.get_comment_style("test.custom")
        assert custom_style == {"start": "//", "middle": "//", "end": "//"}


class TestLicenseHeaderManager:
    """Test LicenseHeaderManager functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_file = os.path.join(self.temp_dir, "template.txt")

        # Create template file
        with open(self.template_file, "w") as f:
            f.write("Copyright (c) {year} {copyright_holder}\nLicense text here")

        self.registry = CommentRegistry()
        self.manager = LicenseHeaderManager(
            self.template_file, "Test Corp", self.registry
        )

    def test_load_template(self):
        """Test template loading."""
        template = self.manager.load_template()
        assert "Copyright (c) {year} {copyright_holder}" in template
        assert "License text here" in template

    def test_format_template(self):
        """Test template formatting with placeholders."""
        template = "Copyright (c) {year} {copyright_holder}"
        formatted = self.manager.format_template(template)

        assert str(self.manager.current_year) in formatted
        assert "Test Corp" in formatted

    def test_create_header_comment_single_line(self):
        """Test creating header with single-line comments."""
        content = "Line 1\nLine 2"
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        result = self.manager.create_header_comment(content, comment_style)

        assert result == "# Line 1\n# Line 2"

    def test_create_header_comment_multi_line(self):
        """Test creating header with multi-line comments."""
        content = "Line 1\nLine 2"
        comment_style = {"start": "/*", "middle": " *", "end": " */"}

        result = self.manager.create_header_comment(content, comment_style)

        expected = "/*\n * Line 1\n * Line 2\n */"
        assert result == expected


class TestShouldProcessFile:
    """Test file filtering functionality."""

    def test_no_patterns(self):
        """Test processing when no patterns are specified."""
        assert should_process_file("test.py", [], [])

    def test_include_patterns(self):
        """Test include pattern matching."""
        assert should_process_file("test.py", ["*.py"], [])
        assert not should_process_file("test.js", ["*.py"], [])

    def test_exclude_patterns(self):
        """Test exclude pattern matching."""
        assert not should_process_file("test.py", [], ["*.py"])
        assert should_process_file("test.js", [], ["*.py"])

    def test_include_and_exclude_patterns(self):
        """Test both include and exclude patterns."""
        # Excluded files should not be processed even if they match include
        assert not should_process_file("test.py", ["*.py"], ["test.py"])

        # Files matching include but not exclude should be processed
        assert should_process_file("other.py", ["*.py"], ["test.py"])


class TestMain:
    """Test main function and CLI interface."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_file = os.path.join(self.temp_dir, "template.txt")
        self.test_file = os.path.join(self.temp_dir, "test.py")

        # Create template file
        with open(self.template_file, "w") as f:
            f.write("Copyright (c) {year} {copyright_holder}")

        # Create test Python file
        with open(self.test_file, "w") as f:
            f.write("print('hello world')\n")

    def test_main_with_valid_args(self):
        """Test main function with valid arguments."""
        test_args = [
            "license_header_hook.py",
            "--template",
            self.template_file,
            "--copyright-holder",
            "Test Corp",
            self.test_file,
        ]

        with patch("sys.argv", test_args):
            result = main()

        # Should return 1 when files are modified
        assert result == 1

        # Check that file was modified
        with open(self.test_file) as f:
            content = f.read()

        assert "Copyright (c)" in content
        assert "Test Corp" in content

    def test_main_no_files_to_process(self):
        """Test main function when no files need processing."""
        # Create file that already has correct header
        template_content = f"Copyright (c) {2025} Test Corp"
        header = f"# {template_content}"

        with open(self.test_file, "w") as f:
            f.write(f"{header}\n\nprint('hello world')\n")

        test_args = [
            "license_header_hook.py",
            "--template",
            self.template_file,
            "--copyright-holder",
            "Test Corp",
            self.test_file,
        ]

        with patch("sys.argv", test_args):
            result = main()

        # Should return 0 when no files are modified
        assert result == 0


if __name__ == "__main__":
    pytest.main([__file__])

    def test_main_missing_template_file(self):
        """Test main function with missing template file."""
        test_args = [
            "license_header_hook.py",
            "--template",
            "nonexistent.txt",
            "--copyright-holder",
            "Test Corp",
            self.test_file,
        ]

        with patch("sys.argv", test_args):
            with pytest.raises(FileNotFoundError):
                main()

    def test_main_with_include_exclude_patterns(self):
        """Test main function with include/exclude patterns."""
        # Create multiple test files
        py_file = os.path.join(self.temp_dir, "test.py")
        js_file = os.path.join(self.temp_dir, "test.js")

        with open(py_file, "w") as f:
            f.write("print('python')\n")
        with open(js_file, "w") as f:
            f.write("console.log('javascript');\n")

        test_args = [
            "license_header_hook.py",
            "--template",
            self.template_file,
            "--copyright-holder",
            "Test Corp",
            "--include",
            "*.py",
            "--exclude",
            "test.py",
            py_file,
            js_file,
        ]

        with patch("sys.argv", test_args):
            result = main()

        # Should return 0 since py file is excluded and js file doesn't match include
        assert result == 0


class TestLicenseHeaderManagerAdvanced:
    """Advanced tests for LicenseHeaderManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.template_file = os.path.join(self.temp_dir, "template.txt")

        # Create template file
        with open(self.template_file, "w") as f:
            f.write("Copyright (c) {year} {copyright_holder}\nLicense text here")

        self.registry = CommentRegistry()
        self.manager = LicenseHeaderManager(
            self.template_file, "Test Corp", self.registry
        )

    def test_process_file_with_shebang(self):
        """Test processing file with shebang line."""
        test_file = os.path.join(self.temp_dir, "script.py")

        with open(test_file, "w") as f:
            f.write("#!/usr/bin/env python3\nprint('hello')\n")

        result = self.manager.process_file(test_file)
        assert result is True

        # Check that shebang is preserved
        with open(test_file) as f:
            content = f.read()

        lines = content.split("\n")
        assert lines[0] == "#!/usr/bin/env python3"
        assert "Copyright (c)" in content

    def test_process_file_with_existing_header(self):
        """Test processing file that already has a header."""
        test_file = os.path.join(self.temp_dir, "existing.py")

        # Create file with existing header
        with open(test_file, "w") as f:
            f.write("# Copyright (c) 2020 Old Corp\n# Old license\n\nprint('hello')\n")

        result = self.manager.process_file(test_file)
        assert result is True

        # Check that old header is replaced
        with open(test_file) as f:
            content = f.read()

        assert "Old Corp" not in content
        assert "Test Corp" in content
        assert str(self.manager.current_year) in content

    def test_process_file_multiline_comments(self):
        """Test processing file with multi-line comment style."""
        test_file = os.path.join(self.temp_dir, "test.js")

        with open(test_file, "w") as f:
            f.write("console.log('hello');\n")

        result = self.manager.process_file(test_file)
        assert result is True

        # Check multi-line comment format
        with open(test_file) as f:
            content = f.read()

        assert content.startswith("/*")
        assert " * Copyright (c)" in content
        assert " */" in content

    def test_process_file_unsupported_extension(self):
        """Test processing file with unsupported extension."""
        test_file = os.path.join(self.temp_dir, "test.unknown")

        with open(test_file, "w") as f:
            f.write("some content\n")

        result = self.manager.process_file(test_file)
        assert result is False

    def test_process_file_read_error(self):
        """Test processing file with read error."""
        # Test with non-existent file
        result = self.manager.process_file("nonexistent.py")
        assert result is False

    def test_extract_existing_header_multiline(self):
        """Test extracting existing multi-line header."""
        content = """/*
 * Copyright (c) 2020 Old Corp
 * License text
 */

console.log('hello');
"""
        comment_style = {"start": "/*", "middle": " *", "end": " */"}

        header = self.manager.extract_existing_header(content, comment_style)
        assert header is not None
        assert "Old Corp" in header

    def test_extract_existing_header_single_line(self):
        """Test extracting existing single-line header."""
        content = """# Copyright (c) 2020 Old Corp
# License text

print('hello')
"""
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        header = self.manager.extract_existing_header(content, comment_style)
        assert header is not None
        assert "Old Corp" in header

    def test_extract_existing_header_with_shebang(self):
        """Test extracting header from file with shebang."""
        content = """#!/usr/bin/env python3
# Copyright (c) 2020 Old Corp
# License text

print('hello')
"""
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        header = self.manager.extract_existing_header(content, comment_style)
        assert header is not None
        assert "Old Corp" in header

    def test_extract_existing_header_no_header(self):
        """Test extracting header when none exists."""
        content = "print('hello')\n"
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        header = self.manager.extract_existing_header(content, comment_style)
        assert header is None

    def test_remove_existing_header_multiline(self):
        """Test removing existing multi-line header."""
        content = """/*
 * Copyright (c) 2020 Old Corp
 * License text
 */

console.log('hello');
"""
        comment_style = {"start": "/*", "middle": " *", "end": " */"}

        result = self.manager.remove_existing_header(content, comment_style)
        assert "Old Corp" not in result
        assert "console.log('hello');" in result

    def test_remove_existing_header_with_shebang(self):
        """Test removing header while preserving shebang."""
        content = """#!/usr/bin/env python3
# Copyright (c) 2020 Old Corp
# License text

print('hello')
"""
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        result = self.manager.remove_existing_header(content, comment_style)
        assert result.startswith("#!/usr/bin/env python3")
        assert "Old Corp" not in result
        assert "print('hello')" in result

    def test_process_file_no_change_when_header_correct(self):
        """Test that file is not modified when header is already correct."""
        test_file = os.path.join(self.temp_dir, "correct_header.py")

        # Create file with correct header
        template = self.manager.load_template()
        formatted = self.manager.format_template(template)
        comment_style = self.manager.comment_registry.get_comment_style(
            "correct_header.py"
        )
        correct_header = self.manager.create_header_comment(formatted, comment_style)

        with open(test_file, "w") as f:
            f.write(f"{correct_header}\n\nprint('hello')\n")

        # Store original modification time
        original_stat = os.stat(test_file)

        result = self.manager.process_file(test_file)
        assert result is False  # No change needed

        # Verify file wasn't modified
        new_stat = os.stat(test_file)
        assert new_stat.st_mtime == original_stat.st_mtime

    def test_extract_header_content_single_line(self):
        """Test extracting content from single-line comments."""
        header = "# Copyright (c) 2025 Test Corp\n# License text"
        comment_style = {"start": "#", "middle": "#", "end": "#"}

        content = self.manager._extract_header_content(header, comment_style)
        expected = "Copyright (c) 2025 Test Corp\nLicense text"
        assert content == expected

    def test_extract_header_content_multi_line(self):
        """Test extracting content from multi-line comments."""
        header = "/*\n * Copyright (c) 2025 Test Corp\n * License text\n */"
        comment_style = {"start": "/*", "middle": " *", "end": " */"}

        content = self.manager._extract_header_content(header, comment_style)
        expected = "Copyright (c) 2025 Test Corp\nLicense text"
        assert content == expected
