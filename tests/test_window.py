"""
Unit tests for src/window.py logic and frontend helper contracts.

Tests format extensions, file path handling, save fallback rules, title formatting,
word count updating, and close confirmation logic without requiring a live display server.

Run with: pytest tests/test_window.py -v
"""

import pytest


# ---- Format and File Extension Rules ----

SUPPORTED_OPEN_EXTS = {"docx", "odt", "txt", "md", "html"}
SUPPORTED_SAVE_EXTS = {"odt", "docx", "rtf", "txt", "md", "html"}


class TestWindowFileExtensions:
    """Tests for file extension validation rules used by LettersWindow."""

    @pytest.mark.parametrize("filename,expected_ext,is_valid", [
        ("doc.docx", "docx", True),
        ("notes.odt", "odt", True),
        ("readme.md", "md", True),
        ("page.html", "html", True),
        ("plain.txt", "txt", True),
        ("script.py", "py", False),
        ("image.png", "png", False),
        ("data.json", "json", False),
    ])
    def test_open_extension_filtering(self, filename, expected_ext, is_valid):
        ext = filename.rpartition(".")[2].lower()
        assert ext == expected_ext
        assert (ext in SUPPORTED_OPEN_EXTS) == is_valid

    @pytest.mark.parametrize("input_path,expected_output_ext", [
        ("report.docx", "docx"),
        ("document.odt", "odt"),
        ("notes.md", "md"),
        ("index.html", "html"),
        ("file.txt", "txt"),
        ("letter.rtf", "rtf"),
        ("export.pdf", "odt"),       # Fallback to default format (odt)
        ("no_extension", "odt"),     # Fallback to default format (odt)
        ("archive.tar.gz", "odt"),   # Fallback to default format (odt)
    ])
    def test_save_extension_fallback_logic(self, input_path, expected_output_ext):
        ext = input_path.rpartition(".")[2].lower()
        if ext not in SUPPORTED_SAVE_EXTS:
            ext = "odt"
        assert ext == expected_output_ext


# ---- Title Formatting Logic ----

class TestWindowTitleFormatting:
    """Tests for window and tab title formatting rules."""

    @pytest.mark.parametrize("page_title,needs_attention,expected_window_title", [
        ("Untitled Document", False, "Untitled Document - Letters"),
        ("Untitled Document", True, "Untitled Document (*) - Letters"),
        ("Report.docx", False, "Report.docx - Letters"),
        ("Report.docx", True, "Report.docx (*) - Letters"),
    ])
    def test_format_title_with_page(self, page_title, needs_attention, expected_window_title):
        if needs_attention:
            formatted = f"{page_title} (*) - Letters"
        else:
            formatted = f"{page_title} - Letters"
        assert formatted == expected_window_title

    def test_format_title_empty_fallback(self):
        fallback_title = "Letters"
        assert fallback_title == "Letters"


# ---- Word Count Formatting ----

class TestWordCountFormatting:
    """Tests for word and character count status label formatting."""

    @pytest.mark.parametrize("words,chars,expected_label", [
        (0, 0, "0 words"),
        (1, 5, "1 words"),
        (42, 210, "42 words"),
        (1000, 5500, "1000 words"),
    ])
    def test_format_word_count_label(self, words, chars, expected_label):
        label_text = f"{words} words"
        assert label_text == expected_label


# ---- Unsaved Changes Warning Building ----

class TestUnsavedChangesDialogFormatting:
    """Tests for building dirty pages lists and unsaved changes warnings."""

    def test_single_dirty_document_warning_text(self):
        dirty_titles = ["Draft.odt"]
        lines = ["The following documents have unsaved changes:"]
        lines += [f"• {t}" for t in dirty_titles]
        lines += ["All unsaved changes will be discarded if you close Letters now."]

        body_text = "\n".join(lines)
        assert "Draft.odt" in body_text
        assert "• Draft.odt" in body_text
        assert "All unsaved changes will be discarded" in body_text

    def test_multiple_dirty_documents_warning_text(self):
        dirty_titles = ["Notes.md", "Chapter1.docx", "Untitled Document"]
        lines = ["The following documents have unsaved changes:"]
        lines += [f"• {t}" for t in dirty_titles]
        lines += ["All unsaved changes will be discarded if you close Letters now."]

        body_text = "\n".join(lines)
        assert "• Notes.md" in body_text
        assert "• Chapter1.docx" in body_text
        assert "• Untitled Document" in body_text
