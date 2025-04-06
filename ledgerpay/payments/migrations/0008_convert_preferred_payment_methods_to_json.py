from django.db import migrations
import json

def convert_to_json(apps, schema_editor):
    Wallet = apps.get_model('payments', 'Wallet')
    for wallet in Wallet.objects.all():
        try:
            parsed = json.loads(wallet.preferred_payment_methods)
            wallet.preferred_payment_methods = json.dumps(parsed)
        except json.JSONDecodeError:
            if wallet.preferred_payment_methods:
                fixed = wallet.preferred_payment_methods.replace("'", '"')
                try:
                    parsed = json.loads(fixed)
                    wallet.preferred_payment_methods = json.dumps(parsed)
                except json.JSONDecodeError:
                    wallet.preferred_payment_methods = json.dumps([])
            else:
                wallet.preferred_payment_methods = json.dumps([])
        wallet.save()

def reverse_convert(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0006_wallet_preferred_payment_methods'),
    ]

    operations = [
        migrations.RunPython(convert_to_json, reverse_convert),
    ]