from odoo import api, fields, models


class AssetFlowDashboard(models.TransientModel):
    _name = "assetflow.dashboard"
    _description = "AssetFlow Dashboard"

    assets_available = fields.Integer(compute="_compute_dashboard")
    assets_allocated = fields.Integer(compute="_compute_dashboard")
    maintenance_today = fields.Integer(compute="_compute_dashboard")
    active_bookings = fields.Integer(compute="_compute_dashboard")
    pending_transfers = fields.Integer(compute="_compute_dashboard")
    upcoming_returns = fields.Integer(compute="_compute_dashboard")

    @api.depends()
    def _compute_dashboard(self):
        Asset = self.env["assetflow.asset"]
        Allocation = self.env["assetflow.asset.allocation"]
        Maintenance = self.env["assetflow.maintenance"]
        Booking = self.env["assetflow.booking"]
        Transfer = self.env["assetflow.transfer"]

        today = fields.Date.today()

        for rec in self:
            rec.assets_available = Asset.search_count([
                ("status", "=", "available")
            ])

            rec.assets_allocated = Asset.search_count([
                ("status", "=", "allocated")
            ])

            rec.maintenance_today = Maintenance.search_count([
                ("create_date", ">=", today)
            ])

            rec.active_bookings = Booking.search_count([
                ("state", "=", "approved")
            ])

            rec.pending_transfers = Transfer.search_count([
                ("state", "=", "requested")
            ])

            rec.upcoming_returns = Allocation.search_count([
                ("expected_return_date", ">=", today),
                ("state", "=", "allocated")
            ])