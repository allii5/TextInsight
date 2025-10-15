import csv
import re
import dns.resolver


class StudentAccountsDTO:
    def __init__(self, data, files):
        self.number_of_accounts = data.get('number_of_accounts')
        self.csv_file = files.get('csv_file')
        self.errors = {}
        self.valid_emails = []
        self.invalid_emails = []
        self.duplicate_emails = []

        self._validate()

    def _validate(self):
        # Validate number_of_accounts
        try:
            self.number_of_accounts = int(self.number_of_accounts)
            if self.number_of_accounts < 1 or self.number_of_accounts > 50:
                self.errors['number_of_accounts'] = 'Number of accounts must be between 1 and 50.'
        except (ValueError, TypeError):
            self.errors['number_of_accounts'] = 'Number of accounts must be an integer.'

        # Validate csv_file
        if not self.csv_file:
            self.errors['csv_file'] = 'CSV file is required.'
        else:
            if not self.csv_file.name.endswith('.csv'):
                self.errors['csv_file'] = 'Only CSV files are allowed.'
            else:
                self._validate_csv_file()

    def _validate_csv_file(self):
        try:
            decoded_file = self.csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            headers = next(csv_reader, None)

            # Check if 'email' column exists
            if not headers or 'email' not in headers[0].lower():
                self.errors['csv_file'] = 'CSV file must have an "email" column.'
                return

            valid_email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
            seen_emails = set()

            for row in csv_reader:
                if row:
                    email = row[0].strip()
                    if email in seen_emails:
                        self.duplicate_emails.append(email)
                    else:
                        seen_emails.add(email)
                        if not valid_email_pattern.match(email) or not self._validate_email_domain(email):
                            self.invalid_emails.append(email)
                        else:
                            self.valid_emails.append(email)

            if len(self.valid_emails) == 0:
                self.errors['csv_file'] = 'No valid emails found in the uploaded CSV file. Please check and re-upload.'


        except UnicodeDecodeError:
            self.errors['csv_file'] = 'Unable to read the file. Please upload a valid CSV file.'
        except Exception as e:
            self.errors['csv_file'] = f'An error occurred while validating the file: {e}'

    def _validate_email_domain(self, email):
        """Validate if the domain in the email has MX records."""
        try:
            domain = email.split('@')[1]
            dns.resolver.resolve(domain, 'MX')
            return True
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            return False
        except Exception as e:
            print(f"Domain validation error: {e}")
            return False

    def is_valid(self):
        return len(self.errors) == 0

    def get_summary(self):
        return {
            'valid_emails': self.valid_emails,
            'invalid_emails': self.invalid_emails,
            'duplicate_emails': self.duplicate_emails,
            'requested_accounts': self.number_of_accounts,
            'valid_email_count': len(self.valid_emails),
        }
