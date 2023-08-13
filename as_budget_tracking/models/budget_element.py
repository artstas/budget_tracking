from odoo import models, fields, api


class BudgetElement(models.Model):
    _name = "budget.element"
    _description = "Budget Element"

    name = fields.Char(required=True)
    date_start = fields.Date(required=True)
    date_finish = fields.Date(required=True)
    currency_id = fields.Many2one(comodel_name="res.currency", )
    total_amount = fields.Monetary(
        compute="_compute_total_amount", store=True, )
    total_income = fields.Monetary(
        compute="_compute_total_amount", store=True, )
    total_expenses = fields.Monetary(
        compute="_compute_total_amount", store=True, )
    line_ids = fields.One2many(
        comodel_name="budget.element.line",
        inverse_name="budget_element_id", )

    @api.depends("line_ids")
    def _compute_total_amount(self):
        for obj in self:
            if obj.line_ids and obj.id:
                total_income = sum(self.env["budget.element.line"].search([
                    ("budget_element_id", "=", obj.id),
                    ("type", "=", "income")]).mapped("amount"))
                total_expenses = sum(self.env["budget.element.line"].search([
                        ("budget_element_id", "=", obj.id),
                        ("type", "=", "expenses")]).mapped("amount"))
                obj.total_amount = total_income - total_expenses
                obj.total_income = total_income
                obj.total_expenses = total_expenses
            else:
                obj.total_amount = 0
                obj.total_income = 0
                obj.total_expenses = 0


class BudgetElementLine(models.Model):
    _name = "budget.element.line"
    _description = "Budget Element Line"

    sequence = fields.Integer()
    budget_element_id = fields.Many2one(comodel_name="budget.element", )
    date = fields.Datetime(
        required=True, default=lambda self: fields.Datetime.now(), )
    type = fields.Selection(selection=[
            ("income", "Income"),
            ("expenses", "Expenses")], related="category_id.type",
    )
    note = fields.Char()
    category_id = fields.Many2one(
        comodel_name="budget.category", required=True, )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="budget_element_id.currency_id", )
    amount = fields.Monetary(required=True, )
