#!/bin/bash
set -o errexit -o nounset -o pipefail

command rsync --info="progress2" --archive --force --stats --human-readable --progress --itemize-changes "$HOME/SeaDrive/My Libraries/webdav/obsidian/" .
