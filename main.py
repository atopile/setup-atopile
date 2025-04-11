import os
from ruamel.yaml import YAML

yaml = YAML()


def main():
    if os.environ.get("ATO_CONFIG") and os.environ.get("SPECIFIED_VERSION"):
        raise ValueError("Cannot specify both ATO_CONFIG and SPECIFIED_VERSION")

    if specified_version := os.environ.get("SPECIFIED_VERSION"):
        print(f"version={specified_version}")
        return

    ato_config = os.environ.get("ATO_CONFIG", "ato.yaml")
    with open(ato_config, "r") as f:
        config = yaml.load(f)
        requires_atopile = config["requires-atopile"]
        # FIXME: this is the dumbest way to do this
        atopile_version = requires_atopile.split(",")[0].strip("^=><* ")
        print(f"version={atopile_version}")


if __name__ == "__main__":
    main()
