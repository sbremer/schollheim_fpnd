# Copy this file to config.py and apply your local configuration

# User Config
users_config = {}
users_config['Firstname Lastname'] = 'email_address@server.com'
users_config['Firstname2 Lastname2'] = 'other_email_address@server.com'
# ... More users

# Email Config
email_config = {}
email_config['server'] = 'your-mailserver.com'
email_config['port'] = 587
email_config['auth_user'] = 'login_username'
email_config['auth_passwd'] = 'very_secret_password_goes_here'
email_config['from'] = 'Friendly Parcel Notifier Daemon <response_email_address@your-mailserver.com>'
