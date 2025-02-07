## \package ui.buttons
#
#  Custom buttons for application

# MIT licensing
# See: docs/LICENSE.txt


import os, wx

import util

from dbr.containers  import Contains
from fields.cmdfield import CommandField
from globals.ident   import btnid
from globals.paths   import getBitmapsDir
from globals.strings import GS
from globals.strings import IsString
from ui.layout       import BoxSizer
from ui.style        import layout as lyt


logger = util.getLogger()

## Standard button that inherits CommandField
class Button(wx.Button, CommandField):
  def __init__(self, parent, btnId=wx.ID_ANY, label=wx.EmptyString, pos=wx.DefaultPosition,
      size=wx.DefaultSize, style=0, name=wx.ButtonNameStr, commands=None, requireAll=False):

    wx.Button.__init__(self, parent, btnId, label, pos, size, style, name=name)
    CommandField.__init__(self, commands, requireAll)


## The same as wx.BitmapButton but defaults to style=wx.NO_BORDER
class CustomButton(wx.BitmapButton, CommandField):
  def __init__(self, parent, bitmap, btnId=wx.ID_ANY, pos=wx.DefaultPosition,
      size=wx.DefaultSize, style=wx.NO_BORDER, validator=wx.DefaultValidator,
      name=wx.ButtonNameStr, commands=None, requireAll=False):

    if not isinstance(bitmap, wx.Bitmap):
      bitmap = wx.Bitmap(bitmap)

    wx.BitmapButton.__init__(self, parent, btnId, bitmap, pos, size, style|wx.NO_BORDER,
        validator, name)
    CommandField.__init__(self, commands, requireAll)


## TODO: Doxygen
class LayoutButton(BoxSizer):
  def __init__(self, button, label, parent=None, btnId=wx.ID_ANY, size=32,
      tooltip=None, name=None, showLabel=True):

    BoxSizer.__init__(self, wx.VERTICAL)

    if IsString(button):
      self.Button = CreateButton(parent, btnId, label, button, size, tooltip, name)

    else:
      self.Button = button

    self.Add(self.Button, 1, wx.ALIGN_CENTER)

    if isinstance(self.Button, CustomButton):
      if not label:
        label = self.Button.Name

      self.Label = wx.StaticText(self.Button.GetParent(), label=label)

      self.Add(self.Label, 0, wx.ALIGN_CENTER)

      self.Show(self.Label, showLabel)


  ## TODO: Doxygen
  def Bind(self, eventType, eventHandler):
    self.Button.Bind(eventType, eventHandler)


  ## TODO: Doxygen
  def GetLabel(self):
    if isinstance(self.Button, CustomButton):
      return self.Label.GetLabel()

    return self.Button.GetLabel()


  ## TODO: Doxygen
  def LabelIsShown(self):
    if not isinstance(self.Button, CustomButton):
      # Instance is a wx.Button
      return True

    return self.IsShown(self.Label)


  ## TODO: Doxygen
  def ShowLabel(self, show=True):
    self.Show(self.Label, show)


## BoxSizer class to distinguish between other sizers
class ButtonSizer(BoxSizer):
  def __init__(self, orient):
    BoxSizer.__init__(self, orient)


  ## TODO: Doxygen
  def Add(self, button, proportion=0, flag=0, border=0, label=None, userData=None):
    # FIXME: Create method to call from Add & Insert methods & reduce code
    if isinstance(button, LayoutButton):
      add_object = button

    else:
      if isinstance(button, CustomButton):
        if label == None:
          label = button.GetToolTipText()

        add_object = BoxSizer(wx.VERTICAL)
        add_object.Add(button, 0, wx.ALIGN_CENTER)
        add_object.Add(wx.StaticText(button.Parent, label=label), 0, wx.ALIGN_CENTER_HORIZONTAL)

      else:
        add_object = button

    return BoxSizer.Add(self, add_object, proportion, flag, border, userData)


  ## TODO: Doxygen
  def HideLabels(self):
    self.ShowLabels(False)


  ## TODO: Doxygen
  def Insert(self, index, button, proportion=0, flag=0, border=0, label=None, userData=None):
    if isinstance(button, CustomButton):
      if label == None:
        label = button.GetToolTipText()

      add_object = BoxSizer(wx.VERTICAL)
      add_object.Add(button, 0, wx.ALIGN_CENTER)
      add_object.Add(wx.StaticText(button.Parent, label=label), 0, wx.ALIGN_CENTER_HORIZONTAL)

    else:
      add_object = button

    return BoxSizer.Insert(self, index, add_object, proportion, flag, border, userData)


  ## Changes label for all buttons with specified ID
  #
  #  \param btnId
  #  \b \e Integer ID of buttons to change labels
  #  \param newLabel
  #  New \b \e string label for button
  #  \return
  #  \b \e True if matching button found
  def SetLabel(self, btnId, newLabel):
    label_set = False

    for SI in self.GetChildren():
      btn_objects = SI.GetSizer()
      if btn_objects:
        btn_objects = btn_objects.GetChildren()

        button = btn_objects[0].GetWindow()

        if button and button.GetId() == btnId:
          if isinstance(button, CustomButton):
            static_text = btn_objects[1].GetWindow()
            static_text.SetLabel(newLabel)
            button.SetToolTip(newLabel)

            label_set = True

          else:
            button.SetLabel(newLabel)
            button.SetToolTip(newLabel)

            label_set = True

    return label_set


  ## Show or hide text labels
  def ShowLabels(self, show=True):
    buttons = self.GetChildren()

    if buttons:
      for SIZER in self.GetChildren():
        SIZER = SIZER.GetSizer()

        if SIZER:
          label = SIZER.GetChildren()[1]
          label.Show(show)

      window = self.GetContainingWindow()
      if window:
        window.Layout()


## TODO: Doxygen
#
#  \param button_ids
#  \b \e List of IDs of buttons to be added
#  \param parent_sizer
#  The \b \e wx.Sizer instance that the buttons sizer should be added to
#  \param show_labels:
#  If True, button labels will be shown on custom button instances
#  \param reverse
#  Reverse order of buttons added
#  \return
#  \b \e ui.button.ButtonSizer instance containing the buttons
def AddCustomButtons(window, button_ids, parent_sizer=None, show_labels=True, reverse=True,
      flag=wx.ALIGN_RIGHT|lyt.PAD_RB, border=5):
  lyt_buttons = ButtonSizer(wx.HORIZONTAL)

  if reverse:
    button_ids = reversed(button_ids)

  for ID in button_ids:
    new_button = CreateButton(window, ID)
    lyt_buttons.Add(new_button, 0, wx.ALIGN_CENTER)

  lyt_buttons.ShowLabels(show_labels)

  if isinstance(parent_sizer, wx.BoxSizer):
    parent_sizer.Add(lyt_buttons, 0, flag, border)

    return None

  # parent_sizer is boolean
  elif parent_sizer:
    window.GetSizer().Add(lyt_buttons, 0, flag, border)

    return None

  return lyt_buttons


## Find sizer instance that contains buttons
#
#  Helper function for ReplaceStandardButtons
#
#  \param sizer
#  \b \e wx.Sizer or \b \e wx.Window instance to search for child button sizer
def GetButtonSizer(sizer):
  if isinstance(sizer, wx.Window):
    sizer = sizer.GetSizer()

  if isinstance(sizer, (ButtonSizer, wx.StdDialogButtonSizer)):
    return sizer

  for S in sizer.GetChildren():
    S = S.GetSizer()

    if S:
      S = GetButtonSizer(S)

      if S:
        return S


def _get_containing_sizer(parent, sizer):
  if isinstance(parent, wx.Window):
    parent = parent.GetSizer()

  if not parent or parent == sizer:
    return None

  if Contains(parent, sizer):
    return parent

  for S in parent.GetChildren():
    S = S.GetSizer()

    if S:
      S = _get_containing_sizer(S, sizer)

      if S:
        return S


## Replaces standard dialog buttons with custom ones
#
#  \param dialog
#  Dialog instance containing the buttons
def ReplaceStandardButtons(dialog):
  if isinstance(dialog, (wx.FileDialog, wx.MessageDialog)):
    logger.warn("FIXME: Cannot replace buttons on object type: {}".format(type(dialog)))

    return

  lyt_buttons = GetButtonSizer(dialog.GetSizer())

  removed_button_ids = []

  if lyt_buttons:
    for FIELD in lyt_buttons.GetChildren():
      FIELD = FIELD.GetWindow()

      if isinstance(FIELD, wx.Button):
        lyt_buttons.Detach(FIELD)
        removed_button_ids.append(FIELD.GetId())
        FIELD.Destroy()

  # Replace sizer with ButtonSizer
  if not isinstance(lyt_buttons, ButtonSizer):
    container_sizer = _get_containing_sizer(dialog, lyt_buttons)

    index = 0
    for S in container_sizer.GetChildren():
      S = S.GetSizer()

      if S and S == lyt_buttons:
        break

      index += 1

    container_sizer.Remove(lyt_buttons)
    lyt_buttons = ButtonSizer(wx.HORIZONTAL)
    container_sizer.Insert(index, lyt_buttons, 0, wx.ALIGN_RIGHT)

  # Don't add padding to first item
  FLAGS = 0

  for ID in removed_button_ids:
    lyt_buttons.Add(CreateButton(dialog, ID), 0, FLAGS, 5)

    if not FLAGS:
      FLAGS = wx.LEFT

  dialog.Fit()
  dialog.Layout()


## Creates a new custom button
#
#  \param parent
#  \b \e wx.Window parent instance
#  \param label
#  Text to be shown on button or tooltip
#  \param btnId
#  <b><i>Integer identifier
#  \param image
#  Base name of image file to use for custom buttons (uses standard image if set to 'None')
#  \param size
#  Image size to use for button
#  \param tooltip
#  Text to display when cursor hovers over button
#  \param name
#  Name attribute
#  \return
#  ui.button.CustomButton instance or wx.Button instance if image file not found
def CreateButton(parent, btnId=wx.ID_ANY, label=wx.EmptyString, image=None, size=32, tooltip=None, name=None,
      commands=None, requireAll=False):
  if not image:
    image = btnid.GetImage(btnId)

  # Use titleized version of the image name for the label
  if not label and image:
    label = image.title()

  if not name:
    name = label

  button = None

  if image:
    image = os.path.join(getBitmapsDir(), "button", GS(size), "{}.png".format(image))

    if not os.path.isfile(image):
      logger.warn(
          "CreateButton: Attempted to set not-existent image for button (ID {}):".format(btnId),
          details=image)

    else:
      button = CustomButton(parent, image, btnId, name=name, commands=commands,
          requireAll=requireAll)

      if not tooltip:
        tooltip = label

      button.SetToolTip(tooltip)

  # Use a standard button
  if not button:
    button = Button(parent, btnId, label, name=name, commands=commands,
        requireAll=requireAll)

  return button
