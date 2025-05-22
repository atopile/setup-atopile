# Setup the atopile CLI in Github Actions

A Github action to run atopile CLI ⚙️🚀

## Configuration

Use this action to run `ato` commands within your GitHub Actions workflows. You can specify the `atopile` version explicitly or derive it from a configuration file.

```yaml .github/workflows/main.yml
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: atopile/setup-atopile@v1
        with:
          # Either: derive the version from a config file (e.g., pyproject.toml or ato.yaml)
          # [Recommended and default if neither are provided]
          ato-config: "ato.yaml"
          # Or: Specify the atopile version directly
          version: "0.3.23"
          # Optionally: specify a working directory to look for ato.yaml
          working-directory: "packages/my-package"

      # Do something!
      - run: ato --version
```

## Working with Multiple Packages

You can use this action with multiple packages in different directories:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: [package1, package2, package3]
    steps:
      - uses: actions/checkout@v4
      - uses: atopile/setup-atopile@v1
        with:
          working-directory: ${{ matrix.package }}
      - run: ato sync
        working-directory: ${{ matrix.package }}
      - run: ato build
        working-directory: ${{ matrix.package }}
```

See the [action.yml](action.yml) for full details.
