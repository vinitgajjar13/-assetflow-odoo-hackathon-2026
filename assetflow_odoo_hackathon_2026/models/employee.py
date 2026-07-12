from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    asset_role = fields.Selection(
        [
            ("employee", "Employee"),
            ("department_head", "Department Head"),
            ("asset_manager", "Asset Manager"),
            ("admin", "Administrator"),
        ],
        default="employee",
        string="AssetFlow Role",
    )

    status = fields.Selection(
        [
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        default="active",
    )

    allocated_asset_ids = fields.One2many(
        "assetflow.asset.allocation",
        "employee_id",
        string="Allocated Assets",
    )

    allocated_asset_count = fields.Integer(
        compute="_compute_asset_count"
    )

    @api.depends("allocated_asset_ids")
    def _compute_asset_count(self):
        for rec in self:
            rec.allocated_asset_count = len(
                rec.allocated_asset_ids.filtered(
                    lambda x: x.state == "allocated"
                )
            )

    @api.constrains("work_email")
    def _check_email(self):
        for rec in self:
            if rec.work_email:
                duplicate = self.search([
                    ("work_email", "=", rec.work_email),
                    ("id", "!=", rec.id),
                ], limit=1)

                if duplicate:
                    raise ValidationError(
                        "Employee email already exists."
                    )

    def action_view_allocated_assets(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Allocated Assets",
            "res_model": "assetflow.asset.allocation",
            "view_mode": "list,form",
            "domain": [("employee_id", "=", self.id)],
        }