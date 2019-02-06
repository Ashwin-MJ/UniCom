# Generated by Django 2.1.3 on 2019-02-06 11:18

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback_with_category',
            fields=[
                ('categoryName', models.CharField(default='No category', max_length=200)),
                ('feedback_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'student_feedback_app_feedback_with_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback_with_course',
            fields=[
                ('courseName', models.CharField(default='No course', max_length=200)),
                ('date_given', models.DateTimeField(default=django.utils.timezone.now)),
                ('feedback_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('pre_defined_message_id', models.CharField(default='No message', max_length=200)),
                ('points', models.IntegerField(default=0)),
                ('datetime_given', models.DateTimeField(default=django.utils.timezone.now)),
                ('optional_message', models.CharField(default='', max_length=200)),
            ],
            options={
                'db_table': 'student_feedback_app_feedback_with_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback_with_from_user',
            fields=[
                ('fromUserName', models.CharField(default='No giving user', max_length=200)),
                ('from_user_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'student_feedback_app_feedback_with_from_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback_with_student',
            fields=[
                ('studentName', models.CharField(default='No student', max_length=200)),
                ('student_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'student_feedback_app_feedback_with_student',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', models.SlugField()),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/default_image.jpg', upload_to='profile_pictures')),
                ('id_number', models.CharField(max_length=20, unique=True)),
                ('username', models.CharField(max_length=25, unique=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_lecturer', models.BooleanField(default=False)),
                ('degree', models.CharField(default='Degree not specified', max_length=60)),
                ('bio', models.CharField(default='Biography not specified', max_length=250)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(default='Empty', max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('subject', models.CharField(max_length=40, verbose_name='Subject')),
                ('course_description', models.CharField(default='', max_length=200)),
                ('subject_slug', models.SlugField(default='empty_slug')),
                ('course_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('course_token', models.CharField(default='', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('date_given', models.DateTimeField(default=django.utils.timezone.now)),
                ('feedback_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('points', models.IntegerField(default=0)),
                ('datetime_given', models.DateTimeField(default=django.utils.timezone.now)),
                ('optional_message', models.CharField(default='', max_length=200)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_feedback_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('text', models.CharField(default='No message', max_length=200, primary_key=True, serialize=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_feedback_app.Category')),
            ],
        ),
        migrations.CreateModel(
            name='LecturerProfile',
            fields=[
                ('lecturer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('courses', models.ManyToManyField(to='student_feedback_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('score', models.IntegerField(default=0)),
                ('courses', models.ManyToManyField(to='student_feedback_app.Course')),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='from_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedback',
            name='pre_defined_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_feedback_app.Message'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='which_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_feedback_app.Course'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='PendingApproval',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('student_feedback_app.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_feedback_app.StudentProfile'),
        ),
        migrations.AddField(
            model_name='course',
            name='lecturers',
            field=models.ManyToManyField(to='student_feedback_app.LecturerProfile'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to='student_feedback_app.StudentProfile'),
        ),
    ]
