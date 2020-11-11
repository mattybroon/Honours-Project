from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
import datetime


def yearSelection():
    yearDropdown = []
    for y in range(2018, (datetime.datetime.now().year + 2)):
        yearDropdown.append((y, y))
    return yearDropdown


def defaultAssignmentMark():
    return [0]


class Module(models.Model):
    SEMESTER_CHOICES = [('ATM', 'Autumn'), ('SPR', 'Spring'), ('SMR', 'Summer')]
    OCCURRENCE_CHOICES = [('A', 'Stirling'), ('D', 'Muscat')]

    module_code = models.CharField(max_length=7, primary_key=True)
    module_name = models.CharField(max_length=100)
    module_coordinator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=3, choices=SEMESTER_CHOICES, default='AUT')
    occurrence = models.CharField(max_length=2, choices=OCCURRENCE_CHOICES, default='A')
    module_credits = models.IntegerField(default=20)
    module_SCQF = models.IntegerField(default=0)
    number_of_checkpoints = models.IntegerField(default=0)
    checkpoint_weight = models.IntegerField(default=0)
    assignment_mark_total = ArrayField(models.IntegerField(default=100))
    assignment_weight = models.IntegerField(default=50)
    exam_mark_total = models.IntegerField(default=100)
    exam_weight = models.IntegerField(default=50)

    def __str__(self):
        return self.module_name

    def get_absolute_url(self):
        return reverse('module-details', kwargs={'pk': self.pk})


class Student(models.Model):
    student_ID = models.IntegerField(primary_key=True)
    student_forename = models.CharField(max_length=30)
    student_surname = models.CharField(max_length=30)

    def __str__(self):
        return "%s %s" % (self.student_forename, self.student_surname)

    def get_absolute_url(self):
        return reverse('student-details', kwargs={'pk': self.pk})


class StudentMark(models.Model):
    result_ID = models.AutoField(primary_key=True)
    module_code = models.ForeignKey(Module, on_delete=models.CASCADE)
    student_ID = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    checkpoints_complete = models.IntegerField(default=0)
    assignment_mark_results = ArrayField(models.IntegerField(default=0), default=defaultAssignmentMark)
    exam_mark_results = models.IntegerField(default=0)
    total_mark = models.IntegerField(default=0)
    grade = models.CharField(default='0', max_length=5)
    comment = models.TextField(default='', blank=True)

    def __str__(self):
        return "%s %s %s" % (self.module_code, self.student_ID, self.year)

    def get_absolute_url(self):
        return reverse('results-details', kwargs={'module_code': self.module_code.module_code, 'year': self.year, 'student_id': self.student_ID.student_ID, 'pk': self.result_ID})

    def calculate_mark(self):
        total_components = 0
        if self.module_code.checkpoint_weight > 0:
            total_components += 1
            weighted_checkpoint = (self.checkpoints_complete/self.module_code.number_of_checkpoints)*self.module_code.checkpoint_weight
        else:
            weighted_checkpoint = None
        if self.module_code.assignment_weight > 0:
            total_components += 1
            calculate_assignments = []
            for i in range(len(self.module_code.assignment_mark_total)):
                try:
                    print(self.module_code.assignment_mark_total[i])
                    print(self.assignment_mark_results[i])
                    calculate_assignments.append(self.assignment_mark_results[i]/self.module_code.assignment_mark_total[i])
                except IndexError:
                    calculate_assignments.append(0)
            weighted_assignment = (sum(calculate_assignments)/len(calculate_assignments))*self.module_code.assignment_weight
            print(weighted_assignment)
        else:
            weighted_assignment = None
        if self.module_code.exam_weight > 0:
            total_components += 1
            weighted_exam = (self.exam_mark_results/self.module_code.exam_mark_total)*self.module_code.exam_weight
        else:
            weighted_exam = None
        if total_components > 0:
            weighted_total = sum((filter(None, [weighted_checkpoint, weighted_assignment, weighted_exam])))
            return weighted_total
        else:
            return 0

    def calculate_grade(self):
        if self.total_mark >= 70:
            return "1"
        elif self.total_mark >= 60:
            return "2:1"
        elif self.total_mark >= 50:
            return "2:2"
        elif self.total_mark >= 40:
            return "3"
        else:
            return "F"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_mark = self.calculate_mark()
        self.grade = self.calculate_grade()
        super().save()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['module_code', 'student_ID', 'year'], name='unique_student_mark')]
