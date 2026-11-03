---
bundle:
  name: arxivchecker
  version: 0.1.0
  description: >-
    A study-to-arXiv capability: a portable method, traceable evidence and
    preflight helpers, an /arxiv mode, and a staged paper preparation recipe.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main#subdirectory=bundles/anchors/bundle.md
  - bundle: arxivchecker:behaviors/arxivchecker
---

@anchors:context/system.md
