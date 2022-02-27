## ExpTracker (Django-powered) App

- ### Introduction

	- The ExpTracker App allow to manage your daily expense.
	- In this app you can add as many accounts as you want.
	- In each account you can make as many transaction as you want.

---

- ### App Structure

	- This project contain two apps.
		- accounts app
		- myexpense app
	- The accounts app manage the user data.
	- The myexpense app manages the all data related to the expense(transactions, expense accounts.)

---

- ### How to Install on local machine
	- Create virtual environmnet with python-env
	- clone the github directory or download it
	- install the required packages in requirements.txt file with pip.
	- now run the local development server provided by the django.
	
- ### Sections
	- #### Accounts:
		- Manage all your accounts relerated to expense.
	- #### My Transactions
		- views all your Transaction's.

	- #### Borrow / Lent Money
		- you can record all borrowed or Lented money with the person details.

	- #### Individual Person Account's
		- Create an individual person account and manage their transactions.

---

- ### How to Use

	- step 1 :
		- Create a user account by hitting the register link on the login page.

	- step 2 :
		- Now login with the created user account (use username and password)
	- step 3 :
		- Now go to **Accounts** section.
		- Create new **New ExpAccount** 
		- If you created multiple accounts then you have to set the any one accunt as the **default** account.
		- Now you are done here!
	- step 4 :
		- Go to the **Dashboard** section.
		- Now you can see the **ExpAccount** Detail's.
		- and with the following forms you can add or spend money from your account.
		- If you want to see your transactions in your **ExpAccount** then go to the **My Transactions** section.
	- step 5 :
		- Borrow / Lent Money.
		- This is the seperate section for keeping record's for borrowed or lented money.
	- step 6 :
		- Individual Person's Account
		- Create Person Account with their name, address, mobile number.
		- Now go to the **view_data** link.
		- In this page you can make and record the transactions with that person.

---