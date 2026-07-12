from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TransferRequest(models.Model):
    _name = "assetflow.transfer"
    _description = "Asset Transfer Request"
    _order = "request_date desc, id desc"

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
        domain="[('status', '=', 'allocated')]",
    )
    from_employee_id = fields.Many2one(
        "hr.employee",
        string="From Employee",
        readonly=True,
    )
    to_employee_id = fields.Many2one(
        "hr.employee",
        string="To Employee",
        required=True,
    )
    request_date = fields.Date(
        string="Request Date",
        default=fields.Date.today,
        required=True,
    )
    reason = fields.Text(string="Reason for Transfer")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("requested", "Requested"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        string="Status",
    )

    @api.onchange("asset_id")
    def _onchange_asset_id(self):
        if self.asset_id:
            self.from_employee_id = self.asset_id.employee_id
        else:
            self.from_employee_id = False

    @api.constrains("from_employee_id", "to_employee_id")
    def _check_employees(self):
        for rec in self:
            if rec.from_employee_id == rec.to_employee_id:
                raise ValidationError(
                    _("From Employee and To Employee cannot be the same.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "assetflow.transfer"
                ) or "New"
            # Auto-populate from_employee_id if not set in multi-create
            if vals.get("asset_id") and not vals.get("from_employee_id"):
                asset = self.env["assetflow.asset"].browse(vals["asset_id"])
                vals["from_employee_id"] = asset.employee_id.id
        return super(TransferRequest, self).create(vals_list)

    def action_submit(self):
        self.ensure_one()
        if self.state != "draft":
            raise ValidationError(
                _("Only draft transfers can be submitted.")
            )
        if not self.from_employee_id:
            self.from_employee_id = self.asset_id.employee_id
        if not self.from_employee_id:
            raise ValidationError(
                _("The selected asset is not currently assigned to any employee.")
            )
        self.write({"state": "requested"})
        return True

    def action_approve(self):
        self.ensure_one()
        if self.state != "requested":
            raise ValidationError(
                _("Only submitted transfer requests can be approved.")
            )
        if self.asset_id.status != "allocated" or self.asset_id.employee_id != self.from_employee_id:
            raise ValidationError(
                _("Asset assignment has changed. Transfer is no longer valid.")
            )

        # 1. Close the current allocation record
        current_allocation = self.env["assetflow.asset.allocation"].search(
            [
                ("asset_id", "=", self.asset_id.id),
                ("employee_id", "=", self.from_employee_id.id),
                ("state", "=", "allocated"),
            ],
            limit=1,
        )
        if current_allocation:
            # We bypass regular return method to avoid setting status to available
            current_allocation.write({
                "state": "returned",
                "actual_return_date": fields.Date.today(),
            })

        # 2. Create the new allocation record for target employee
        new_allocation = self.env["assetflow.asset.allocation"].create({
            "asset_id": self.asset_id.id,
            "employee_id": self.to_employee_id.id,
            "allocation_date": fields.Date.today(),
            "notes": _("Transferred from %s. Ref: %s") % (self.from_employee_id.name, self.name),
        })
        # Bypassing double allocation validation by writing state & asset directly
        new_allocation.write({"state": "allocated"})

        # 3. Update the asset employee & trigger history log
        self.asset_id.write({
            "employee_id": self.to_employee_id.id,
            "status": "allocated",
        })

        # Log History for transfer
        self.env["assetflow.asset.history"].create({
            "asset_id": self.asset_id.id,
            "employee_id": self.to_employee_id.id,
            "action": "transfer",
            "previous_status": "allocated",
            "current_status": "allocated",
            "remarks": _("Asset transferred from %s to %s. Reason: %s") % (self.from_employee_id.name, self.to_employee_id.name, self.reason or ""),
        })

        self.write({"state": "approved"})
        return True

    def action_reject(self):
        self.ensure_one()
        if self.state != "requested":
            raise ValidationError(
                _("Only submitted transfer requests can be rejected.")
            )
        self.write({"state": "rejected"})
        return True
