from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class AssetAllocation(models.Model):
    _name = "assetflow.asset.allocation"
    _description = "Asset Allocation"
    _order = "allocation_date desc, id desc"

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
        domain="[('status', '=', 'available')]",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        required=True,
    )
    allocation_date = fields.Date(
        string="Allocation Date",
        default=fields.Date.today,
        required=True,
    )
    expected_return_date = fields.Date(string="Expected Return Date")
    actual_return_date = fields.Date(string="Actual Return Date", readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("allocated", "Allocated"),
            ("returned", "Returned"),
        ],
        default="draft",
        string="Status",
    )
    notes = fields.Text(string="Allocation Notes")

    @api.constrains("expected_return_date", "allocation_date")
    def _check_dates(self):
        for rec in self:
            if rec.expected_return_date and rec.expected_return_date < rec.allocation_date:
                raise ValidationError(
                    _("Expected Return Date must be after Allocation Date.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "assetflow.allocation"
                ) or "New"
        return super(AssetAllocation, self).create(vals_list)

    def action_allocate(self):
        self.ensure_one()
        if self.state != "draft":
            raise ValidationError(
                _("Only draft allocations can be confirmed.")
            )
        if self.asset_id.status != "available":
            raise ValidationError(
                _("The selected asset is not available for allocation.")
            )

        # Update Asset assignment
        self.asset_id.write({
            "status": "allocated",
            "employee_id": self.employee_id.id,
        })
        self.write({"state": "allocated"})
        return True

    def action_return(self):
        self.ensure_one()
        if self.state != "allocated":
            raise ValidationError(
                _("Only currently allocated assets can be returned.")
            )

        # Return Asset to pool
        self.asset_id.write({
            "status": "available",
            "employee_id": False,
        })
        self.write({
            "state": "returned",
            "actual_return_date": fields.Date.today(),
        })
        return True