#!/usr/bin/env bash
set -euo pipefail

# Install the same scientific environment used by Binder inside the workspace.
# No system package repositories or global Python installations are changed.
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"
if [[ "$(uname -s)" != Linux ]]; then
  printf 'This bootstrap is for the Linux devcontainer. Use the Mac launchers locally.\n' >&2
  exit 1
fi
case "$(uname -m)" in
  x86_64) mamba_platform=linux-64 ;;
  aarch64|arm64) mamba_platform=linux-aarch64 ;;
  *) printf 'Unsupported Linux architecture: %s\n' "$(uname -m)" >&2; exit 1 ;;
esac
for required in curl tar; do
  command -v "$required" >/dev/null || { printf 'Missing bootstrap tool: %s\n' "$required" >&2; exit 1; }
done

runtime_dir="$repo_dir/.runtime"
mamba="$runtime_dir/bin/micromamba"
env_dir="$runtime_dir/env"
export MAMBA_ROOT_PREFIX="$runtime_dir/mamba-root"
mkdir -p "$runtime_dir/bin" "$MAMBA_ROOT_PREFIX"
if [[ ! -x "$mamba" ]]; then
  archive="$(mktemp "$runtime_dir/micromamba-download.XXXXXX")"
  trap 'rm -f "$archive"' EXIT
  curl --fail --location --retry 3 \
    "https://micro.mamba.pm/api/micromamba/$mamba_platform/latest" --output "$archive"
  tar -xjf "$archive" -C "$runtime_dir" bin/micromamba
  chmod u+x "$mamba"
  rm -f "$archive"
  trap - EXIT
fi

if [[ -f "$env_dir/conda-meta/history" ]]; then
  "$mamba" env update --yes --prefix "$env_dir" --file binder/environment.yml
else
  "$mamba" create --yes --prefix "$env_dir" --file binder/environment.yml
fi
export PATH="$env_dir/bin:$runtime_dir/bin:$PATH"
"$mamba" run --prefix "$env_dir" bash binder/postBuild

echo
echo "Workshop environment is ready with hash-verified real ACCESS-CM2 inputs."
echo "Open notebooks/00_yl_20_minute_binder_demo.ipynb to begin."
