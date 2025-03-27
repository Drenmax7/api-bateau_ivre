# Generated by Django 5.1.6 on 2025-03-27 09:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chaloupe',
            fields=[
                ('id_chaloupe', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('nom', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Connexion',
            fields=[
                ('jour', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id_evenement', models.AutoField(primary_key=True, serialize=False)),
                ('place_disponible', models.IntegerField()),
                ('date_evenement', models.DateTimeField()),
                ('titre', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_utilisateur', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('civilite', models.CharField(max_length=50)),
                ('adresse', models.CharField(max_length=200)),
                ('ville', models.CharField(max_length=50)),
                ('pays', models.CharField(max_length=50)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('code_postal', models.CharField(blank=True, max_length=15, null=True)),
                ('telephone', models.CharField(max_length=20)),
                ('complement_adresse', models.CharField(blank=True, max_length=100, null=True)),
                ('premiere_connexion', models.DateTimeField(blank=True, null=True)),
                ('derniere_connexion', models.DateTimeField(blank=True, null=True)),
                ('mail', models.EmailField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('id_client_welogin', models.PositiveIntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.college')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Societaire',
            fields=[
                ('id_societaire', models.AutoField(primary_key=True, serialize=False)),
                ('organisation', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_societaire', models.CharField(max_length=50)),
                ('id_utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartSocial',
            fields=[
                ('id_achat', models.AutoField(primary_key=True, serialize=False)),
                ('date_achat', models.DateTimeField()),
                ('quantite', models.SmallIntegerField()),
                ('numero_achat', models.SmallIntegerField()),
                ('num_facture', models.CharField(max_length=50)),
                ('id_societaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.societaire')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueConnexion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('jour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.connexion')),
            ],
            options={
                'unique_together': {('id_utilisateur', 'jour')},
            },
        ),
        migrations.CreateModel(
            name='Rejoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirige', models.BooleanField()),
                ('id_chaloupe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.chaloupe')),
                ('id_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_utilisateur', 'id_chaloupe')},
            },
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_place', models.SmallIntegerField()),
                ('id_evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.evenement')),
                ('id_utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id_utilisateur', 'id_evenement')},
            },
        ),
    ]
