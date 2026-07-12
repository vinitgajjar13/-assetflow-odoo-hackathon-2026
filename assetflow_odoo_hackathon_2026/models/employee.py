from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_code = fields.Char(
        string="Employee Code",
        copy=False,
        readonly=True,
        default="New",
    )

    asset_role = fields.Selection(
        [
            ("employee", "Employee"),
            ("department_head", "Department Head"),
            ("asset_manager", "Asset Manager"),
            ("admin", "Administrator"),
        ],
        string="AssetFlow Role",
        default="employee",
        tracking=True,
    )

    status = fields.Selection(
        [
            ("active", "Active"),
            ("inactive", "Inactive"),
        ],
        string="Status",
        default="active",
        tracking=True,
    )

    assetflow_department_id = fields.Many2one(
        "assetflow.department",
        string="AssetFlow Department",
    )

    allocated_asset_ids = fields.One2many(
        "assetflow.asset.allocation",
        "employee_id",
        string="Allocated Assets",
    )

    allocated_asset_count = fields.Integer(
        compute="_compute_asset_count",
        string="Allocated Assets Count",
    )

    @api.depends("allocated_asset_ids.state")
    def _compute_asset_count(self):
        for rec in self:
            rec.allocated_asset_count = len(
                rec.allocated_asset_ids.filtered(
                    lambda a: a.state == "allocated"
                )
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("employee_code", "New") == "New":
                vals["employee_code"] = self.env["ir.sequence"].next_by_code(
                    "assetflow.employee"
                ) or "New"
        return super().create(vals_list)

    def action_view_allocated_assets(self):
        self.ensure_one()
        return {
            "name": "Allocated Assets",
            "type": "ir.actions.act_window",
            "res_model": "assetflow.asset.allocation",
            "view_mode": "list,form",
            "domain": [("employee_id", "=", self.id)],
            "context": {"default_employee_id": self.id},
        }

    @api.constrains("work_email")
    def _check_email(self):
        for rec in self:
            if rec.work_email:
                employee = self.search(
                    [
                        ("work_email", "=", rec.work_email),
                        ("id", "!=", rec.id),
                    ],
                    limit=1,
                )
                if employee:
                    raise ValidationError(
                        "Employee email must be unique."
                    )