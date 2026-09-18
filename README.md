<!-- version: 1.0.0 | build: 2026-09-18 | update: 2026-09-18 -->
# msr-validator

The reference validator library for [MSR JSON](https://github.com/msr-standard/specification)
manifests, in Python.

> **Status: not yet released.** This repository holds the structure and the
> rules the implementation will follow. Nothing is published on PyPI yet. To
> validate a manifest today, see [AGENTS.md in the specification](https://github.com/msr-standard/specification/blob/main/AGENTS.md#validate).

## Role in the MSR JSON project

```
msr-standard/specification   source of truth: schemas, examples, RFCs
        ▲
        │  bundles the schema of a pinned release tag
msr-standard/msr-validator   this repository: the library
        ▲
        │  depends on
msr-standard/msr-cli         the `msr` command-line tool
```

Dependencies point one way only. This library never depends on the CLI, and the
specification depends on nothing.

Its first consumers are software registries — such as mysoftrank.com — that
must validate every manifest they index. A registry that imports this package
instead of keeping its own copy of the schema cannot drift from the standard.

## Rules this implementation follows

- **No committed copy of the schema.** The package ships the canonical schema so
  it can validate offline, but that file is generated at build time from a
  pinned release tag of `msr-standard/specification`, is gitignored, and CI
  fails if it is not byte-identical to that tag.
- **The supported protocol version is explicit.** Each release states which
  MSR JSON versions it validates.
- **Python**, published on PyPI as `msr-validator`.

## Author

MSR JSON was created by Antonio Santos. See the
[specification's AUTHORS](https://github.com/msr-standard/specification/blob/main/AUTHORS).

## License

[MIT](LICENSE). The specification and schemas it validates against are
CC-BY-4.0, in the specification repository.
