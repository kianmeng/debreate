## \package ui.about

# MIT licensing
# See: docs/LICENSE.txt


import os, wx

import util

from dbr.font            import MONOSPACED_MD
from dbr.functions       import GetContainerItemCount
from dbr.language        import GT
from globals             import paths
from globals.application import APP_name
from globals.application import AUTHOR_email
from globals.application import AUTHOR_name
from globals.constants   import INSTALLED
from globals.constants   import PREFIX
from globals.dateinfo    import GetYear
from globals.ident       import btnid
from globals.mime        import GetFileMimeType
from globals.system      import PY_VER_STRING
from globals.system      import WX_VER_STRING
from input.list          import ListCtrl
from input.text          import TextAreaPanel
from libdbr.fileio       import readFile
from ui.button           import CreateButton
from ui.dialog           import ShowErrorDialog
from ui.hyperlink        import Hyperlink
from ui.layout           import BoxSizer
from ui.style            import layout as lyt


logger = util.getLogger()

# Font for the name
bigfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
sys_info_font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)


## Dialog that shows information about the application
class AboutDialog(wx.Dialog):
  ## Constructor
  #
  #  \param parent
  #  	The parent window
  #  \param id
  #  	Window id (FIXME: Not necessary)
  #  \param title
  #  	Text to be shown in the title bar
  def __init__(self, parent, size=(600,558)):
    wx.Dialog.__init__(self, parent, wx.ID_ABOUT, GT("About"), size=size,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

    self.SetMinSize(wx.Size(400, 375))
    self.CenterOnParent()

    # Create a tabbed interface
    tabs = wx.Notebook(self, -1)

    # Pages
    self.t_about = wx.Panel(tabs, -1)
    t_credits = wx.Panel(tabs, -1)
    t_changelog = wx.Panel(tabs, -1)
    t_license = wx.Panel(tabs, -1)

    # Add pages to tabbed interface
    tabs.AddPage(self.t_about, GT("About"))
    tabs.AddPage(t_credits, GT("Credits"))
    tabs.AddPage(t_changelog, GT("Changelog"))
    tabs.AddPage(t_license, GT("License"))

    # FIXME: Center verticall on about tab
    self.about_layout_V1 = BoxSizer(wx.VERTICAL)
    self.about_layout_V1.AddStretchSpacer()
    self.about_layout_V1.AddStretchSpacer()

    self.t_about.SetAutoLayout(True)
    self.t_about.SetSizer(self.about_layout_V1)
    self.t_about.Layout()

    ## List of credits
    self.credits = ListCtrl(t_credits)
    self.credits.SetSingleStyle(wx.LC_REPORT)
    self.credits.InsertColumn(0, GT("Name"), width=150)
    self.credits.InsertColumn(1, GT("Job"), width=200)
    self.credits.InsertColumn(2, GT("Email"), width=240)

    credits_sizer = BoxSizer(wx.VERTICAL)
    credits_sizer.Add(self.credits, 1, wx.EXPAND)

    t_credits.SetAutoLayout(True)
    t_credits.SetSizer(credits_sizer)
    t_credits.Layout()

    ## Changelog text area
    self.changelog = TextAreaPanel(t_changelog, style=wx.TE_READONLY)
    self.changelog.SetFont(MONOSPACED_MD)

    log_sizer = BoxSizer(wx.VERTICAL)
    log_sizer.Add(self.changelog, 1, wx.EXPAND)

    t_changelog.SetSizer(log_sizer)
    t_changelog.Layout()


    ## Licensing information text area
    self.license = TextAreaPanel(t_license, style=wx.TE_READONLY)
    self.license.SetFont(MONOSPACED_MD)

    license_sizer = BoxSizer(wx.VERTICAL)
    license_sizer.Add(self.license, 1, wx.EXPAND)

    t_license.SetSizer(license_sizer)
    t_license.Layout()


    # System info
    sys_info = wx.Panel(tabs, -1)
    tabs.AddPage(sys_info, GT("System Information"))

    ## System's <a href="https://www.python.org/">Python</a> version
    self.py_info = wx.StaticText(sys_info, -1,
        GT("Python version: {}").format(PY_VER_STRING))

    ## System's <a href="https://wxpython.org/">wxPython</a> version
    self.wx_info = wx.StaticText(sys_info, -1,
        GT("wxPython version: {}").format(WX_VER_STRING))

    ## Debreate's installation prefix
    install_prefix = wx.StaticText(sys_info,
        label=GT("App location: {}").format(paths.getAppDir()))

    if INSTALLED:
      install_prefix.SetLabel(GT("Installation prefix: {}").format(PREFIX))

    self.py_info.SetFont(sys_info_font)
    self.wx_info.SetFont(sys_info_font)


    sysinfo_layout_V1 = BoxSizer(wx.VERTICAL)
    sysinfo_layout_V1.AddStretchSpacer()
    sysinfo_layout_V1.Add(self.py_info, 0, wx.ALIGN_CENTER|wx.BOTTOM, 5)
    sysinfo_layout_V1.Add(self.wx_info, 0, wx.ALIGN_CENTER|wx.TOP, 5)
    sysinfo_layout_V1.AddSpacer(20)
    sysinfo_layout_V1.Add(install_prefix, 0, wx.ALIGN_CENTER|wx.TOP, 5)
    sysinfo_layout_V1.AddStretchSpacer()

    sys_info.SetSizer(sysinfo_layout_V1)
    sys_info.Layout()

    # Button to close the dialog
    btn_confirm = CreateButton(self, btnid.CONFIRM)

    sizer = BoxSizer(wx.VERTICAL)
    sizer.Add(tabs, 1, wx.EXPAND)
    sizer.Add(btn_confirm, 0, wx.ALIGN_RIGHT|lyt.PAD_RTB, 5)

    self.SetSizer(sizer)
    self.Layout()


  ## Displays logo in 'about' tab
  #
  #  \param graphic
  #  	Path to image file
  def SetGraphic(self, graphic):
    insertion_point = GetContainerItemCount(self.about_layout_V1) - 1

    if not isinstance(graphic, wx.Bitmap):
      graphic = wx.Image(graphic)
      graphic.Rescale(64, 64, wx.IMAGE_QUALITY_HIGH)
      graphic = graphic.ConvertToBitmap()

    self.about_layout_V1.Insert(
      insertion_point,
      wx.StaticBitmap(self.t_about, wx.ID_ANY, graphic),
      0,
      wx.ALL|wx.ALIGN_CENTER,
      10
    )

    self.t_about.Layout()


  ## Displays version in 'about' tab
  #
  #  \param version
  #  	String to display
  def SetVersion(self, version):
    insertion_point = GetContainerItemCount(self.about_layout_V1) - 1

    app_label = wx.StaticText(
      self.t_about,
      label="{} {}".format(APP_name, version)
    )
    app_label.SetFont(bigfont)

    self.about_layout_V1.Insert(
      insertion_point,
      app_label,
      0,
      wx.ALL|wx.ALIGN_CENTER,
      10
    )

    self.t_about.Layout()


  ## Display author's name
  #
  #  \param author
  #  	String to display
  def SetAuthor(self, author):
    insertion_point = GetContainerItemCount(self.about_layout_V1) - 1

    self.about_layout_V1.Insert(
      insertion_point,
      wx.StaticText(self.t_about, label=author),
      0,
      wx.ALL|wx.ALIGN_CENTER,
      10
    )

    self.t_about.Layout()


  ## Sets a hotlink to the app's homepage
  #
  #  TODO: Remove: Deprecated, unused
  #  \param URL
  #  	URL to open when link is clicked
  def SetWebsite(self, URL):
    self.website.SetLabel(URL)
    self.website.SetURL(URL)


  ## Adds URL hotlinks to about dialog
  #
  #  \param url_list
  #  	\b \e tuple : Website labels & URL definitions
  def SetWebsites(self, url_list):
    insertion_point = GetContainerItemCount(self.about_layout_V1) - 1

    link_layout = BoxSizer(wx.VERTICAL)
    for label, link in url_list:
      link_layout.Add(
        Hyperlink(self.t_about, wx.ID_ANY, label=label, url=link),
        0,
        wx.ALIGN_CENTER,
        10
      )

    self.about_layout_V1.Insert(
      insertion_point,
      link_layout,
      0,
      wx.ALL|wx.ALIGN_CENTER,
      10
    )
    self.t_about.Layout()


  ## Displays a description about the app on the 'about' tab
  def SetDescription(self, desc):
    # Place between spacers
    insertion_point = GetContainerItemCount(self.about_layout_V1) - 1

    self.about_layout_V1.Insert(
      insertion_point,
      wx.StaticText(self.t_about, label=desc),
      0,
      wx.ALL|wx.ALIGN_CENTER,
      10
    )

    self.t_about.Layout()


  ## Adds a developer to the list of credits
  #
  #  \param name
  #  	str: Developer's name
  #  \param email
  #  	str: Developer's email address
  def AddDeveloper(self, name, email):
    next_item = self.credits.GetItemCount()
    self.credits.InsertStringItem(next_item, name)
    self.credits.SetStringItem(next_item, 2, email)
    self.credits.SetStringItem(next_item, 1, GT("Developer"))


  ## Adds a packager to the list of credits
  #
  #  \param name
  #  	\b \e str : Packager's name
  #  \param email
  #  	\b \e str : Packager's email address
  def AddPackager(self, name, email):
    next_item = self.credits.GetItemCount()
    self.credits.InsertStringItem(next_item, name)
    self.credits.SetStringItem(next_item, 2, email)
    self.credits.SetStringItem(next_item, 1, GT("Packager"))


  ## Adds a translator to the list of credits
  #
  #  \param name
  #  	\b \e str : Translator's name
  #  \param email
  #  	\b \e str : Translator's email address
  #  \param lang
  #  	\b \e str : Locale code for the translation
  def AddTranslator(self, name, email, lang):
    job = GT("Translation")
    job = "{} ({})".format(job, lang)
    next_item = self.credits.GetItemCount()
    self.credits.InsertStringItem(next_item, name)
    self.credits.SetStringItem(next_item, 2, email)
    self.credits.SetStringItem(next_item, 1, job)


  ## Adds a general job to the credits list
  #
  #  \param name
  #  	\b \e str : Contributer's name
  #  \param job
  #  	\b \e str : Job description
  #  \param email
  #  	\b \e str : Job holder's email address
  def AddJob(self, name, job, email=wx.EmptyString):
    next_item = self.credits.GetItemCount()
    self.credits.InsertStringItem(next_item, name)
    self.credits.SetStringItem(next_item, 1, job)

    if email != wx.EmptyString:
      self.credits.SetStringItem(next_item, 2, email)


  ## Adds list of jobs for single contributer
  #
  #  \param name
  #  	\b \e str : Contributer's name
  #  \param jobs
  #  	\b \e string \b \e list|tuple : Contributer's jobs
  #  \param email
  #  	\b \e str : Optional contributer's email address
  def AddJobs(self, name, jobs, email=wx.EmptyString):
    if isinstance(jobs, str):
      logger.debug(GT("Converting string argument \"jobs\" to tuple"))
      jobs = (jobs,)

    for x, value in enumerate(jobs):
      next_item = self.credits.GetItemCount()
      if x == 0:
        self.credits.InsertStringItem(next_item, name)
        if email != wx.EmptyString:
          self.credits.SetStringItem(next_item, 2, email)
      else:
        self.credits.InsertStringItem(next_item, wx.EmptyString)

      self.credits.SetStringItem(next_item, 1, value)

  # FIXME: Unused?
  def NoResizeCol(self, event=None):
    if event:
      event.Veto()


  ## Sets text to be shown on the 'Changelog' tab
  #
  #  FIXME: Change to create in class constructor
  #  \param log_file
  #  	\b \e str : Path to changelog file on filesystem
  def SetChangelog(self):
    ## Defines where the changelog is located
    #
    #  By default it is located in the folder 'doc'
    #   under the applications root directory. The
    #   install script or Makefile should change this
    #   to reflect installed path.
    if INSTALLED:
      CHANGELOG = os.path.normpath(os.path.join(PREFIX, "share/doc/debreate/changelog"))
    else:
      CHANGELOG = os.path.normpath(os.path.join(paths.getAppDir(), "docs/changelog"))

    if os.path.isfile(CHANGELOG):
      changelog_mimetype = GetFileMimeType(CHANGELOG)

      logger.debug(GT("Changelog mimetype: {}").format(changelog_mimetype))

      # Set log text in case of read error
      log_text = GT("Error reading changelog: {}\n\t").format(CHANGELOG)
      log_text = "{}{}".format(log_text,
                  GT("Cannot decode, unrecognized mimetype: {}").format(changelog_mimetype))

      if changelog_mimetype == "text/plain":
        log_text = readFile(CHANGELOG)

      else:
        ShowErrorDialog(log_text, parent=self)

    else:
      log_text = GT("ERROR: Could not locate changelog file:\n\t'{}' not found".format(CHANGELOG))

    self.changelog.SetValue(log_text)
    self.changelog.SetInsertionPoint(0)


  ## Sets text to be shown on the 'License' tab
  #
  #  \param lic_file
  #  	\b \e : Path to license file on the filesystem
  def SetLicense(self):
    ## Defines where the LICENSE.txt is located
    #
    #  By default it is located in the folder 'doc'
    #   under the applications root directory. The
    #   install script or Makefile should change this
    #   to reflect installed path.
    if INSTALLED:
      license_path = os.path.normpath(os.path.join(PREFIX, "share/doc/debreate/LICENSE.txt"))
    else:
      license_path = os.path.normpath(os.path.join(paths.getAppDir(), "docs/LICENSE.txt"))

    if os.path.isfile(license_path):
      lic_text = readFile(license_path)

    else:
      lic_text = GT("ERROR: Could not locate license file:\n\t'{}' not found".format(license_path))
      lic_text += "\n\nCopyright © {} {} <{}>".format(GetYear(), AUTHOR_name, AUTHOR_email)
      lic_text += "\n\nhttps://opensource.org/licenses/MIT"

    self.license.SetValue(lic_text)
    self.license.SetInsertionPoint(0)


  ## Defines action to take when 'Ok' button is press
  #
  #  Closes the dialog.
  #  \param event
  #  	<b><em>(wx.EVT_BUTTON)</em></b>
  def OnOk(self, event=None):
    self.Close()
