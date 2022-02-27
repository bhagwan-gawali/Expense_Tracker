from django.contrib import admin

from .models import Money, ExpAccounts, ExpTransactions, TrackMoney, TrackMoneyTx

admin.site.register(Money)
admin.site.register(ExpAccounts)
admin.site.register(ExpTransactions)
admin.site.register(TrackMoney)
admin.site.register(TrackMoneyTx)
