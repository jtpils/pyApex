# -*- coding: utf-8 -*-
__title__ = 'Zoom Base Point'
__doc__ = """Zoom in active view to Project base point. If it's hidden - enables "Reveal Hidden" mode.
Shift+Click - to Site point

Находит базовую точку проекта на текущем виде. Если точка скрыта - включает режим показа скрытых объектов.
Shift+Click - Точку съемки"""

__helpurl__ = "https://apex-project.github.io/pyApex/help#zoom-base-point"

from pyrevit.versionmgr import PYREVIT_VERSION
pyRevitNewer44 = PYREVIT_VERSION.major >=4 and PYREVIT_VERSION.minor >=5

if pyRevitNewer44:
    from pyrevit import script, revit
    output = script.get_output()
    logger = script.get_logger()
    linkify = output.linkify
    doc = revit.doc
    uidoc = revit.uidoc
    selection = revit.get_selection()
else:
    from scriptutils import logger, this_script

    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    output = this_script.output

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementId, Transaction

cl = FilteredElementCollector(doc, uidoc.ActiveView.Id).WhereElementIsNotElementType()

if __shiftclick__:
    category = BuiltInCategory.OST_SharedBasePoint
else:
    category = BuiltInCategory.OST_ProjectBasePoint

elements = cl.OfCategory(category).ToElementIds()

if len(elements)==0:
    t = Transaction(doc, "[%s] Reveal hidden" % __title__)
    t.Start()

    uidoc.ActiveView.EnableRevealHiddenMode()
    cl = FilteredElementCollector(doc, uidoc.ActiveView.Id).WhereElementIsNotElementType()
    elements = cl.OfCategory(category).ToElementIds()
    if len(elements) == 0:
        t.RollBack()
        cl = FilteredElementCollector(doc).WhereElementIsNotElementType()
        elements = cl.OfCategory(category).ToElementIds()
    else:
        t.Commit()

uidoc.ShowElements(elements[0])