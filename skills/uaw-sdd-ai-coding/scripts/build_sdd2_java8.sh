#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE="$SCRIPT_DIR/Sdd2Control.java"
MANIFEST="$SCRIPT_DIR/java8/MANIFEST.MF"
RUNTIME_DIR="$SCRIPT_DIR/runtime"
TARGET="$RUNTIME_DIR/sdd2-control.jar"
CHECKSUM="$RUNTIME_DIR/sdd2-control.sha256"
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/sdd2-java8-build.XXXXXX")

cleanup() {
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT HUP INT TERM

if ! command -v javac >/dev/null 2>&1; then
  echo "构建失败：未检测到 javac。维护者需要 JDK 9 及以上版本以使用 --release 8 构建 Java 8 兼容 JAR。" >&2
  exit 2
fi

if ! command -v jar >/dev/null 2>&1; then
  echo "构建失败：未检测到 jar 命令。请安装完整 JDK 后重试。" >&2
  exit 2
fi

mkdir -p "$RUNTIME_DIR"
javac --release 8 -Xlint:all -encoding UTF-8 -d "$BUILD_DIR" "$SOURCE"
jar cfm "$TARGET" "$MANIFEST" -C "$BUILD_DIR" .

if command -v shasum >/dev/null 2>&1; then
  DIGEST_OUTPUT=$(shasum -a 256 "$TARGET")
elif command -v sha256sum >/dev/null 2>&1; then
  DIGEST_OUTPUT=$(sha256sum "$TARGET")
else
  echo "构建失败：未检测到 shasum 或 sha256sum，无法生成运行时完整性文件。" >&2
  exit 2
fi
JAR_SHA256=${DIGEST_OUTPUT%% *}
printf '%s\n' "$JAR_SHA256" > "$CHECKSUM"

echo "已生成 Java 8 兼容控制器：$TARGET"
echo "已生成运行时完整性文件：$CHECKSUM"
