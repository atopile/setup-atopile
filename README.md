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
          # [Recommended]
          ato-config: "ato.yaml"
          # Or: Specify the atopile version directly
          version: "0.3.23"

      # Do something!
      - run: ato --version
```

See the [action.yml](action.yml) for full details.
