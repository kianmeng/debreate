## \package globals.changes

# MIT licensing
# See: docs/LICENSE.txt


from globals.application import APP_name
from globals.application import AUTHOR_email
from globals.application import AUTHOR_name
from globals.application import VERSION_string
from globals.dateinfo    import GetDate
from globals.dateinfo    import GetTime
from globals.dateinfo    import GetTimeZone
from globals.dateinfo    import dtfmt
from globals.strings     import RemoveEmptyLines
from globals.strings     import TextIsEmpty
from globals.system      import OS_codename


section_delims = "*-+#"

def _strip_line(line, preserve_indent=False):
  chars = " \t"

  if preserve_indent:
    return line.rstrip(chars)

  return line.strip(chars)


def _format_section(line, preserve_indent=False):
  global section_delims

  return "  * {}".format(_strip_line(line, preserve_indent).lstrip(" \t{}".format(section_delims)))


## Formats lines for changelog output
def _format_lines(lines, preserve_indent=False):
  if isinstance(lines, tuple):
    lines = list(lines)

  if lines:
    global section_delims

    for INDEX in range(len(lines)):
      if INDEX == 0:
        # First line will always start with an asterix
        lines[INDEX] = _format_section(lines[INDEX], preserve_indent)
        continue

      # Make sure line is not empty before setting section
      if lines[INDEX] and lines[INDEX].lstrip(" \t")[0] in section_delims:
        lines[INDEX] = _format_section(lines[INDEX], preserve_indent)

      else:
        lines[INDEX] = "	{}".format(_strip_line(lines[INDEX], preserve_indent))

  return tuple(lines)


## Formats date & time for changelog
def _get_cl_timestamp():
  fmt = dtfmt.CL
  return "{} {} {}".format(GetDate(fmt), GetTime(fmt), GetTimeZone(fmt))


## Function to format text Debian changelog standards
#
#  \param text
#  \b \e String to be formatted
#  \return
#  Debian changelog format
def FormatChangelog(text, name=APP_name, version=VERSION_string, dist=OS_codename,
      urgency="low", packager=AUTHOR_name, email=AUTHOR_email, preserve_indent=False):
  if TextIsEmpty(text):
    return None

  # Remove leading & trailing whitespace & empty lines & split into
  # list of lines.
  lines = text.strip(" \t\n\r").split("\n")

  if not lines:
    return None

  lines = RemoveEmptyLines(lines)
  lines = _format_lines(lines, preserve_indent)

  text = "\n".join(lines)
  header = "{} ({}) {}; urgency={}\n".format(name, version, dist, urgency)
  footer = "\n -- {} <{}>  {}".format(packager, email, _get_cl_timestamp())

  return "\n".join((header, text, footer))
