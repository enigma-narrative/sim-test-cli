# mct

A CLI for managing a personal list of git "template" repositories and cloning
them under a new name to start a new project.

## Install

```bash
pip install git+https://github.com/jyurkiw/sim-template-cli.git
```

or with `uv`:

```bash
uv pip install git+https://github.com/jyurkiw/sim-template-cli.git
```

This installs an `mct` executable directly on your `PATH` — no `python -m`
or `uv run` prefix needed.

## Usage

### `mct init`

Create an `.mctrc` file in the current directory.

```bash
mct init --username jyurkiw [--template_site_path https://github.com] [template ...]
```

### `mct ls`

List all templates recorded in the active `.mctrc`.

```bash
mct ls
```

### `mct add`

Add template names to the active `.mctrc` (asks for confirmation).

```bash
mct add my-template another-template
```

### `mct rm`

Remove template names from the active `.mctrc` (asks for confirmation).

```bash
mct rm my-template
```

### `mct new`

Clone a template under a new name and point its remote at the new project's
(not-yet-necessarily-existing) repo URL.

```bash
mct new --template my-template my-new-project
```

## Configuration

`mct` searches the current directory and its parents (up to the drive root)
for an `.mctrc` file. The first one found is used.

```toml
template_site_path = "https://github.com"
username = "jyurkiw"
templates = ["my-template", "another-template"]
```

The full address of a repository is assembled as
`{template_site_path}/{username}/{repo_name}`.

## Documentation

Full docs: https://jyurkiw.github.io/sim-template-cli/
