# Basic Conversion - Standard Converters

This document lists all Standard Converter combinations available in PanConvert.

## Standard Converter Combinations

The following conversion pairs are predefined as standard converters:

### From Markdown
| From Format | To Format | Extra Parameters |
|-------------|-----------|------------------|
| markdown | latex | --standalone |
| markdown | opml | --standalone |
| markdown | lyx | (via LyX converter) |
| markdown | html | --standalone |

### From Opml
| From Format | To Format | Extra Parameters |
|-------------|-----------|------------------|
| opml | markdown | (none) |
| opml | latex | --standalone |
| opml | html | --standalone |

### From Latex
| From Format | To Format | Extra Parameters |
|-------------|-----------|------------------|
| latex | markdown | (none) |
| latex | opml | --standalone |
| latex | html | --standalone |
| latex | epub | --output=/Users/apaeffgen/Downloads/Output_Panconvert.epub;--standalone |

### From Html
| From Format | To Format | Extra Parameters |
|-------------|-----------|------------------|
| html | markdown | (none) |
| html | opml | --standalone |
| html | latex | --standalone |

## Summary

**Total Standard Converter Combinations: 15**

- **Markdown** as source: 4 conversions (to latex, opml, lyx, html)
- **Opml** as source: 3 conversions (to markdown, latex, html)
- **Latex** as source: 4 conversions (to markdown, opml, html, epub)
- **Html** as source: 4 conversions (to markdown, opml, latex)

## Notes

- Standard converters work with both single-file and batch conversion modes.
- The LyX converter requires multimarkdown to be installed separately.
- The EPUB converter from Latex has a hardcoded output path to `/Users/apaeffgen/Downloads/Output_Panconvert.epub`.
- When using standard converters in batch mode, the same conversion pairs are available.
