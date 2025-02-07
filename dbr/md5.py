## \package dbr.md5

# MIT licensing
# See: docs/LICENSE.txt


import os

import util

from dbr.language    import GT
from globals.execute import GetCommandOutput
from globals.execute import GetExecutable
from globals.ident   import chkid
from globals.ident   import pgid
from libdbr.fileio   import writeFile
from ui.dialog       import ErrorDialog
from wiz.helper      import GetField
from wiz.helper      import GetMainWindow


logger = util.getLogger()

## Creates a file of md5 hashes for files within the staged directory
#
#  FIXME: Should binary files be handled differently?
#  \param stage_dir
#  Temporary directory to scan files into list
#  \param parent
#  The window to be parent of error messages
def WriteMD5(stage_dir, parent=None):
  CMD_md5sum = GetExecutable("md5sum")

  # Show an error if the 'md5sum' command does not exist
  # This is only a failsafe & should never actually occur
  if not CMD_md5sum:
    if not parent:
      parent = GetMainWindow()

    md5_label = GetField(pgid.BUILD, chkid.MD5).GetLabel()

    err_msg1 = GT("The \"md5sum\" command was not found on the system.")
    err_msg2 = GT("Uncheck the \"{}\" box.").format(md5_label)
    err_msg3 = GT("Please report this error to one of the following addresses:")
    err_url1 = "https://github.com/AntumDeluge/debreate/issues"
    err_url2 = "https://sourceforge.net/p/debreate/bugs/"

    logger.error("{} {} {}\n\t{}\n\t{}".format(err_msg1, err_msg2, err_msg3, err_url1, err_url2))

    md5_error = ErrorDialog(parent, text="{}\n{}\n\n{}".format(err_msg1, err_msg2, err_msg3))
    md5_error.AddURL(err_url1)
    md5_error.AddURL(err_url2)
    md5_error.ShowModal()

    return None

  temp_list = []
  md5_list = [] # Final list used to write the md5sum file
  for ROOT, DIRS, FILES in os.walk(stage_dir):
    # Ignore the 'DEBIAN' directory
    if os.path.basename(ROOT) == "DEBIAN":
      continue

    for F in FILES:
      F = "{}/{}".format(ROOT, F)

      md5 = GetCommandOutput(CMD_md5sum, ("-t", F))

      logger.debug("WriteMD5: GetCommandOutput: {}".format(md5))

      temp_list.append(md5)

  for item in temp_list:
    # Remove [stage_dir] from the path name in the md5sum so that it has a
    # true unix path
    # e.g., instead of "/myfolder_temp/usr/local/bin", "/usr/local/bin"
    sum_split = item.split("{}/".format(stage_dir))
    sum_join = "".join(sum_split)
    md5_list.append(sum_join)

  # Create the md5sums file in the "DEBIAN" directory
  # NOTE: lintian ignores the last character of the file, so should end with newline character (\n)
  return writeFile("{}/DEBIAN/md5sums".format(stage_dir), "{}\n".format("\n".join(md5_list)))
