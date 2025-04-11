import os
from ruamel.yaml import YAML

yaml = YAML()


def main():
    if os.environ.get("ATO_CONFIG") and os.environ.get("SPECIFIED_VERSION"):
        raise ValueError("Cannot specify both ATO_CONFIG and SPECIFIED_VERSION")

    if specified_version := os.environ.get("SPECIFIED_VERSION"):
        print(f"version={specified_version}")
    elif ato_config := os.environ.get("ATO_CONFIG"):
        with open(ato_config, "r") as f:
            config = yaml.load(f)
            requires_atopile = config["requires-atopile"]
            # FIXME: this is the dumbest way to do this
            atopile_version = requires_atopile.split(",")[0].strip("^=><* ")
            print(f"version={atopile_version}")
    else:
        raise ValueError("No ATO_CONFIG or SPECIFIED_VERSION provided")


if __name__ == "__main__":
    main()
