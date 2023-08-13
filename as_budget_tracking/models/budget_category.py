from odoo import models, fields


class BudgetCategory(models.Model):
    _name = "budget.category"
    _description = "Budget Category"

    sequence = fields.Integer()
    name = fields.Char(required=True, )
    type = fields.Selection(selection=[
            ("income", "Income"),
            ("expenses", "Expenses")], required=True, )
