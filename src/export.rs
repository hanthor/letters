// export.rs — Document export: Markdown → Typst → PDF.
// SPDX-License-Identifier: GPL-3.0-or-later

use pulldown_cmark::{Parser, html};

/// Convert Markdown to Typst source.
pub fn markdown_to_typst(md: &str) -> String {
    let mut out = String::from("#set page(width: auto, height: auto, margin: 2cm)\n");
    out.push_str("#set text(font: \"Sans\", size: 11pt)\n\n");
    // Simple: convert to HTML first, then basic Typst
    let parser = Parser::new(md);
    let mut html_buf = String::new();
    html::push_html(&mut html_buf, parser);
    // Basic HTML→Typst conversion
    out.push_str(&html_to_typst(&html_buf));
    out
}

fn html_to_typst(html: &str) -> String {
    html.replace("<h1>", "= ")
        .replace("</h1>", "\n")
        .replace("<h2>", "== ")
        .replace("</h2>", "\n")
        .replace("<h3>", "=== ")
        .replace("</h3>", "\n")
        .replace("<p>", "")
        .replace("</p>", "\n\n")
        .replace("<strong>", "*")
        .replace("</strong>", "*")
        .replace("<em>", "_")
        .replace("</em>", "_")
        .replace("<ul>", "")
        .replace("</ul>", "")
        .replace("<li>", "- ")
        .replace("</li>", "\n")
        .replace("<code>", "`")
        .replace("</code>", "`")
}

/// Export document text to Typst source.
pub fn text_to_typst(text: &str) -> String {
    if text.starts_with('#') {
        // Already Typst
        text.to_string()
    } else {
        // Assume Markdown
        markdown_to_typst(text)
    }
}

/// Compile Typst source to PDF.
pub fn to_pdf(source: &str, output_path: &str) -> Result<(), String> {
    let world = typst::World::new(Default::default());
    let document = typst::compile(source, &world)
        .map_err(|e| format!("Typst compile failed: {:?}", e))?;
    std::fs::write(output_path, &document)
        .map_err(|e| format!("Write PDF: {}", e))?;
    Ok(())
}

/// Save document as Typst source file.
pub fn save_typst(text: &str, path: &str) -> Result<(), String> {
    let typst_src = text_to_typst(text);
    std::fs::write(path, &typst_src).map_err(|e| format!("Write: {}", e))
}
