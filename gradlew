#!/usr/bin/env sh
set -eu

GRADLE_VERSION="9.2.1"
GRADLE_HOME_BASE="${GRADLE_USER_HOME:-${HOME}/.gradle}/black-arcana-bootstrap"
GRADLE_INSTALL="${GRADLE_HOME_BASE}/gradle-${GRADLE_VERSION}"
DIST="gradle-${GRADLE_VERSION}-bin.zip"
DIST_URL="https://services.gradle.org/distributions/${DIST}"
CHECKSUM_URL="${DIST_URL}.sha256"

fetch() {
    if command -v curl >/dev/null 2>&1; then
        curl --fail --location --retry 3 --silent --show-error "$1" --output "$2"
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$1" -O "$2"
    else
        echo "Black Arcana Gradle bootstrap requires curl or wget." >&2
        exit 1
    fi
}

if [ ! -x "${GRADLE_INSTALL}/bin/gradle" ]; then
    command -v unzip >/dev/null 2>&1 || {
        echo "Black Arcana Gradle bootstrap requires unzip." >&2
        exit 1
    }

    mkdir -p "${GRADLE_HOME_BASE}"
    ZIP="${GRADLE_HOME_BASE}/${DIST}"
    SHA_FILE="${ZIP}.sha256"
    TMP="${GRADLE_HOME_BASE}/.gradle-${GRADLE_VERSION}-tmp-$$"

    fetch "${DIST_URL}" "${ZIP}"
    fetch "${CHECKSUM_URL}" "${SHA_FILE}"

    if command -v sha256sum >/dev/null 2>&1; then
        EXPECTED="$(tr -d '[:space:]' < "${SHA_FILE}")"
        ACTUAL="$(sha256sum "${ZIP}" | awk '{print $1}')"
    elif command -v shasum >/dev/null 2>&1; then
        EXPECTED="$(tr -d '[:space:]' < "${SHA_FILE}")"
        ACTUAL="$(shasum -a 256 "${ZIP}" | awk '{print $1}')"
    else
        echo "Black Arcana Gradle bootstrap requires sha256sum or shasum." >&2
        exit 1
    fi

    [ "${EXPECTED}" = "${ACTUAL}" ] || {
        echo "Gradle distribution checksum mismatch." >&2
        rm -f "${ZIP}" "${SHA_FILE}"
        exit 1
    }

    rm -rf "${TMP}"
    mkdir -p "${TMP}"
    unzip -q "${ZIP}" -d "${TMP}"
    rm -rf "${GRADLE_INSTALL}"
    mv "${TMP}/gradle-${GRADLE_VERSION}" "${GRADLE_INSTALL}"
    rm -rf "${TMP}" "${ZIP}" "${SHA_FILE}"
fi

exec "${GRADLE_INSTALL}/bin/gradle" "$@"
