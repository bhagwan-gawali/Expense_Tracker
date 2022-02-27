from logging.config import valid_ident
from django.db import models
from django.core.validators import MaxValueValidator, MaxLengthValidator
from django.contrib.auth.models import User
from django.utils import timezone

class ExpAccounts(models.Model):
    '''Models for Expense Account '''
    acc_name = models.CharField('Account Name', max_length=100)
    acc_type = models.CharField(max_length=60, choices=[('personal', 'Personal'), ('commercial', 'Commercial'), ('other', 'Other')])
    initial_amount = models.FloatField(default=0.0, max_length=15)
    rem_amount = models.FloatField(default=0.0)
    status = models.IntegerField(default=0)
    date_created = models.DateField(default=timezone.now)
    user_acc = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.acc_name

class ExpTransactions(models.Model):
    CHOICES = [
        ('food', 'Food'),
        ('hospital', 'Hospital'),
        ('other_income', 'Other Income'),
        ('pension','Pension'),
        ('gift', 'Gift'),
        ('travel', 'Travel'),
        ('refund', 'Refund'),
        ('grocery', 'Grocery'),
        ('restourant', 'Restourant'),
        ('supermarket', 'Supermarket'),
        ('bus', 'Bus'),
        ('car', 'Car'),
        ('metro', 'Metro'),
        ('health', 'Health'),
        ('toll', 'Toll'),
        ('house', 'House'),
        ('train', 'Train'),
        ('airplane', 'Airplane'),
        ('visits', 'Visits'),
        ('fuel', 'Fuel'),
        ('gas', 'Gas'),
        ('repair', 'Repair'),
        ('maintanance', 'Maintanance'),
        ('parking', 'Parking'),
        ('fines', 'Fines'),
        ('loan_mortages', 'Loan/Mortages'),
        ('hotel', 'Hotel'),
        ('rent', 'Rent'),
        ('tv', 'TV'),
        ('furniture', 'Furniture'),
        ('decoration', 'Decoration'),
        ('water', 'Water'),
        ('books', 'Books'),
        ('phone', 'Phone'),
        ('doctor', 'Docter'),
        ('travel', 'Travel'),
        ('garden', 'Garden'),
        ('movies', 'Movies'),
        ('clothing', 'Clothing'),
        ('dalan', 'dalan'),
        ('market', 'Market'),
        ('other', 'Other'),
    ]
    person_name = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=100, choices=CHOICES)
    date_time = models.DateField(default=timezone.now)
    add_spend = models.IntegerField(choices=[(0, 'Spend'), (1, 'Add')]) # 0 -> spend, 1 -> add
    extra_note = models.TextField()
    exp_acc = models.ForeignKey(ExpAccounts, on_delete=models.CASCADE)

    def __str__(self):
        return self.person_name

class Money(models.Model):
    p_name = models.CharField(max_length=100)
    address = models.TextField()
    amount = models.FloatField()
    date_time = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50, default='0')
    m_number = models.CharField(max_length=10)
    cat_type = models.CharField(max_length=50, choices=(('0', 'Borrow Money'), ('1', 'Lent Money'))) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TrackMoney(models.Model):
    p_name = models.CharField(max_length=50, verbose_name='Person Name')
    amount = models.FloatField(default=0.0)
    address = models.TextField()
    p_number = models.CharField(max_length=10, verbose_name='Mobile Number')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateField(default=timezone.now)
    tx_acc = models.ManyToManyField('TrackMoneyTx')

    def __str__(self):
        return self.p_name


class TrackMoneyTx(models.Model):
    original_amount = models.FloatField(default=0.0)
    paid_amount = models.FloatField()
    rem_amount = models.FloatField()
    total_amount = models.FloatField(default=0.0)
    extra_note = models.TextField()
    date_time = models.DateField(default=timezone.now)
    trackmoney_acc = models.ForeignKey(TrackMoney, on_delete=models.CASCADE)

    def __str__(self):
        return self.trackmoney_acc.p_name
