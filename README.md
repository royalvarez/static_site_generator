# Static Site Generator

## Overview

Static Site Generator generates webpages from markdown files and static assets.

The Static Site Generator is a command line tool making website generation simple. The generator copies static assets like images and CSS, parsing through markdown files contained in the content directory, converts each markdown file to HTML, and generates static webpages at a destination path to serve to the website.

## Features

- **Markdown to HTML conversion** recursively converts files from .md to .html.
- **Template engine** wraps generated content inside template.html.
- **Asset copying** moves all static files (images, css) to the directory serving the webpages.
- **Block and Inline parsing** supports paragraphs, headers, code blocks, blockquotes, lists, bold, italic, images and links.
- **Base path support** configurable base path for seamless hosting on custom root paths.

## Installation

### Prerequisites

- Python 3.13+

### Clone The Repository

```bash
git clone https://github.com/royalvarez/static_site_generator.git
cd static_site_generator
```

## Usage

Run the static site generator in the terminal
```bash
./build.sh <base path>
```

### Example

```bash
./build.sh "/begin_project/"
```

When no argument is given to the command line, the default base path becomes `"/"`.

## License

This project is licensed under the [MIT License](./LICENSE).