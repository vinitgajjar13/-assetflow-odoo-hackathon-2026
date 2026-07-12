from odoo import fields, models, api


class Audit(models.Model):
    _name = "assetflow.audit"
    _description = "Asset Audit"
    _order = "id desc"

    name = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )
    asset_id = fields.Many2one(
        "assetflow.asset",
        string="Asset",
        required=True,
    )
    audit_date = fields.Date(
        string="Audit Date",
        default=fields.Date.today,
    )
    auditor_id = fields.Many2one(
        "hr.employee",
        string="Auditor",
    )
    remarks = fields.Text(string="Remarks")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("verified", "Verified"),
        ],
        default="draft",
        string="Status",
    )