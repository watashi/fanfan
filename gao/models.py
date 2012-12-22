# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from decimal import Decimal

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Account(BaseModel):
    name = models.CharField(max_length=80, unique=True)

    def __unicode__(self):
        return '#%s' % self.name

    def balance(self):
        income = self.receive_records.aggregate(Sum('amount'))['amount__sum']
        expenditure = self.send_records.aggregate(Sum('amount'))['amount__sum']
        return (income or Decimal(0)) - (expenditure or Decimal(0))

class Good(BaseModel):
    name = models.CharField(max_length=80, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    account_set = models.ManyToManyField(Account)

    def __unicode__(self):
        return u'%s(¥%s)' % (self.name, self.price)

class Record(BaseModel):
    account_from = models.ForeignKey(Account, related_name='send_records')
    account_to = models.ForeignKey(Account, related_name='receive_records')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s ==¥%s=> %s: %s' % (self.account_from, self.amount, self.account_to, self.comment)

