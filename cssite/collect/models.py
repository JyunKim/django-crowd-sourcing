from django import forms
from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class Account(models.Model):
    GENDER_CHOICES = [
        ('남성', '남성'),
        ('여성', '여성'),
    ]
    
    ROLE_CHOICES = [
        ('제출자', '제출자'),
        ('평가자', '평가자'),
        ('관리자', '관리자'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('이름', max_length=20)
    contact = models.CharField('연락처', max_length=20)
    birth = models.DateField('생년월일', null=True, blank=True)
    gender = models.CharField('성별', max_length=5, choices=GENDER_CHOICES)
    address = models.CharField('주소', max_length=100)
    role = models.CharField('역할', max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role
    

class Task(models.Model):
    name = models.CharField('태스크 이름', max_length=45, unique=True)
    minimal_upload_frequency = models.CharField('최소 업로드 주기', max_length=45)
    activation_state = models.BooleanField('활성화 상태', default=True)
    description = models.CharField('태스크 설명', max_length=100)
    original_data_description = models.CharField('원본 데이터 설명', max_length=100)

    def __str__(self):
        return self.name


class Participation(models.Model):
    class Meta:
        unique_together = (('account', 'task'),)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='participations', verbose_name='제출자')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='participations', verbose_name='태스크')
    admission = models.BooleanField('승인 상태', default=False)
    submit_count = models.IntegerField('제출 횟수', default=0)


def grading_score_validator(value):
    if value < 0 or value > 10:
        raise forms.ValidationError('0 ~ 10 사이의 숫자를 입력해주세요.')


class ParsedFile(models.Model):
    submitter = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='parsed_submits', verbose_name='제출자')
    grader = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='parsed_grades', verbose_name='평가자', null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='parsedfiles', verbose_name='태스크')
    directory = models.CharField('파일 경로', max_length=200)
    submit_number = models.IntegerField('제출 회차')
    start_date = models.DateField('시작 날짜')
    end_date = models.DateField('종료 날짜')
    total_tuple = models.IntegerField('전체 튜플 수')
    duplicated_tuple = models.IntegerField('중복 튜플 수')
    null_ratio = models.FloatField('null 비율')
    grading_score = models.IntegerField('평가 점수', null=True, blank=True, validators=[grading_score_validator])
    pass_state = models.BooleanField('패스 여부', null=True, blank=True)
    grading_end_date = models.DateField('평가 종료 날짜')
    grade_date = models.DateField('평가 날짜', auto_now=True)

    def __str__(self):
        return self.directory


class MappingInfo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='mapping_infos', verbose_name='태스크')
    orginal_schema_name = models.CharField('원본 스키마 이름', max_length=45)
    orginal_column_name = models.CharField('원본 스키마 속성 레이블', max_length=45)
    parsing_column_name = models.CharField('파싱 스키마 속성 레이블', max_length=45)

    def __str__(self):
        return self.orginal_schema_name
