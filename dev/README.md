## Cheatsheet

1. Remove all data from the database and generate random data for testing:

   ```bash
   python manage.py flush --no-input
   python manage.py shell -c "from dev import generate_test_data"
   ```
