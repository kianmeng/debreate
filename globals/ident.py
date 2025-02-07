## \package globals.ident
#
#  Miscellaneous IDs

# MIT licensing
# See: docs/LICENSE.txt


import wx

import util

from dbr.language import GT


logger = util.getLogger()

## Creates a new bitwise compatible ID
#
#  Along with return a new ID, it also updates the id_wrapper reference
#
#  FIXME: Better method than using a list to pass reference?
#  \param id_wrapper
#  \b \e List instance to reference ID number so can be incremented
#  \return
#  New ID number
def AddId(id_wrapper):
  new_id = id_wrapper[0]
  id_wrapper[0] *= 2

  return new_id


## Creates a ID & adds to a member list
#
#  \param member_list
#  \b \e List instance to add ID to
def NewId(member_list=None):
  new_id = wx.NewId()

  if isinstance(member_list, list):
    member_list.append(new_id)

  return new_id


# Page IDs
next_page_id = 1000
page_ids = {}

## Creates a new page ID & adds to a member list instance for iteration
def NewPageId(page_name=None, member_list=None):
  global next_page_id

  this_page_id = next_page_id
  next_page_id += 1

  page_ids[this_page_id] = page_name

  if isinstance(member_list, list):
    # Add to member list for iterating
    member_list.append(this_page_id)

  return this_page_id


## Abstract ID class
class FieldId:
  def __init__(self):
    self.IdList = []


  ## Adds a predetermined ID to ID list
  #
  #  \param staticId
  #  <b><i>integer</i></b>:
  #    Predefined ID to set
  def AddStaticId(self, staticId):
    self.IdList.append(staticId)

    return staticId


  ## Add a new ID
  def NewId(self):
    return NewId(self.IdList)


## Page IDs
class PageId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.Labels = {}

    self.GREETING = self.NewId(GT("Information"))
    self.CONTROL = self.NewId(GT("Control"))
    self.DEPENDS = self.NewId(GT("Depends"))
    self.FILES = self.NewId(GT("Files"))
    self.MAN = self.NewId(GT("Man"))
    self.SCRIPTS = self.NewId(GT("Scripts"))
    self.CHANGELOG = self.NewId(GT("Changelog"))
    self.COPYRIGHT = self.NewId(GT("Copyright"))
    self.MENU = self.NewId(GT("Menu"))
    self.BUILD = self.NewId(GT("Build"))


  ## Adds a predetermined ID to ID list & text label to label list
  #
  #  \param staticId
  #  <b><i>integer</i></b>:
  #    Predefined ID to set
  #  \param label
  #  <b><i>string</i></b>
  #    Page label/title
  def AddStaticId(self, staticId, label):
    new_id = FieldId.AddStaticId(self, staticId)

    self.Labels[new_id] = label

    return new_id


  ## Add a new ID & text label to label list
  #
  #  param label
  #  <b><i>string</i></b>:
  #    Page label/title
  def NewId(self, label):
    #new_id = FieldId.NewId(self)
    new_id = NewPageId(label, self.IdList)

    self.Labels[new_id] = label

    return new_id

pgid = PageId()


## IDs for text input fields
class InputId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.ARCH = self.NewId()
    self.CAT = self.NewId()
    self.CAT2 = self.NewId()
    self.CHANGES = self.NewId()
    self.CHECK = self.NewId()
    self.CUSTOM = self.NewId()
    self.DESCR = self.NewId()
    self.DIST = self.NewId()
    self.EMAIL = self.NewId()
    self.ENC = self.NewId()
    self.EXEC = self.NewId()
    self.FNAME = self.NewId()
    self.ICON = self.NewId()
    self.KEY = self.NewId()
    self.LIST = self.NewId()
    self.MAINTAINER = self.NewId()
    self.MIME = self.NewId()
    self.NAME = self.NewId()
    self.NOTIFY = self.NewId()
    self.OTHER = self.NewId()
    self.PACKAGE = self.NewId()
    self.TARGET = self.NewId()
    self.TERM = self.NewId()
    self.TYPE = self.NewId()
    self.VALUE = self.NewId()
    self.VERSION = self.NewId()

inputid = InputId()


## IDs for button fields
class ButtonId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    ## Image labels associated with button IDs
    self.Images = {}

    self.ADD = self.AddStaticId(wx.ID_ADD, "add")
    self.APPEND = self.NewId("append")
    self.BIN = self.NewId()
    self.BROWSE = self.NewId("browse")
    self.BUILD = self.NewId("build")
    self.CANCEL = self.AddStaticId(wx.ID_CANCEL, "cancel")
    self.CLEAR = self.AddStaticId(wx.ID_CLEAR, "clear")
    self.CLOSE = self.AddStaticId(wx.ID_CLOSE)
    self.CONFIRM = self.AddStaticId(wx.ID_OK, "confirm")
    self.EXIT = self.AddStaticId(wx.ID_EXIT, "exit")
    self.FULL = self.NewId("full")
    self.HELP = self.AddStaticId(wx.ID_HELP, "help")
    self.HIDE = self.NewId("hide")
    self.IMPORT = self.NewId("import")
    self.MODE = self.NewId("mode")
    self.NEXT = self.NewId("next")
    self.PREV = self.NewId("prev")
    self.PREVIEW = self.AddStaticId(wx.ID_PREVIEW, "preview")
    self.REFRESH = self.AddStaticId(wx.ID_REFRESH, "refresh")
    self.REMOVE = self.AddStaticId(wx.ID_REMOVE, "remove")
    self.RENAME = self.NewId("rename")
    self.SAVE = self.AddStaticId(wx.ID_SAVE, "save")
    self.SHORT = self.NewId("short")
    self.SRC = self.NewId()
    self.STAGE = self.NewId()
    self.TARGET = self.NewId()
    self.ZOOM = self.AddStaticId(wx.ID_PREVIEW_ZOOM, "zoom")


  ## Adds a predetermined ID to ID list & optional bitmap image reference
  #
  #  \param staticId
  #  <b><i>integer</i></b>:
  #    Predefined ID to set
  #  \param imageName
  #  <b><i>string</i></b>:
  #    Image file basename
  def AddStaticId(self, staticId, imageName=None):
    self.Images[staticId] = imageName

    return FieldId.AddStaticId(self, staticId)


  ## Retrieves the image linked to the ID
  #
  #  \param btnId
  #  Requested button ID
  #  \return
  #  <b><i>string</i></b>:
  #    Image label associated with button ID (<b><i>None</i></b> if ID has no image)
  def GetImage(self, btnId):
    if btnId in self.Images:
      return self.Images[btnId]

    logger.warn("ButtonId.GetImage: Requested button ID {} with no associated image".format(btnId))


  ## Adds a new ID & optional bitmap image reference
  #
  #  \param imageName
  #  <b><i>string</i></b>:
  #    Image file basename
  def NewId(self, imageName=None):
    new_id = FieldId.NewId(self)

    self.Images[new_id] = imageName

    return new_id

btnid = ButtonId()


## IDs for check box fields
class ChkId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.CAT = self.NewId()
    self.DELETE = self.AddStaticId(wx.ID_DELETE)
    self.EDIT = self.AddStaticId(wx.ID_EDIT)
    self.ENABLE = self.NewId()
    self.FNAME = self.NewId()
    self.INSTALL = self.NewId()
    self.LINT = self.NewId()
    self.MD5 = self.NewId()
    self.NOTIFY = self.NewId()
    self.REMOVE = self.NewId()
    self.STRIP = self.NewId()
    self.SYMLINK = self.NewId()
    self.TARGET = self.NewId()
    self.TERM = self.NewId()
    self.TOPLEVEL = self.NewId()

chkid = ChkId()


## IDs for list fields
class ListId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.CAT = self.NewId()

listid = ListId()


## IDs for menus
class MenuId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.ABOUT = self.AddStaticId(wx.ID_ABOUT)
    self.ACTION = self.NewId()
    self.ALIEN = self.NewId()
    self.BUILD = self.NewId()
    self.CCACHE = self.NewId()
    self.COMPRESS = self.NewId()
    self.DEBUG = self.NewId()
    self.DIST = self.NewId()
    self.EXIT = btnid.EXIT
    self.EXPAND = self.NewId()
    self.FILE = self.AddStaticId(wx.ID_FILE)
    self.HELP = btnid.HELP
    self.LOG = self.NewId()
    self.NEW = self.AddStaticId(wx.ID_NEW)
    self.OPEN = self.AddStaticId(wx.ID_OPEN)
    self.OPENLOGS = self.NewId()
    self.OPTIONS = self.NewId()
    self.PAGE = self.NewId()
    self.QBUILD = self.NewId()
    self.RENAME = btnid.RENAME
    self.SAVE = btnid.SAVE
    self.SAVEAS = self.AddStaticId(wx.ID_SAVEAS)
    self.THEME = self.NewId()
    self.TOGGLEHIDDEN = self.NewId()
    self.TOOLTIPS = self.NewId()
    self.UPDATE = self.NewId()

menuid = MenuId()


## IDs for panels
class PanelId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.BACKGROUND = self.NewId()

pnlid = PanelId()


## IDs for choice/selection fields
class SelId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.LICENSE = self.NewId()
    self.URGENCY = self.NewId()

selid = SelId()


## IDs for static text fields
class TxtId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.FNAME = self.NewId()

txtid = TxtId()


## IDs for reference manual menu item links
class RefId(FieldId):
  def __init__(self):
    FieldId.__init__(self)

    self.DEBSRC = self.NewId()
    self.DPM = self.NewId()
    self.DPMCtrl = self.NewId()
    self.DPMLog = self.NewId()
    self.LAUNCHERS = self.NewId()
    self.LINT_TAGS = self.NewId()
    self.LINT_OVERRIDE = self.NewId()
    self.MAN = self.NewId()
    self.UPM = self.NewId()

refid = RefId()
