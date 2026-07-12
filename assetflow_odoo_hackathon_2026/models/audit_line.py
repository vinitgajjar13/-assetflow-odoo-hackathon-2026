from odoo import fields, models, api


class AuditLine(models.Model):
    _name = "assetflow.audit.line"
    _description = "Asset Audit Line"
    _order = "id desc"

    cycle_id = fields.Many2one(
        "assetflow.audit.cycle",
        string="Audit Cycle",
        required=True,
        ondelete="cascade",
    )
    asset_id = fields.Many2one(
        "assetflow.asset",
        string="Asset",
        required=True,
    )
    status = fields.Selection(
        [
            ("verified", "Verified"),
            ("missing", "Missing"),
            ("damaged", "Damaged"),
        ],
        string="Status",
    )
    remarks = fields.Text(string="Remarks")
