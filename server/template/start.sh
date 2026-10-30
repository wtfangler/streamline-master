#!/usr/bin/env bash
# @PACK@ server. Set JAVA_EXE to a Java @JAVA@+ binary if it is not on PATH.
set -euo pipefail
cd -- "$(dirname -- "$0")"
JAVA_EXE="${JAVA_EXE:-java}"
version="$("$JAVA_EXE" -version 2>&1 | sed -n 's/.*version "\([^"]*\)".*/\1/p' | head -n 1)" || version=""
major="${version%%[.+-]*}"
if [[ ! "$major" =~ ^[0-9]+$ ]] || (( major < @JAVA@ )); then
    printf 'Java @JAVA@ or newer is required. Found: %s\nSet JAVA_EXE to the Java @JAVA@ binary path.\n' "${version:-not available}" >&2
    exit 1
fi
if [[ ! -f fabric-server-launch.jar ]]; then
    printf 'Missing fabric-server-launch.jar. Complete the server build first.\n' >&2
    exit 1
fi
exec "$JAVA_EXE" -Xms1G -Xmx@RAM@ @JVM@ -jar fabric-server-launch.jar nogui
