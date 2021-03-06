# Generated by Django 3.2.5 on 2022-03-20 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='concentration',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='course',
            name='campus',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='cognate_course',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='concentration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rest.concentration'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='credit_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.CharField(blank=True, choices=[('CS', 'CS'), ('ECE', 'ECE'), ('Statistics', 'Statistics'), ('Math', 'Math')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='faculty',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='learning_objective',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='modality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='prerequisite_concepts',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='prerequisite_courses',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rest.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='special_study',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='syllabus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='term_offering',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='degreerequirement',
            name='comparator',
            field=models.CharField(blank=True, choices=[('AL', 'At least'), ('AM', 'At most')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='degreerequirement',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rest.course'),
        ),
        migrations.AlterField(
            model_name='degreerequirement',
            name='value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
