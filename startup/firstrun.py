## \package startup.firstrun

# MIT licensing
# See: docs/LICENSE.txt


import os, wx

import util

from dbr.config          import ConfCode
from dbr.config          import InitializeConfig
from dbr.config          import default_config
from dbr.image           import GetBitmap
from dbr.language        import GT
from globals.application import APP_logo
from ui.dialog           import ShowErrorDialog
from ui.layout           import BoxSizer
from ui.style            import layout as lyt


logger = util.getLogger()

## Shows the first run dialog
def LaunchFirstRun(debreate_app):
  FR_dialog = FirstRun()
  debreate_app.SetTopWindow(FR_dialog)
  FR_dialog.ShowModal()

  init_conf_code = InitializeConfig()

  logger.debug("Configuration initialized: {}".format(init_conf_code == ConfCode.SUCCESS))

  if (init_conf_code != ConfCode.SUCCESS) or (not os.path.isfile(default_config)):
    msg_l1 = GT("An error occurred trying to create the configuration file:")
    msg_l2 = GT("Please report this error to Debreate's developers")
    ShowErrorDialog("{} {}\n\n{}".format(msg_l1, default_config, msg_l2))

    return init_conf_code

  FR_dialog.Destroy()

  # Delete first run dialog from memory
  del(FR_dialog)

  return init_conf_code


## Dialog shown when Debreate is run for first time
#
#  If configuration file is not found or corrupted
#  this dialog is shown.
class FirstRun(wx.Dialog):
  def __init__(self):
    wx.Dialog.__init__(self, None, wx.ID_ANY, GT("Debreate First Run"), size=(450,300))

    m2 = GT("This message only displays on the first run, or if\nthe configuration file becomes corrupted.")
    m3 = GT("The default configuration file will now be created.")
    m4 = GT("To delete this file, type the following command in a\nterminal:")

    message1 = GT("Thank you for using Debreate.")
    message1 = "{}\n\n{}".format(message1, m2)

    message2 = m3
    message2 = "{}\n{}".format(message2, m4)

    # Set the titlebar icon
    self.SetIcon(APP_logo)

    # Display a message to create a config file
    text1 = wx.StaticText(self, label=message1)
    text2 = wx.StaticText(self, label=message2)

    rm_cmd = wx.TextCtrl(self, value="rm -f ~/.config/debreate/config",
        style=wx.TE_READONLY|wx.BORDER_NONE)
    rm_cmd.SetBackgroundColour(self.BackgroundColour)

    layout_V1 = BoxSizer(wx.VERTICAL)
    layout_V1.Add(text1, 1)
    layout_V1.Add(text2, 1, wx.TOP, 15)
    layout_V1.Add(rm_cmd, 0, wx.EXPAND|wx.TOP, 10)

    # Show the Debreate icon
    icon = wx.StaticBitmap(self, bitmap=GetBitmap("logo", 64, "icon"))

    # Button to confirm
    self.button_ok = wx.Button(self, wx.ID_OK)

    # Nice border
    self.border = wx.StaticBox(self, -1)
    border_box = wx.StaticBoxSizer(self.border, wx.HORIZONTAL)
    border_box.AddSpacer(10)
    border_box.Add(icon, 0, wx.ALIGN_CENTER)
    border_box.AddSpacer(10)
    border_box.Add(layout_V1, 1, wx.ALIGN_CENTER)

    # Set Layout
    sizer = BoxSizer(wx.VERTICAL)
    sizer.Add(border_box, 1, wx.EXPAND|lyt.PAD_LR, 5)
    sizer.Add(self.button_ok, 0, wx.ALIGN_RIGHT|lyt.PAD_RB|wx.TOP, 5)

    self.SetSizer(sizer)
    self.Layout()
