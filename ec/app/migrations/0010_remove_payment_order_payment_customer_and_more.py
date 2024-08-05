# Generated by Django 5.0.4 on 2024-04-15 00:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_order_payment_delete_orderplaced'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.AddField(
            model_name='payment',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.customer'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='Credit Card', max_length=50),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Chấp nhận', 'Chấp nhận'), ('Đóng gói', 'Đóng gói'), ('Đang giao hàng', 'Đang giao hàng'), ('Đã giao hàng', 'Đã giao hàng'), ('Hủy', 'Hủy'), ('Chờ xử lý', 'Chờ xử lý')], default='Chờ xử lý', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='order_placed',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.orderplaced'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
