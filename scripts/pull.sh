#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail

command rsync --info="progress2" --archive --force --stats --human-readable --progress --itemize-changes "$HOME/net/SeaDrive/My Libraries/webdav/obsidian/" .
