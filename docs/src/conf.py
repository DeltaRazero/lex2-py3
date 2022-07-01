# Configuration file for the Sphinx documentation builder.

# -- Imports -----------------------------------------------------------------

import sys
import pathlib

from typing import Any, List, Dict

from sphinx.domains import python
from sphinx.ext     import autodoc


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

DOC_ROOT = pathlib.Path(__file__).parent
PRJ_ROOT = DOC_ROOT / "../../"


# -- Project information -----------------------------------------------------

# Import library module from sourcecode repository
sys.path.insert(0, str(PRJ_ROOT))
import lex2

project   = "lex2-py3"
copyright = "2020-2022, DeltaRazero"
author    = "DeltaRazero"

# The full version, including alpha/beta/rc tags
version = f"v{lex2.__version__}"
release = version


# -- Sphinx glob configuration --------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_includes"]


# -- Extensions configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",     # Core library for html generation from docstrings
    "sphinx.ext.autosummary", # Create neat summary tables
    "sphinx.ext.napoleon",    #
    "sphinx.ext.autosectionlabel",
]

# autosectionlabel_prefix_document = True

autodoc_default_options = {
    "members"          : None,
    "member-order"     : "bysource",
    "undoc-members"    : False,
    "inherited-members": False,
    "show-inheritance" : True,
    "exclude-members"  : "__weakref__",
}
autodoc_inherit_docstrings = True
autodoc_class_signature    = "separated"
autodoc_typehints          = "description"
autodoc_typehints_format   = "short"
autodoc_typehints_description_target = "documented"

autoclass_content = "class"

autosummary_generate           = True # Turn on sphinx.ext.autosummary
autosummary_generate_overwrite = True
autosummary_imported_members   = True

napoleon_use_param       = True
napoleon_numpy_docstring = True
napoleon_custom_sections = [
    # Class attributes
    (  "Public Attributes", "Attributes"),
    ( "Private Attributes", "Attributes"),
    ("Readonly Attributes", "Attributes"),
    # Functions as template pre-processors
    "Template Parameters",
    # Enums
    "Values",
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 3,
    "display_version": True,
}
html_context = {
    "display_github": True,
    "github_user"   : "deltarazero",
    "github_repo"   : "lex2-py",
    "github_version": "master/doc/src/",
}
html_css_files = [
    "css/custom.css",
]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- RST prolog and epilog configuration --------------------------------------

def rst_include(fp: str): return f"    .. include:: /_includes/{fp}.rst"

rst_prolog = '\n'.join([

    # :: INCLUDES :: #
    rst_include("colors"),
    rst_include("text"),

    # :: VARIABLES :: #
f"""
    .. |project| replace:: {project}
""",

])


# -- Sphinx hooks ------------------------------------------------------------

class FunctionDocstringDocumenter(autodoc.FunctionDocumenter):
    """Documenter for extracting only the docstring of a function.
    See also https://stackoverflow.com/questions/7825263/including-docstring-in-sphinx-documentation
    """
    # Name of the directive
    objtype = "function_docstring"
    # Don't indent the content
    content_indent = ""
    # Prevent the documenter getting used in automodule
    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return False
    # Don't add a header to the docstring
    def add_directive_header(self, sig: str):
        return None


def docstring_insert_newline_for_bydefault(app: Any, what: str, name: str, obj: Any, options: Dict[str, Any], lines: List[str]):
    """Inserts a linebreak when the text `By default` is encountered."""
    BY_DEFAULT = "By default"
    it = enumerate(lines)
    for i, line in it:
        if (BY_DEFAULT in line):
            indentation = line.split(BY_DEFAULT)[0] if (line[0]==' ') else ""
            lines.insert(i, indentation)
            next(it, None) # Skip one iteration because an element was inserted in-between just now


def remove_module_docstring(app: Any, what: str, name: str, obj: Any, options: Dict[str, Any], lines: List[str]):
    """Removes the docstring content for automodule."""
    if (what == "module" and ("no-value" in options)):
        del lines[:]


def attribute_modifier(app: Any, what: str, name: str, obj: Any, options: Dict[str, Any], lines: List[str]):
    """aaa."""
    if (what != "attribute"):
        return
    MODIFIERS = [
        "readonly",
        "constant",
        "constant",
    ]
    it = enumerate(lines)
    for i, line in it:
        for modifier in MODIFIERS:
            modifier = f"<{modifier}>"
            if (modifier in line):
                lines[i] = line.replace(modifier, f"``{modifier}``")


def setup(app: Any):
    """Connect hooks into Sphinx instance."""
    app.add_autodocumenter(FunctionDocstringDocumenter)
    app.connect("autodoc-process-docstring", docstring_insert_newline_for_bydefault)
    app.connect("autodoc-process-docstring", remove_module_docstring)
    app.connect("autodoc-process-docstring", attribute_modifier)


# -- Sphinx monkey patches ---------------------------------------------------

def add_line_no_object_base(self: autodoc.Documenter, line: str, source: str, *lineno: int) -> None:
    """Monkey patch to not show `object` base class for :show-inheritance: automodule option."""
    # >> Don't show `Bases: object` when the :show-inheritance: option is used for automodule
    if ":class:`object`" in line:
        return
    if line.strip():  # not a blank line
        self.directive.result.append(self.indent + line, source, *lineno)
    else:
        self.directive.result.append('', source, *lineno)

autodoc.Documenter.add_line = add_line_no_object_base


def note_object_surpressedwarning(self: python.PythonDomain, name: str, objtype: str, node_id: str, aliased: bool = False, location: Any = None) -> None:
    """Monkey patch to surpress the `duplicate object description` warning."""
    if name in self.objects:
        other = self.objects[name]
        # The original definition found. Override it!
        if other.aliased and aliased is False: pass
        # The original definition is already registered.
        elif other.aliased is False and aliased: return
        # Duplicated >> Monkey patch to not log a warning here
        else: pass
    self.objects[name] = python.ObjectEntry(self.env.docname, node_id, objtype, aliased)

python.PythonDomain.note_object = note_object_surpressedwarning
