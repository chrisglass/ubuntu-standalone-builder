#!/usr/bin/env python
from __future__ import print_function

import argparse
import sys


TEMPLATE = """\
#cloud-config
packages:
- bzr
runcmd:
# Setup environment
- export HOME=/home/ubuntu
- export BUILD_ID=output
- export CHROOT_ROOT=/home/ubuntu/build-$BUILD_ID/chroot-autobuild

# Setup build chroot
- wget http://cloud-images.ubuntu.com/releases/xenial/release/ubuntu-16.04-server-cloudimg-amd64-root.tar.xz -O /tmp/root.tar.xz
- mkdir -p $CHROOT_ROOT
- tar -C $CHROOT_ROOT -x -f /tmp/root.tar.xz
- mkdir $CHROOT_ROOT/build
- rm $CHROOT_ROOT/etc/resolv.conf  # We need to write over this symlink

# Pull in build scripts
- bzr branch lp:launchpad-buildd /home/ubuntu/launchpad-buildd

# Perform the build
- /home/ubuntu/launchpad-buildd/mount-chroot $BUILD_ID
- /home/ubuntu/launchpad-buildd/update-debian-chroot $BUILD_ID{}
- /home/ubuntu/launchpad-buildd/buildlivefs --arch amd64 --project ubuntu-cpc --series xenial --build-id $BUILD_ID
- /home/ubuntu/launchpad-buildd/umount-chroot $BUILD_ID
- mkdir /home/ubuntu/images
- mv $CHROOT_ROOT/build/livecd.ubuntu-cpc.* /home/ubuntu/images
"""


def _write_cloud_config(output_file, ppa=""):
    """
    Write an image building cloud-config file to a given location.

    :param output_file:
        The path for the file to write to.
    :param ppa:
        An optional extra PPA to inject in the build chroot.
    """
    
    if ppa:
        # If we passed a PPA, inject a line in the template.
        ppa = "\n- chroot $CHROOT_ROOT -- add-apt-repository -y -u {}".format(ppa)
        
    contents = TEMPLATE.format(ppa)
        
    with open(output_file, 'w') as f:
        f.write(contents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_filename')
    parser.add_argument('--ppa', dest='ppa', default="")
    args = parser.parse_args()

    _write_cloud_config(args.output_filename, ppa=args.ppa)


if __name__ == '__main__':
    main()
