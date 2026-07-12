from odoo import models, fields, api


class Department(models.Model):
    _name = "assetflow.department"
    _description = "AssetFlow Department"
    _order = "name"

    name = fields.Char(string="Department Name", required=True)
    code = fields.Char(
        string="Department Code",
        copy=False,
        readonly=True,
        default="New",
    )
    manager_id = fields.Many2one(
        "hr.employee",
        string="Department Manager",
    )
    employee_ids = fields.One2many(
        "hr.employee",
        "department_id",
        string="Employees",
    )
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = self.env["ir.sequence"].next_by_code(
                "assetflow.department"
            ) or "New"
        return super().create(vals)