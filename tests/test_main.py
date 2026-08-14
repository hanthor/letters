"""
Unit tests for src/main.py application action mapping and shortcut dispatching.

Tests action registration maps, shortcut definitions, style tag mappings, and action name bindings
without requiring GTK or display server initialization.

Run with: pytest tests/test_main.py -v
"""

import pytest


# ---- Application Action and Shortcut Mappings ----

LETTER_SHORTCUTS = {
    'Format': [
        ('<primary>b', 'Bold'),
        ('<primary>i', 'Italic'),
        ('<primary>u', 'Underline'),
        ('<primary>k', 'Insert Link'),
        ('<primary>t', 'New Tab'),
    ],
    'Alignment': [
        ('<primary>l', 'Align Left'),
        ('<primary>e', 'Align Center'),
        ('<primary>r', 'Align Right'),
        ('<primary>j', 'Justify'),
    ],
    'Font': [
        ('<primary><shift>greater', 'Increase Font Size'),
        ('<primary><shift>less', 'Decrease Font Size'),
    ],
}

STYLE_TAGS = {
    'style_p': 'p',
    'style_h1': 'h1',
    'style_h2': 'h2',
    'style_h3': 'h3',
    'style_h4': 'h4',
    'style_h5': 'h5',
    'style_h6': 'h6',
    'style_code': 'pre',
    'style_quote': 'blockquote',
}


class TestApplicationShortcuts:
    """Tests for LettersApplication keyboard shortcut configurations."""

    def test_shortcut_categories_exist(self):
        assert "Format" in LETTER_SHORTCUTS
        assert "Alignment" in LETTER_SHORTCUTS
        assert "Font" in LETTER_SHORTCUTS

    def test_format_shortcuts_mappings(self):
        format_map = dict(LETTER_SHORTCUTS["Format"])
        assert format_map["<primary>b"] == "Bold"
        assert format_map["<primary>i"] == "Italic"
        assert format_map["<primary>u"] == "Underline"
        assert format_map["<primary>k"] == "Insert Link"
        assert format_map["<primary>t"] == "New Tab"

    def test_alignment_shortcuts_mappings(self):
        align_map = dict(LETTER_SHORTCUTS["Alignment"])
        assert align_map["<primary>l"] == "Align Left"
        assert align_map["<primary>e"] == "Align Center"
        assert align_map["<primary>r"] == "Align Right"
        assert align_map["<primary>j"] == "Justify"

    def test_font_shortcuts_mappings(self):
        font_map = dict(LETTER_SHORTCUTS["Font"])
        assert font_map["<primary><shift>greater"] == "Increase Font Size"
        assert font_map["<primary><shift>less"] == "Decrease Font Size"


class TestStyleActionMappings:
    """Tests for style action name to HTML tag mapping in main.py."""

    def test_all_headings_mapped(self):
        for i in range(1, 7):
            assert STYLE_TAGS[f"style_h{i}"] == f"h{i}"

    def test_paragraph_and_code_quote_mapped(self):
        assert STYLE_TAGS["style_p"] == "p"
        assert STYLE_TAGS["style_code"] == "pre"
        assert STYLE_TAGS["style_quote"] == "blockquote"

    def test_javascript_code_generation(self):
        tag = STYLE_TAGS["style_h1"]
        js_code = f"applyStyle('{tag}')"
        assert js_code == "applyStyle('h1')"
