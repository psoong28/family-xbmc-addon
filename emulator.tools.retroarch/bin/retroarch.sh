#!/bin/sh

. /etc/profile

oe_setup_addon emulator.tools.retroarch

systemd-run $ADDON_DIR/bin/retroarch.start "$@"
