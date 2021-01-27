## Cheatsheet

1. Remove all data from the database and generate random data for testing:

   ```bash
   python manage.py flush --no-input
   python manage.py shell < dev/generate_test_data.py
   ```

2. Release a new version

   ```bash
   dev/release old_version new_version
   ```
