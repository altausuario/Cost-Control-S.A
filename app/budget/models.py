from crum import get_current_request
from django.db import models
from django.forms import model_to_dict
from expenses.models import Expenses
from income.models import Income
from user.models import User
# Create your models here.
class Budget(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    date_creation = models.DateTimeField(auto_now_add=True)
    total_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total categories')
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total discharge')
    total = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Total')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budget')
    def __str__(self):
        return self.name
    def fecha_creation(self):
        if self.date_creation:
            return '{}'.format(self.date_creation.strftime('%Y-%m-%d'))
        return '{}'.format(self.date_creation.strftime('%Y-%m-%d'))
    def save(self, *args, **kwargs):
        request = get_current_request()
        if not self.user_id:
            self.user_id = request.user.id
        super().save(*args, **kwargs)
    def DetIncome(self):
        data = []
        for ic in IncomeConetion.objects.filter(budget_id=self.id):
            inc = ic.income_id
            for i in Income.objects.filter(id=inc):
                data.append(i)
        return data
    def DetExpenses(self):
        data = []
        for ec in ExpensesConetion.objects.filter(budget_id=self.id):
            inc = ec.expenses_id
            for e in Expenses.objects.filter(id=inc):
                data.append(e)
        return data
    def toJSON(self):
        item = model_to_dict(self)
        item['date_creation'] = self.fecha_creation()
        item['detIncome'] = [i.toJSON() for i in self.DetIncome()]
        item['detExpenses'] = [i.toJSON() for i in self.DetExpenses()]
        return item
    class Meta:
        db_table = 'tb_Budgets'
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        ordering = ['id']
class IncomeConetion(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='incomeConetion')
    income = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='incomeConetion')
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        db_table = 'tb_IncomeConetion'
        verbose_name = 'IncomeConetion'
        verbose_name_plural = 'IncomeConetions'
        ordering = ['id']
class ExpensesConetion(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expensesConetion')
    expenses = models.ForeignKey(Expenses, on_delete=models.CASCADE, related_name='expensesConetion')
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        db_table = 'tb_ExpensesConetion'
        verbose_name = 'ExpensesConetion'
        verbose_name_plural = 'ExpensesConetions'
        ordering = ['id']