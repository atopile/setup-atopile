import os
from ruamel.yaml import YAML
from pathlib import Path

yaml = YAML()


def main():
    if os.environ.get("ATO_CONFIG") and os.environ.get("SPECIFIED_VERSION"):
        raise ValueError("Cannot specify both ATO_CONFIG and SPECIFIED_VERSION")

    if specified_version := os.environ.get("SPECIFIED_VERSION"):
        print(f"version={specified_version}")
        return

    ato_config = os.environ.get("ATO_CONFIG")
    DEFAULT_ATO_CONFIG = Path("ato.yaml")
    if ato_config or not DEFAULT_ATO_CONFIG.is_file():
        if not ato_config:
            ato_config = DEFAULT_ATO_CONFIG

        with open(ato_config, "r") as f:
            config = yaml.load(f)
            requires_atopile = config["requires-atopile"]
            # FIXME: this is the dumbest way to do this
            atopile_version = requires_atopile.split(",")[0].strip("^=><* ")
            print(f"version={atopile_version}")

    raise RuntimeError("No version specified or detected.")


if __name__ == "__main__":
    main()
