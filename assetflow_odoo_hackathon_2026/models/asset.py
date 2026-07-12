from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Asset(models.Model):
    _name = "assetflow.asset"
    _description = "Asset"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "asset_code desc, id desc"

    name = fields.Char(string="Asset Name", required=True, tracking=True)
    asset_code = fields.Char(
        string="Asset Code",
        copy=False,
        readonly=True,
        default="New",
        tracking=True,
    )
    serial_no = fields.Char(string="Serial Number", tracking=True)
    category_id = fields.Many2one(
        "assetflow.asset.category",
        string="Category",
        required=True,
        tracking=True,
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Assigned Employee",
        readonly=True,
        tracking=True,
    )
    purchase_date = fields.Date(string="Purchase Date", tracking=True)
    purchase_cost = fields.Float(string="Purchase Cost", tracking=True)
    status = fields.Selection(
        [
            ("available", "Available"),
            ("allocated", "Allocated"),
            ("maintenance", "Under Maintenance"),
            ("lost", "Lost"),
            ("retired", "Retired"),
            ("disposed", "Disposed"),
        ],
        default="available",
        tracking=True,
    )
    image = fields.Image(string="Asset Image")
    note = fields.Text(string="Internal Notes")
    active = fields.Boolean(default=True, tracking=True)

    allocation_ids = fields.One2many(
        "assetflow.asset.allocation",
        "asset_id",
        string="Allocation Logs",
    )
    maintenance_ids = fields.One2many(
        "assetflow.maintenance",
        "asset_id",
        string="Maintenance Logs",
    )
    audit_line_ids = fields.One2many(
        "assetflow.audit.line",
        "asset_id",
        string="Audit Logs",
    )
    history_ids = fields.One2many(
        "assetflow.asset.history",
        "asset_id",
        string="History",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("asset_code", "New") == "New":
                vals["asset_code"] = self.env["ir.sequence"].next_by_code(
                    "assetflow.asset"
                ) or "New"
        records = super(Asset, self).create(vals_list)
        for record in records:
            # Create registration history
            self.env["assetflow.asset.history"].create({
                "asset_id": record.id,
                "action": "registered",
                "current_status": record.status,
                "remarks": _("Asset registered in the system."),
            })
        return records

    def write(self, vals):
        # Tracking status change to create history records
        if "status" in vals:
            for rec in self:
                old_status = rec.status
                new_status = vals["status"]
                if old_status != new_status:
                    action = "registered"
                    remarks = ""
                    if new_status == "allocated":
                        action = "allocated"
                        remarks = _("Asset allocated to employee: %s") % (vals.get("employee_id") or rec.employee_id.name or "N/A")
                    elif new_status == "available":
                        if old_status == "allocated":
                            action = "returned"
                            remarks = _("Asset returned by employee.")
                        elif old_status == "maintenance":
                            action = "returned"
                            remarks = _("Asset returned from maintenance.")
                        else:
                            action = "registered"
                            remarks = _("Asset status marked as Available.")
                    elif new_status == "maintenance":
                        action = "maintenance"
                        remarks = _("Asset sent to maintenance.")
                    elif new_status == "lost":
                        action = "audit"
                        remarks = _("Asset marked as Lost.")
                    elif new_status == "retired":
                        action = "retired"
                        remarks = _("Asset retired.")
                    elif new_status == "disposed":
                        action = "disposed"
                        remarks = _("Asset disposed.")

                    self.env["assetflow.asset.history"].create({
                        "asset_id": rec.id,
                        "employee_id": vals.get("employee_id") or rec.employee_id.id,
                        "action": action,
                        "previous_status": old_status,
                        "current_status": new_status,
                        "remarks": remarks,
                    })

        return super(Asset, self).write(vals)

    def action_request_transfer(self):
        self.ensure_one()
        return {
            "name": _("Request Transfer"),
            "type": "ir.actions.act_window",
            "res_model": "assetflow.transfer",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_asset_id": self.id,
                "default_from_employee_id": self.employee_id.id,
            }
        }