---
created: 2025-03-02T14:34:38+08:00
modified: 2025-03-02T14:53:19+08:00
tags:
  - Programming/Python
  - TODO
title: Modern Python Packaging
---

## Building

```toml title="pyproject.toml"
#:schema https://json.schemastore.org/pyproject.json
# https://packaging.python.org/en/latest/specifications/pyproject-toml/

[build-system]
build-backend = "hatchling.build"
requires = ["hatch-vcs", "hatchling"]

[dependency-groups]
build = ["check-wheel-contents", "hatch", "twine"]
dev = []
docs = []
test = []

[project]
authors = [
  { email = "30631553+liblaf@users.noreply.github.com", name = "liblaf" },
]
classifiers = [
  "Development Status :: 4 - Beta",
  "License :: OSI Approved :: MIT License",
]
description = "Add your description here"
dynamic = ["version"]
keywords = []
license = "MIT"
name = "liblaf-grapes"
readme = "docs/README.md"
requires-python = ">=3.12"
dependencies = []

[project.urls]
"Changelog" = "https://github.com/liblaf/grapes/blob/main/CHANGELOG.md"
"Documentation" = "https://liblaf.github.io/grapes/"
"Homepage" = "https://github.com/liblaf/grapes"
"Issue Tracker" = "https://github.com/liblaf/grapes/issues"
"Release Notes" = "https://github.com/liblaf/grapes/releases"
"Source Code" = "https://github.com/liblaf/grapes"

[tool.check-wheel-contents]
ignore = ["W002"]

[tool.hatch.build.hooks.vcs]
version-file = "src/liblaf/grapes/_version.py"

[tool.hatch.build.targets.sdist]
only-include = ["src/"]

[tool.hatch.build.targets.wheel]
packages = ["src/liblaf"]

[tool.hatch.version]
source = "vcs"
```

```make
build:
    rm --force --recursive dist/
    pyproject-build
    check-wheel-contents dist/*.whl
    twine check --strict dist/*
```

TODO: introduce commonly used classifiers

## Versioning

TODO: introduce `hatch-vcs`, `release-please`

```yaml title=".github/workflows/release-please.yaml"
# This file is @generated by <https://github.com/liblaf/copier-release>.
# DO NOT EDIT!

name: Release Please

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  release-please:
    name: Release Please
    permissions:
      contents: write
      pull-requests: write
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-release-please
      cancel-in-progress: true
    outputs:
      created: ${{ steps.release-please.outputs.release_created }}
      pr: ${{ steps.release-please.outputs.pr }}
      tag: ${{ steps.release-please.outputs.tag_name }}
    steps:
      - id: release-please
        name: Release Please
        uses: googleapis/release-please-action@v4
        with:
          config-file: .github/release-please/config.json
          manifest-file: .github/release-please/.manifest.json
          token: ${{ github.token }}

  changelog-pr:
    name: Changelog (PR)
    permissions:
      contents: write
    needs:
      - release-please
    if: ${{ needs.release-please.outputs.pr }}
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-changelog-pr
      cancel-in-progress: true
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ fromJson(needs.release-please.outputs.pr).headBranchName }}
          token: ${{ github.token }}
          fetch-depth: 0
      - id: tag
        name: Parse Tag
        run: |-
          title="${{ fromJson(needs.release-please.outputs.pr).title }}"
          version=$(echo "$title" | awk '{ print $NF }')
          echo "tag=v$version" >> "$GITHUB_OUTPUT"
      - name: Changelog
        uses: liblaf/actions/changelog@main
        with:
          args: --tag "${{ steps.tag.outputs.tag }}"
          output: CHANGELOG.md
      - name: Commit
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore(docs): update CHANGELOG.md"
          file_pattern: CHANGELOG.md

  changelog-release:
    name: Changelog (Release)
    permissions:
      actions: write
      contents: write
    needs:
      - release-please
    if: ${{ needs.release-please.outputs.created }}
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-changelog-release
      cancel-in-progress: true
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ needs.release-please.outputs.tag }}
          fetch-depth: 0
      - id: changelog
        name: Changelog
        uses: liblaf/actions/changelog@main
        with:
          args: --current --strip all
      - name: Update Release
        run: gh release edit "${{ needs.release-please.outputs.tag }}" --notes-file "${{ steps.changelog.outputs.changelog }}"
        env:
          GH_TOKEN: ${{ github.token }}
      - name: Trigger Release Workflow
        run: |-
          WORKFLOW_FILES=(.github/workflows/{,shared-}release{.yaml,.yml})
          for workflow_file in "${WORKFLOW_FILES[@]}"; do
            if [[ -f $workflow_file ]]; then
              workflow_name=$(basename -- "$workflow_file")
              echo "::notice::Triggering workflow: $workflow_name"
              gh workflow run "$workflow_name" --ref "${{ needs.release-please.outputs.tag }}"
            fi
          done
        env:
          GH_TOKEN: ${{ github.token }}
```

## Publishing

```yaml title=".github/actions/release.yaml"
# This file is @generated by <https://github.com/liblaf/copier-python>.
# DO NOT EDIT!

name: Release

on:
  push:
  release:
    types:
      - published
  workflow_dispatch:

jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    outputs:
      artifact-name: ${{ steps.build.outputs.artifact-name }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - id: build
        name: Build and Inspect a Python Package
        uses: hynek/build-and-inspect-python-package@v2

  publish:
    name: Publish
    permissions:
      id-token: write
    needs:
      - build
    if: github.event_name == 'release' || startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-publish
      cancel-in-progress: true
    steps:
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: ${{ needs.build.outputs.artifact-name }}
          path: dist/
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

  pre-release:
    name: Pre-Release
    permissions:
      contents: write
    needs:
      - build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-pre-release
      cancel-in-progress: true
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: ${{ needs.build.outputs.artifact-name }}
          path: dist/
      - name: Create Pre-Release
        uses: liblaf/actions/release@main
        with:
          clobber: true
          files: dist/*
          prerelease: true
          tag: latest

  release:
    name: Release
    permissions:
      contents: write
    needs:
      - build
    if: github.event_name == 'release' || startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}-release
      cancel-in-progress: true
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Download Artifacts
        uses: actions/download-artifact@v4
        with:
          name: ${{ needs.build.outputs.artifact-name }}
          path: dist/
      - name: Upload Release Assets
        uses: liblaf/actions/release@main
        with:
          files: dist/*
          tag: ${{ github.event.release.tag_name || github.ref_name }}
```

## Release Workflow

1. commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
2. [Release Please](https://github.com/googleapis/release-please) analyzes commits and generate release PRs
3. User merge the release PR
4. CI pipeline builds, verifies and publishes packages

## References

- [liblaf/copier-python](https://github.com/liblaf/copier-python)
- [liblaf/grapes](https://github.com/liblaf/grapes)
- [Python Packaging User Guide](https://packaging.python.org/)
