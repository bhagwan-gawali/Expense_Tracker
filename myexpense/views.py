import logging
from ossaudiodev import SNDCTL_DSP_SPEED
from pickletools import long1
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Sum
from .models import ExpAccounts, ExpTransactions, Money, TrackMoney, TrackMoneyTx
from .forms import ExpAccountsForm, ExpTransactionForm, MoneyForm, IndividualPersonForm

@login_required
def dashboard(request):
    form1 = ExpTransactionForm(request.POST)
    
    try:
        cur_acc = ExpAccounts.objects.filter(user_acc__exact=request.user, status__exact=1).get()
    except:
        cur_acc = None

    if form1.is_valid():
        add_spend = form1.cleaned_data.get('add_spend')
        amount = form1.cleaned_data.get('amount')
        date = form1.cleaned_data.get('date_time')
        person_name = form1.cleaned_data.get('person_name')
        category = form1.cleaned_data.get('category')
        extra_note = form1.cleaned_data.get('extra_note')

        if (amount > cur_acc.rem_amount) and (add_spend == 0):
            messages.add_message(request, messages.INFO, f'Not enough money to spend from "{cur_acc.acc_name}".')
            return redirect(reverse('myexpense:dashboard'))
        else:
            tx = ExpTransactions(add_spend=add_spend, amount=amount, 
                                date_time=date, person_name=person_name, 
                                category=category, extra_note=extra_note, exp_acc=cur_acc
                                )
            tx.save()

            if add_spend == 0:
                cur_acc.rem_amount -= amount
                cur_acc.save()
            elif add_spend == 1:
                cur_acc.rem_amount += amount
                cur_acc.save()

            messages.add_message(request, messages.SUCCESS, f'{person_name} make the transaction for {amount}')

            return redirect(reverse('myexpense:dashboard'))
    

    data = {'cur_acc': cur_acc, 'form1': form1,}

    return render(request, 'myexpense/pages/dashboard.html', data)

@login_required
def exp_accounts(request):
    form = ExpAccountsForm(request.POST)
    all_exp_acc = ExpAccounts.objects.filter(user_acc__exact=request.user).order_by('-id')

    paginator = Paginator(all_exp_acc, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        def_acc = ExpAccounts.objects.filter(status__exact=1, user_acc=request.user).get()
    except:
        def_acc =  None
    
    if form.is_valid():
        acc_name = form.cleaned_data.get('acc_name')
        acc_type = form.cleaned_data.get('acc_type')
        acc_amount = form.cleaned_data.get('initial_amount')

        exp_acc = ExpAccounts(acc_name=acc_name, acc_type=acc_type, initial_amount=acc_amount, rem_amount=acc_amount, user_acc=request.user)
        exp_acc.save()
        messages.add_message(request, messages.SUCCESS, f'"{acc_name}" Account Created Successfully.')

        return redirect(reverse('myexpense:exp_accounts'))

    
    data = {'form': form, 'exp_acc': all_exp_acc, 'def_acc': def_acc, 'page_obj': page_obj}

    return render(request, 'myexpense/pages/accounts.html', data)

@login_required
def set_default(request, id):
    old_acc = ExpAccounts.objects.filter(status=1)

    if old_acc:
        for acc in old_acc:
            acc.status = 0
            acc.save()
    new_acc = ExpAccounts.objects.get(pk=id)
    new_acc.status = 1
    new_acc.save()

    return redirect(reverse('myexpense:exp_accounts'))

@login_required
def borrow_lent_money(request):
    form2 = MoneyForm(request.POST)

    try:
        all_money = Money.objects.filter(user=request.user).order_by('-id').all()

        br_money = Money.objects.filter(user=request.user, cat_type=0).aggregate(br_sum=Sum('amount'))
        lent_money = Money.objects.filter(user=request.user, cat_type=1).aggregate(lt_sum=Sum('amount'))

        paginator = Paginator(all_money, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = None

    if form2.is_valid():
        person_name = form2.cleaned_data.get('p_name')
        amount = form2.cleaned_data.get('amount')
        date = form2.cleaned_data.get('date_time')
        m_number = form2.cleaned_data.get('m_number')
        cat_type = form2.cleaned_data.get('cat_type')
        address = form2.cleaned_data.get('address')

        money = Money(p_name=person_name, address=address,
                     amount=amount, date_time=date, 
                     m_number=m_number, 
                     cat_type=cat_type, user=request.user
                     )

        money.save()

        messages.add_message(request, messages.SUCCESS, f'{amount} Rupees Transaction has Done!.')

        return redirect(reverse('myexpense:borrow_lent'))


    data = {'form2': form2, 'page_obj': page_obj, 'borrowed_money': br_money['br_sum'], 'lent_money': lent_money['lt_sum']}
    return render(request, 'myexpense/pages/borrow_lent_money.html', data)

@login_required
def my_trnsactions(request):

    try:
        print("In try block...")
        def_acc = ExpAccounts.objects.filter(user_acc=request.user, status=1).get()
        all_tx = ExpTransactions.objects.filter(exp_acc=def_acc).order_by('id')

        paginator = Paginator(all_tx, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        data = {'page_obj': page_obj}
    except:
        print("catch in except")
        def_acc = None
        data = {}    
    
    return render(request, 'myexpense/pages/transactions.html', data)

@login_required
def manage_borrow_lent(request):

    if request.method == 'POST' and request.POST.get('submit') == 'yes':
        p_name = request.POST.get('p_name')

        result = Money.objects.filter(user=request.user, p_name__icontains=p_name).order_by('id').all()
        paginator = Paginator(result, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    else:
        try:
            all_money = Money.objects.filter(user=request.user).order_by('-id').all()

            paginator = Paginator(all_money, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        except:
            page_obj = None

    data = {'page_obj': page_obj}

    return render(request, 'myexpense/pages/manage_borrow_lent.html', data)

@login_required
def make_paid_transaction(request):

    if request.method == 'POST':
        tx_id = request.POST.get('tx_id')

        tx_acc = Money.objects.filter(user=request.user, pk=tx_id).get()

        tx_acc.status = '1'
        tx_acc.save()

        return redirect(reverse('myexpense:manage_borrow_lent'))
    
    messages.add_message(request, messages.WARNING, 'We cant make changes to this transaction.')
    return redirect(reverse('myexpense:manage_borrow_lent'))

@login_required
def make_notpaid_transaction(request):

    if request.method == 'POST':
        tx_id = request.POST.get('tx_id')

        tx_acc = Money.objects.filter(user=request.user, pk=tx_id).get()

        tx_acc.status = '0'
        tx_acc.save()

        return redirect(reverse('myexpense:manage_borrow_lent'))
    
    messages.add_message(request, messages.WARNING, 'We cant make changes to this transaction.')
    return redirect(reverse('myexpense:manage_borrow_lent'))

@login_required
def individual_p_account(request):
    form = IndividualPersonForm(request.POST or None)
    money_data = TrackMoney.objects.filter(user=request.user).order_by('-id').all()

    try:
        paginator = Paginator(money_data, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except:
        pass


    if form.is_valid():
        p_name = form.cleaned_data.get('p_name')
        address = form.cleaned_data.get('address')
        p_number = form.cleaned_data.get('p_number')

        tx_money = TrackMoney(p_name=p_name, address=address, p_number=p_number, user=request.user)
        tx_money.save()

        return redirect(reverse('myexpense:individual_person_account'))
        

    data = {'form': form, 'm_data': money_data, 'page_obj': page_obj}

    return render(request, 'myexpense/pages/individual_p_account.html', data)

@login_required
def manage_individual_p_account(request, id):

    p_data = TrackMoney.objects.filter(id=id).get()

    try:
        tx_data = TrackMoneyTx.objects.filter(trackmoney_acc=p_data)
        paginator = Paginator(tx_data, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except:
        print("No Transaction record found...")

    if request.method == 'POST':
        
        original_amount = request.POST.get('original_amount')
        paid_amount = request.POST.get('paid_amount')
        notes = request.POST.get('extra_notes')

        rem_amount = float(paid_amount) - float(original_amount)
        p_data.amount += rem_amount
        p_data.save()

        my_tx = TrackMoneyTx(original_amount=original_amount, paid_amount=paid_amount, rem_amount=rem_amount, extra_note=notes, trackmoney_acc=p_data)
        my_tx.save()

        return redirect(reverse('myexpense:manage_individual_person_account', args=[id,]))


        # if flag == '1':
        #     p_data.amount += int(amount)
        #     p_data.save()
        #     tx_money = TrackMoneyTx(amount=amount, flag=flag, extra_note=notes, trackmoney_acc=p_data)
        #     tx_money.save()
        #     p_data.tx_acc.add(tx_money)
        # elif flag == '0':
        #     if p_data.amount < 0:
        #         p_data.amount = abs(p_data.amount) - int(amount)
        #         p_data.amount *= -1
        #         p_data.save()
        #     else:
        #         p_data.amount -= int(amount)
        #         p_data.save()
        #     tx_money = TrackMoneyTx(amount=amount, extra_note=notes, flag=flag, trackmoney_acc=p_data)
        #     tx_money.save()
        #     p_data.tx_acc.add(tx_money)


    data = {'p_data': p_data, 'tx_data': tx_data, 'page_obj': page_obj}

    return render(request, 'myexpense/pages/manage_individual_p_account.html', data)

