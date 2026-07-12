from odoo import fields, api, models


class AssetHistory(models.Model):
    _name = "assetflow.asset.history"
    _description = "Asset History"
    _order = "date desc"

    asset_id = fields.Many2one(
        "assetflow.asset",
        string="Asset",
        required=True,
        ondelete="cascade",
    )

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
    )

    department_id = fields.Many2one(
        "hr.department",
        string="Department",
    )

    action = fields.Selection(
        [
            ("registered", "Registered"),
            ("allocated", "Allocated"),
            ("returned", "Returned"),
            ("transfer", "Transferred"),
            ("maintenance", "Maintenance"),
            ("audit", "Audit"),
            ("retired", "Retired"),
            ("disposed", "Disposed"),
        ],
        string="Action",
        required=True,
    )

    previous_status = fields.Selection(
        [
            ("available", "Available"),
            ("allocated", "Allocated"),
            ("maintenance", "Under Maintenance"),
            ("lost", "Lost"),
            ("retired", "Retired"),
            ("disposed", "Disposed"),
        ],
        string="Previous Status",
    )

    current_status = fields.Selection(
        [
            ("available", "Available"),
            ("allocated", "Allocated"),
            ("maintenance", "Under Maintenance"),
            ("lost", "Lost"),
            ("retired", "Retired"),
            ("disposed", "Disposed"),
        ],
        string="Current Status",
    )

    remarks = fields.Text(string="Remarks")

    user_id = fields.Many2one(
        "res.users",
        string="Performed By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now,
        readonly=True,
    )

    @api.depends("asset_id.name", "action")
    def _compute_display_name(self):
        for rec in self:
            action_desc = dict(self._fields["action"].selection).get(rec.action, "")
            rec.display_name = f"{rec.asset_id.name or ''} - {action_desc}"