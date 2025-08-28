def mask_email(email):
    if not email or '@' not in email:
        return email
    a,b = email.split('@',1)
    if len(a) <= 1:
        return '***@' + b
    return a[0] + '***@' + b

def apply_role_masking(results, role='analyst'):
    masked = []
    for r in results:
        row = r.copy()
        if 'email_address' in row and role != 'admin':
            row['email_address'] = mask_email(row['email_address'])
        masked.append(row)
    return masked
