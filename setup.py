#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# vim: set ts=2 sw=2 sts=2 et:


from setuptools import setup
import os
import sys
import shutil
from subprocess import Popen
from diovio import VERSION, AUTHOR, AUTHOR_EMAIL, URL, NAME, DESCRIPTION, LICENSE

#####################################################
#NOTE: The .deb generation via bdist_rpm override   #
#      requires: fakeroot, alien, dpkg-buildpackage #
#####################################################


#-- GOBAL VARS --#
LONG_DESCRIPTION = """%s
Author: %s <%s>
Project: %s
""" % ( DESCRIPTION, AUTHOR, AUTHOR_EMAIL, URL )

SCRIPTS=['diovio']
PACKAGES=[]
MANIFEST="""
include diovio
"""
DATA_FILES={}

#-- PYPI VARS --#
PYPI_DOWNLOAD_URL='https://github.com/diego-treitos/diovio/archive/v'+VERSION+'.tar.gz'
PYPI_DEPENS=['urllib3']
PYPI_KEYWORDS=['http', 'benchmark', 'web', 'performance', 'access.log', 'log', 'plot']


#-- DEB VARS --#
DEB_DEPENDS=['python-urllib3']
DEB_RECOMMENDS=['python-matplotlib']
DEB_SETUP_DIR='setup.files'


def sh_exec(cmdstr):
  return Popen(cmdstr, shell=True)


def presetup():
  """presetup"""
  # WRITE setup.cfg
  setupcfg = open('setup.cfg', 'w')
  setupcfg.write("""[bdist_rpm]\nbinary-only = 1""")
  setupcfg.close()

  # WRITE MANIFEST.in
  manifest = open('MANIFEST.in', 'w')
  manifest.write(MANIFEST)
  manifest.close()


def postsetup():
  """postsetup"""
  rpm_path=None
  for i in range( 1, 20 ):
    rpm_path='dist/'+NAME+'-'+VERSION+'-%d.noarch.rpm' % i
    if os.path.exists( rpm_path ):
      break

  cmd = sh_exec('fakeroot alien -gc %s' % rpm_path)
  if cmd.wait() == 0:
    pack_path=NAME+'-'+VERSION
    # Edit control file
    #
    control_lines = open(os.path.join(pack_path, 'debian/control')).readlines()
    control = open(os.path.join(pack_path, 'debian/control'), 'w')
    for line in control_lines:
      if line.lower().split(':')[0] == 'depends':
        # Add dependencies
        line= 'Depends: ' + ', '.join(DEB_DEPENDS) + '\n'
        # Add recommends
        line+='Recommends: ' + ', '.join(DEB_RECOMMENDS) + '\n'
      if line.lower().split(':')[0] == 'maintainer':
        line= 'Maintainer: ' + AUTHOR + ' <' + AUTHOR_EMAIL + '>\n'
      control.write(line)
    control.close()
    # Edit rules file
    #
    rules_lines = open(os.path.join(pack_path, 'debian/rules')).readlines()
    rules = open(os.path.join(pack_path, 'debian/rules'), 'w')
    for line in rules_lines:
      rules.write(line)
      if line.find('dh_installdirs') != -1:
        rules.write('\tdh_installinit\n')
        rules.write('\tdh_installcron\n')
        rules.write('\tdh_installifupdown\n')
        rules.write('\tdh_installlogrotate\n')
        rules.write('\tdh_installman\n')
    rules.close()
    # Add setup.files
    for sf in os.listdir( DEB_SETUP_DIR ):
      shutil.copyfile( os.path.join(DEB_SETUP_DIR, sf), os.path.join(pack_path, 'debian', sf) )
    cmd = sh_exec('cd %s; dpkg-buildpackage -us -uc -b' % pack_path)
    if cmd.wait() != 0:
      print("ERROR BUILDING .deb PACKAGE")


############################################################################
# PreSetup
if 'bdist_rpm' in sys.argv:
  presetup()

setup(
  name = NAME,
  version = VERSION,
  description = DESCRIPTION,
  long_description = LONG_DESCRIPTION,
  license = LICENSE,
  author = AUTHOR,
  author_email = AUTHOR_EMAIL,
  url = URL,
  # Name the folder where your packages live:
  # (If you have other packages (dirs) or modules (py files) then
  # put them into the package directory - they will be found
  # recursively.)
  packages = PACKAGES,
  # 'package' package must contain files (see list above)
  # I called the package 'package' thus cleverly confusing the whole issue...
  # This dict maps the package name =to=> directories
  # It says, package *needs* these files.
  package_data = DATA_FILES,
  # 'runner' is in the root.
  scripts = SCRIPTS,
  #
  # This next part it for the Cheese Shop, look a little down the page.
  # classifiers = []
  data_files = DATA_FILES,
)

# PostSetup
if 'bdist_rpm' in sys.argv:
  postsetup()
