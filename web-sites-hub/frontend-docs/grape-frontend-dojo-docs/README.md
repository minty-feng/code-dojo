# Frontend Tutorial - Sphinx Documentation Site

Sphinx static documentation site for Frontend Tutorial.

## Project Structure

```
frontend-docs/grape-frontend-dojo-docs/
├── conf.py              # Sphinx configuration file
├── index.rst            # Main index file
├── introduction.md      # Introduction page
├── requirements.txt     # Python dependencies
├── Makefile             # Build script
├── build.sh             # Initial build script
├── prepare-docs.sh      # Create symbolic links script
├── html/                # HTML documentation (symbolic links)
│   ├── index.rst
│   └── *.md -> ../../../grape-frontend-dojo/html/*.md
├── css/                 # CSS documentation
├── javascript/          # JavaScript documentation
├── react/               # React documentation
├── vue/                 # Vue documentation
├── angular/             # Angular documentation
└── typescript/          # TypeScript documentation
```

## Features

1. **No file copying**: Uses symbolic links, directly references source directory files
2. **Real-time updates**: Modifications to source files automatically reflect in documentation
3. **Space efficient**: No additional storage space required
4. **Independent management**: Source files and documentation build are separated

## Quick Start

### Initial Build

```bash
cd web-sites-hub/frontend-docs/grape-frontend-dojo-docs
./build.sh
```

### Subsequent Builds

```bash
# Using make (automatically creates links)
make html

# Or directly using sphinx-build
bash prepare-docs.sh  # Create links first
sphinx-build -b html . _build/html
```

### View Documentation

After building, open `_build/html/index.html` in your browser to view the documentation.

## Deployment

### Create Nginx Deployment Package

```bash
./package-nginx.sh
```

### Server Deployment

```bash
sudo bash deploy.sh frontend-docs-nginx-*.tar.gz
```

## Update Documentation

Document files are linked to source directory through symbolic links:

1. **Modify source files**: Edit files in `grape-frontend-dojo/html/` etc.
2. **Automatic effect**: Symbolic links automatically point to latest content
3. **Rebuild**:
   ```bash
   make html
   ```

## Symbolic Link Mechanism

- **Symbolic link location**: `frontend-docs/grape-frontend-dojo-docs/html/*.md`
- **Points to**: `../../../grape-frontend-dojo/html/*.md`
- **Auto-created**: Running `prepare-docs.sh` or `make html` automatically creates them
- **Real-time sync**: After modifying source files, symbolic links automatically point to latest content

## How It Works

1. `prepare-docs.sh` script creates symbolic links for each language's Markdown files
2. Symbolic links point to actual files in `../../grape-frontend-dojo/` directory
3. Sphinx reads symbolic links during build, actually accessing source files
4. After modifying source files, rebuild to see latest content
