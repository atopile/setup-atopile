import os
from pathlib import Path

import httpx
from ruamel.yaml import YAML
from semver import Version

yaml = YAML()


def parse(version_str: str) -> Version:
    """
    Robustly parse versions, even if a little wonky

    semver package is very strict about matching the semver spec
    spec for reference: https://semver.org/
    if we can't parse the version string, it's most likely because
    hatch uses "." as a separator between the version number and
    prerelease/build information, but semver requires "-"
    we are going to support hatch's shenanigans by splitting and
    reconstituting the string
    hatch example: "0.0.17.dev0+g0151069.d20230928"
    """
    if version_str.startswith("v"):
        version_str = version_str[1:]

    try:
        version = Version.parse(version_str)
    except ValueError:
        dot_split = version_str.split(".")
        version_str = "-".join(
            ".".join(fragments) for fragments in (dot_split[:3], dot_split[3:])
        )
        version = Version.parse(version_str)

    return version


def clean_version(verion: Version) -> Version:
    """
    Clean a version by dropping any prerelease or build information
    """
    return Version(
        verion.major,
        verion.minor,
        verion.patch,
    )


OPERATORS = ("*", "^", "~", "!", "==", ">=", "<=", ">", "<")


def match(spec: str, version: Version) -> bool:
    """
    Check if a version matches a given specifier

    :param spec: the specifier to match against
    :param version: the version to check
    :return: True if the version matches the specifier, False otherwise
    """
    # first clean up the spec string
    spec = spec.strip()

    if spec == "*":
        return True

    if "||" in spec:
        for s in spec.split("||"):
            if match(s, version):
                return True
        return False

    if "," in spec:
        for s in spec.split(","):
            if not match(s, version):
                return False
        return True

    for operator in OPERATORS:
        if spec.startswith(operator):
            specd_version = parse(spec[len(operator) :])
            break
    else:
        # if there's not operator, default to ^ (up to next major)
        specd_version = parse(spec)
        operator = "^"

    if operator == "^":
        # semver doesn't support ^, so we have to do it ourselves
        # ^1.2.3 is equivalent to >=1.2.3 <2.0.0
        return version >= specd_version and version < specd_version.bump_major()

    if operator == "~":
        # semver doesn't support ~, so we have to do it ourselves
        # ~1.2.3 is equivalent to >=1.2.3 <1.3.0
        return version >= specd_version and version < specd_version.bump_minor()

    if operator == "!":
        return version != specd_version

    if operator == "==":
        return version == specd_version

    if operator == ">=":
        return version >= specd_version

    if operator == "<=":
        return version <= specd_version

    if operator == ">":
        return version > specd_version

    if operator == "<":
        return version < specd_version

    else:
        raise ValueError(f"Invalid operator: {operator}")


def get_released_versions() -> list[Version]:
    response = httpx.get("https://pypi.org/pypi/atopile/json", timeout=3)
    response.raise_for_status()

    versions = []
    for version in response.json()["releases"]:
        try:
            versions.append(parse(version))
        except ValueError:
            pass

    return versions


def main():
    if os.environ.get("ATO_CONFIG") and os.environ.get("SPECIFIED_VERSION"):
        raise ValueError("Cannot specify both ATO_CONFIG and SPECIFIED_VERSION")

    if specified_version := os.environ.get("SPECIFIED_VERSION"):
        print(f"version={specified_version}")
        return

    # Handle working directory
    working_directory = os.environ.get("WORKING_DIRECTORY", ".")
    working_path = Path(working_directory)

    ato_config = os.environ.get("ATO_CONFIG")
    if ato_config:
        # If ATO_CONFIG is specified, use it as-is (could be absolute or relative)
        config_path = Path(ato_config)
    else:
        # Default to ato.yaml in the working directory
        config_path = working_path / "ato.yaml"

    if ato_config or config_path.is_file():
        with open(config_path, "r") as f:
            config = yaml.load(f)
            requires_atopile = config["requires-atopile"]
            available_versions = get_released_versions()

            for semver_candidate in sorted(available_versions, reverse=True):
                if semver_candidate.build or semver_candidate.prerelease:
                    continue

                if match(requires_atopile, semver_candidate):
                    print(
                        f"version={semver_candidate.major}.{semver_candidate.minor}.{semver_candidate.patch}"
                    )
                    return

    raise RuntimeError("No version specified or detected.")


if __name__ == "__main__":
    main()
