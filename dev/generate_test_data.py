#  This scripts is used to insert random data into the database. This is for
#  development purposes only.
import decimal
import random
from datetime import date

from dateutil import rrule
from django.contrib.auth.models import User

from sheets.models import Category, Expense

data = dict(username="foo", email="admin@example.com", password="bar")
User.objects.create_user(**data)
print(f"Created user: {data}")

categories = []
for i, color in enumerate(
    ["#ffa502", "#2ed573", "#EA2027", "#3742fa", "#2f3542"]
):
    c = Category(name=f"Category {i + 1}", color=color)
    c.save()
    categories.append(c)


i = 1
for dt in rrule.rrule(
    rrule.DAILY, dtstart=date(2019, 6, 5), until=date(2020, 10, 26)
):
    for _ in range(int(random.expovariate(1.2))):
        data = dict(
            category=random.choice(categories),
            date=dt,
            description=f"Expense #{i} description...",
            amount=decimal.Decimal(random.uniform(1.0, 250.0)),
        )
        i += 1
        Expense(**data).save()
        print(f"Created expense: {data}")
