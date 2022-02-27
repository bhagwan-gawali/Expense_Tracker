from django import forms
from datetime import date
from .models import ExpAccounts, ExpTransactions, Money, TrackMoney

class ExpAccountsForm(forms.ModelForm):
    class Meta:
        model = ExpAccounts
        fields = ['acc_name', 'acc_type', 'initial_amount', ]

        widgets = {
            'acc_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'acc_type': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'initial_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '15'}),

        }

    def clean_acc_name(self):
        data = self.cleaned_data.get('acc_name')
        try:
            ac_name = ExpAccounts.objects.filter(acc_name__exact=data).get()

            if ac_name:
                self.add_error('acc_name', f'Please take different account name, "{ac_name}" is already taken!.')
            
        except:
            pass

        return data

class ExpTransactionForm(forms.ModelForm):
    class Meta:
        model = ExpTransactions
        fields = ['person_name', 'amount', 'category', 'date_time', 'add_spend', 'extra_note']

        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '10'}),
            'category': forms.Select(attrs={'class': 'form-select form-select-sm', }),
            'date_time': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'value':  date.today() }),
            'add_spend': forms.Select(attrs={'class': 'form-select form-select-sm', }),
            'extra_note': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', }),
        }
        
class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['p_name', 'address', 'amount', 'date_time', 'm_number', 'cat_type']

        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '100' }),
            'address': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'maxlength': '500'}),
            'amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '10'}),
            'date_time': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'value':  date.today()}),
            'm_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '10'}),
            'cat_type': forms.Select(attrs={'class': 'form-select form-select-sm', }),
        }

    def clean_m_number(self):
        data = self.cleaned_data.get('m_number')

        if data.isdigit() == False:
            raise forms.ValidationError('It Only accept numbers.')

        return data

class IndividualPersonForm(forms.ModelForm):
    class Meta:
        model = TrackMoney
        fields = ['p_name', 'address', 'p_number',]

        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'address': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'p_number': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': 10}),
            
        }
    
    def clean_p_number(self):
        data = self.cleaned_data.get('p_number')

        if not data.isdigit():
            raise forms.ValidationError('It Only accept numbers.')

        return data

    def clean_p_name(self):
        data = self.cleaned_data.get('p_name')

        try:
            p_name = TrackMoney.objects.filter(p_name=data).get()
            if p_name.p_name:
                self.add_error('p_name', f'Please take different account name, "{p_name}" is already taken!.')
                # raise forms.ValidationError('Already taken...')
            
        except TrackMoney.DoesNotExist:
            pass

        # except forms.ValidationError:
        #     self.add_error('p_name', f'Please take different account name, "{p_name}" is already taken!.')

        return data
