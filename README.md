<!-- version: 1.1.0 | build: 2026-09-20 | update: 2026-09-20 -->
# msr-validator

The reference validator library for [MSR JSON](https://github.com/msrjson/specification)
manifests, in Python.

> **Status: implementation in progress.** Nothing is published on PyPI yet.

## Role in the MSR JSON project

```
msrjson/specification        source of truth: schemas, examples, RFCs
        ▲
        │  bundles the schema of a pinned release tag
msrjson/msr-validator        this repository: the library
        ▲
        │  depends on
msrjson/msr-cli              the `msr` command-line tool
```

Dependencies point one way only. This library never depends on the CLI, and the
specification depends on nothing.

Its first consumers are software registries — such as mysoftrank.com — that
must validate every manifest they index. A registry that imports this package
instead of keeping its own copy of the schema cannot drift from the standard.

## Rules this implementation follows

- **No committed copy of the schema.** The package ships the canonical schema so
  it can validate offline, but that file is generated at build time from a
  pinned release tag of `msrjson/specification`, is gitignored, and CI
  fails if it is not byte-identical to that tag.
- **The supported protocol version is explicit.** Each release states which
  MSR JSON versions it validates.
- **Python**, published on PyPI as `msr-validator`.

## API

```python
from msr_validator import validate

result = validate(open(".well-known/msr.json").read())
if not result.valid:
    for error in result.errors:
        print(error.path, error.message)
```

The package validates offline against the byte-pinned schema from specification
tag `v2.0.0`. Build time downloads that schema, verifies its SHA-256 digest and
includes it in the wheel; source control never includes a second schema copy.

## Author

MSR JSON was created by Antonio Santos. See the
[specification's AUTHORS](https://github.com/msrjson/specification/blob/main/AUTHORS).

## License

[MIT](LICENSE). The specification and schemas it validates against are
CC-BY-4.0, in the specification repository.
