from odoo import fields, models, api


class AuditCycle(models.Model):
    _name = "assetflow.audit.cycle"
    _description = "Asset Audit Cycle"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("progress", "In Progress"),
            ("done", "Completed"),
        ],
        default="draft",
        string="Status",
    )
    line_ids = fields.One2many(
        "assetflow.audit.line",
        "cycle_id",
        string="Audit Lines",
    )
