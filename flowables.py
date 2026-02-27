from copy import deepcopy

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import Flowable, Paragraph, Table, TableStyle

from reportlab.platypus import Flowable
from reportlab.lib import colors

class SolidHR(Flowable):
    def __init__(self, thickness=1, color=colors.black, spaceBefore=0, spaceAfter=0):
        super().__init__()
        self.thickness = thickness
        self.color = color
        self.spaceBefore = spaceBefore
        self.spaceAfter = spaceAfter

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        self.height = self.thickness + self.spaceBefore + self.spaceAfter
        return (availWidth, self.height)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setLineWidth(self.thickness)
        c.setStrokeColor(self.color)
        c.setLineCap(2)  # 2 = square cap (crisper for rules)
        # draw centered in our own height
        y = self.spaceAfter + (self.thickness / 2.0)
        c.line(0, y, self.width, y)
        c.restoreState()

class LRBlock(Flowable):
    def __init__(self, company, title, location, date,
                 company_style, title_style, location_style, date_style,
                 left_ratio=0.75):
        super().__init__()
        self.company = company
        self.title = title
        self.location = location
        self.date = date
        self.company_style = company_style
        self.title_style = title_style
        self.location_style = location_style
        self.date_style = date_style
        self.left_ratio = left_ratio
        self._table = None

    def wrap(self, availWidth, availHeight):
        left = [
            Paragraph(self.company, self.company_style),
            Paragraph(self.title, self.title_style),
        ]

        loc_style = deepcopy(self.location_style); loc_style.alignment = TA_RIGHT
        dt_style  = deepcopy(self.date_style);     dt_style.alignment  = TA_RIGHT
        right = [
            Paragraph(self.location, loc_style),
            Paragraph(self.date, dt_style),
        ]

        w_left = availWidth * self.left_ratio
        w_right = availWidth - w_left  # guarantees exact total width

        self._table = Table([[left, right]], colWidths=[w_left, w_right], hAlign="LEFT")
        self._table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN",  (1, 0), (1, 0), "RIGHT"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING",   (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ]))

        return self._table.wrap(availWidth, availHeight)

    def draw(self):
        # draw at the left edge of the frame (same as HRFlowable)
        self._table.drawOn(self.canv, 0, 0)