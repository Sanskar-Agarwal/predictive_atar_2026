from django.db import models
from core.utility.tools import *
from django.db import transaction


# Create your models here.
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('region_name', max_length=255)
    abbreviation = models.CharField('abbr', max_length=255)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return f"{self.id} - {self.name} - {self.abbreviation}"

    @classmethod
    def get_id_by_abbreviation(cls, abbreviation):
        try:
            region = cls.objects.get(abbreviation=abbreviation)
            return region.id
        except cls.DoesNotExist:
            return None


class GradeType(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField('description', max_length=255)
    label = models.CharField('label', max_length=255, unique=True)

    class Meta:
        db_table = 'grade_type'

    def __str__(self):
        return self.label


# class School(models.Model):
#     name = models.CharField('school_name', max_length=255)
#     id = models.AutoField(primary_key=True)
#     regionid = models.ForeignKey(Region, on_delete=models.CASCADE)
#     gradeTypeID = models.ForeignKey(GradeType, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'core'
#
#     def __str__(self):
#         return self.name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField('subject', max_length=255)
    units = models.CharField('unit', max_length=255)
    category = models.CharField('category', max_length=255)
    regionid = models.ForeignKey(Region, on_delete=models.CASCADE)
    is_language = models.BooleanField(null=True, default=None)

    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.subject


class BasicSubject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('title', max_length=255)
    regionid = models.ForeignKey(Region, on_delete=models.CASCADE)
    ## deleting the referenced record will also delete all records that have a foreign key pointing to it
    subjectid = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'basic_subject'

    def __str__(self):
        return self.title


class ApplicationStudentSubject(models.Model):
    application_student = models.ForeignKey('ApplicationStudent', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.CharField(max_length=255)
    create_time = models.TimeField(auto_now_add=True)

    class Meta:
        db_table = 'application_student_subject'
        unique_together = ('application_student', 'subject')


class ApplicationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    applicantionid = models.IntegerField('application_id')
    atar = models.IntegerField('atar')
    regionid = models.IntegerField("region_id")
    name = models.CharField('name', max_length=255, null=True)
    note = models.CharField('note', max_length=500, null=True)
    subjects = models.ManyToManyField(Subject, through=ApplicationStudentSubject)
    create_time = models.TimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'application_student'

    def __str__(self):
        return f"Application ID: {self.applicantionid}, ATAR: {self.atar}, Subjects: {', '.join(str(subject) for subject in self.subjects.all())}"


class Tas_scaling(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField('code', max_length=255)
    course = models.CharField('course', max_length=255)
    nnpa_n = models.IntegerField('nn/pa_n')
    sa_min = models.IntegerField('sa_min')
    sa_max = models.IntegerField('sa_max')
    sa_n = models.IntegerField('sa_n')
    ca_min = models.IntegerField('ca_min')
    ca_max = models.IntegerField('ca_max')
    ca_n = models.IntegerField('ca_n')
    ha_min = models.IntegerField('ha_min')
    ha_max = models.IntegerField('ha_max')
    ha_n = models.IntegerField('ha_n')
    ea_min = models.IntegerField('ea_min')
    ea_max = models.IntegerField('ea_max')
    ea_n = models.IntegerField('ea_n')

    class Meta:
        db_table = 'tas_scaling'

    def __str__(self):
        return f"CODE: {self.code}, course:{self.course}"

    @classmethod
    def load_data_from_file(cls, df):
        try:
            df.columns = df.columns.str.lower()

            # Create a list of Tas_scaling objects
            tas_scaling_objects = [
                cls(
                    code=row["code"],
                    course=row["course"],
                    nnpa_n=row["nn/pa_n"],
                    sa_min=row["sa_min"],
                    sa_max=row["sa_max"],
                    sa_n=row["sa_n"],
                    ca_min=row["ca_min"],
                    ca_max=row["ca_max"],
                    ca_n=row["ca_n"],
                    ha_min=row["ha_min"],
                    ha_max=row["ha_max"],
                    ha_n=row["ha_n"],
                    ea_min=row["ea_min"],
                    ea_max=row["ea_max"],
                    ea_n=row["ea_n"],
                )
                for _, row in df.iterrows()
            ]

            # Bulk create the objects
            cls.objects.bulk_create(tas_scaling_objects)

            return True  # Success

        except Exception as e:
            print(f"Error loading data: {e}")
            return False  # Failure


class Nsw_scaling(models.Model):
    class Meta:
        db_table = 'nsw_scaling'

    id = models.IntegerField(primary_key=True)
    course = models.CharField(max_length=50)
    number = models.IntegerField(null=True)
    type_of_mark = models.CharField(max_length=20)
    mean = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    sd = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    max_mark = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    p99 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    p90 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    p75 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    p50 = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    p25 = models.DecimalField(max_digits=4, decimal_places=1, null=True)


class Nsw_atar(models.Model):
    class Meta:
        db_table = 'nsw_atar'

    id = models.IntegerField(primary_key=True)
    atar = models.DecimalField(max_digits=5, decimal_places=2)
    year = models.IntegerField()
    score = models.DecimalField(max_digits=6, decimal_places=1)


class Wa_scaling(models.Model):
    class Meta:
        db_table = 'wa_scaling'

    id = models.IntegerField(primary_key=True)
    course = models.CharField(max_length=50)
    mean = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    min_mark = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    max_mark = models.DecimalField(max_digits=4, decimal_places=1, null=True)


class Wa_atar(models.Model):
    class Meta:
        db_table = 'wa_atar'

    id = models.IntegerField(primary_key=True)
    atar = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    min_tea = models.DecimalField(max_digits=5, decimal_places=1, null=True)


class Sa_atar(models.Model):
    class Meta:
        db_table = 'sa_atar'

    id = models.IntegerField(primary_key=True)
    aggregate = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    atar = models.DecimalField(max_digits=4, decimal_places=2, null=True)


class Tas_atar(models.Model):
    class Meta:
        db_table = 'tas_atar'

    id = models.IntegerField(primary_key=True)
    tes = models.IntegerField(null=True)
    atar = models.DecimalField(max_digits=4, decimal_places=2, null=True)


class Tas_subject(models.Model):
    class Meta:
        db_table = 'tas_subject'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField(null=True)


class Tas_scaling_alt(models.Model):
    class Meta:
        db_table = 'tas_scaling_alt'

    id = models.IntegerField(primary_key=True)
    course = models.CharField(max_length=100)
    sa_min = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    sa_max = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ca_min = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ca_max = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ha_min = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ha_max = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ea_min = models.DecimalField(decimal_places=1, null=True, max_digits=4)
    ea_max = models.DecimalField(decimal_places=1, null=True, max_digits=4)


class Vic_scaling(models.Model):
    class Meta:
        db_table = 'vic_scaling'

    id = models.IntegerField(primary_key=True)
    study_code = models.CharField(max_length=10)  # Study code, such as 'AC', 'AH', 'AL03'
    study_name = models.CharField(max_length=50)  # Study name, such as 'Accounting', 'Agricultural & Horticultural Studies'
    mean = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Mean score for the scaling
    sd = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Standard deviation for the scaling

    # Scaled scores corresponding to different study scores
    scaled_score_20 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 20
    scaled_score_25 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 25
    scaled_score_30 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 30
    scaled_score_35 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 35
    scaled_score_40 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 40
    scaled_score_45 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 45
    scaled_score_50 = models.DecimalField(max_digits=4, decimal_places=2, null=True)  # Scaled score for a study score of 50
    
    category = models.CharField(max_length=50, null=True)
    group = models.CharField(max_length=50, null=True)


class Vic_atar(models.Model):
    class Meta:
        db_table = 'vic_atar'

    id = models.IntegerField(primary_key=True)
    atar = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # The ATAR score

    # The range of scaled aggregates corresponding to the particular ATAR score
    range_low = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    range_high = models.DecimalField(max_digits=5, decimal_places=2, null=True)


from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['c_time']

class Invitation(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=32, unique=True)
    is_used = models.BooleanField(default=False)

CustomUser._meta.get_field('groups').remote_field.related_name = 'customuser_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'
