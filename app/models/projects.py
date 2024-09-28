from django.db import models
from .company import Company
from django.utils.timezone import now
from django.apps import apps
import os
from uuid import uuid4


def pitchdeck_image_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("pitchdeck_sections/", filename)


def elevator_pitch_videos_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("elevator_pitch_videos/", filename)


def how_it_works_videos_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("how_it_works_videos/", filename)


def business_plans_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("business_plans/", filename)


def financial_statements_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("financial_statements/", filename)


def other_documents_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("other_documents/", filename)


def project_images_file_path(instance, filename):
    ext = str(filename).split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    return os.path.join("project_images/", filename)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class PitchDeckSection(models.Model):
    project = models.ForeignKey('app.Project', on_delete=models.CASCADE, related_name='pitchdeck_sections', blank=True, null=True)
    # Problem section
    problem_name_ru = models.CharField(max_length=255, blank=True, null=True)
    problem_description_ru = models.TextField(blank=True, null=True)
    problem_name_en = models.CharField(max_length=255)  # English is required
    problem_description_en = models.TextField()
    problem_name_uz = models.CharField(max_length=255, blank=True, null=True)
    problem_description_uz = models.TextField(blank=True, null=True)
    problem_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Solution section
    solution_name_ru = models.CharField(max_length=255, blank=True, null=True)
    solution_description_ru = models.TextField(blank=True, null=True)
    solution_name_en = models.CharField(max_length=255)
    solution_description_en = models.TextField()
    solution_name_uz = models.CharField(max_length=255, blank=True, null=True)
    solution_description_uz = models.TextField(blank=True, null=True)
    solution_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Market Size section
    market_size_name_ru = models.CharField(max_length=255, blank=True, null=True)
    market_size_description_ru = models.TextField(blank=True, null=True)
    market_size_name_en = models.CharField(max_length=255)
    market_size_description_en = models.TextField()
    market_size_name_uz = models.CharField(max_length=255, blank=True, null=True)
    market_size_description_uz = models.TextField(blank=True, null=True)
    market_size_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Target Customer Market Validation section
    target_customer_name_ru = models.CharField(max_length=255, blank=True, null=True)
    target_customer_description_ru = models.TextField(blank=True, null=True)
    target_customer_name_en = models.CharField(max_length=255)
    target_customer_description_en = models.TextField()
    target_customer_name_uz = models.CharField(max_length=255, blank=True, null=True)
    target_customer_description_uz = models.TextField(blank=True, null=True)
    target_customer_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # How It Works section
    how_it_works_name_ru = models.CharField(max_length=255, blank=True, null=True)
    how_it_works_description_ru = models.TextField(blank=True, null=True)
    how_it_works_name_en = models.CharField(max_length=255)
    how_it_works_description_en = models.TextField()
    how_it_works_name_uz = models.CharField(max_length=255, blank=True, null=True)
    how_it_works_description_uz = models.TextField(blank=True, null=True)
    how_it_works_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Special Sauce (Why Us) section
    special_sauce_name_ru = models.CharField(max_length=255, blank=True, null=True)
    special_sauce_description_ru = models.TextField(blank=True, null=True)
    special_sauce_name_en = models.CharField(max_length=255)
    special_sauce_description_en = models.TextField()
    special_sauce_name_uz = models.CharField(max_length=255, blank=True, null=True)
    special_sauce_description_uz = models.TextField(blank=True, null=True)
    special_sauce_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Team section
    team_name_ru = models.CharField(max_length=255, blank=True, null=True)
    team_description_ru = models.TextField(blank=True, null=True)
    team_name_en = models.CharField(max_length=255)
    team_description_en = models.TextField()
    team_name_uz = models.CharField(max_length=255, blank=True, null=True)
    team_description_uz = models.TextField(blank=True, null=True)
    team_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Why Now section
    why_now_name_ru = models.CharField(max_length=255, blank=True, null=True)
    why_now_description_ru = models.TextField(blank=True, null=True)
    why_now_name_en = models.CharField(max_length=255)
    why_now_description_en = models.TextField()
    why_now_name_uz = models.CharField(max_length=255, blank=True, null=True)
    why_now_description_uz = models.TextField(blank=True, null=True)
    why_now_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Business Model section
    business_model_name_ru = models.CharField(max_length=255, blank=True, null=True)
    business_model_description_ru = models.TextField(blank=True, null=True)
    business_model_name_en = models.CharField(max_length=255)
    business_model_description_en = models.TextField()
    business_model_name_uz = models.CharField(max_length=255, blank=True, null=True)
    business_model_description_uz = models.TextField(blank=True, null=True)
    business_model_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Competitors section
    competitors_name_ru = models.CharField(max_length=255, blank=True, null=True)
    competitors_description_ru = models.TextField(blank=True, null=True)
    competitors_name_en = models.CharField(max_length=255)
    competitors_description_en = models.TextField()
    competitors_name_uz = models.CharField(max_length=255, blank=True, null=True)
    competitors_description_uz = models.TextField(blank=True, null=True)
    competitors_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Tractions section
    tractions_name_ru = models.CharField(max_length=255, blank=True, null=True)
    tractions_description_ru = models.TextField(blank=True, null=True)
    tractions_name_en = models.CharField(max_length=255)
    tractions_description_en = models.TextField()
    tractions_name_uz = models.CharField(max_length=255, blank=True, null=True)
    tractions_description_uz = models.TextField(blank=True, null=True)
    tractions_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Financial Acquisitions section
    financial_acquisitions_name_ru = models.CharField(max_length=255, blank=True, null=True)
    financial_acquisitions_description_ru = models.TextField(blank=True, null=True)
    financial_acquisitions_name_en = models.CharField(max_length=255)
    financial_acquisitions_description_en = models.TextField()
    financial_acquisitions_name_uz = models.CharField(max_length=255, blank=True, null=True)
    financial_acquisitions_description_uz = models.TextField(blank=True, null=True)
    financial_acquisitions_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    # Technology section
    technology_name_ru = models.CharField(max_length=255, blank=True, null=True)
    technology_description_ru = models.TextField(blank=True, null=True)
    technology_name_en = models.CharField(max_length=255)
    technology_description_en = models.TextField()
    technology_name_uz = models.CharField(max_length=255, blank=True, null=True)
    technology_description_uz = models.TextField(blank=True, null=True)
    technology_image = models.ImageField(upload_to=pitchdeck_image_file_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.problem_name_en


class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company")  # Assuming you'll create a Company model later
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    startup_name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)   
    district = models.CharField(max_length=100) 
    website_url = models.URLField(max_length=255)
    linkedin = models.URLField(max_length=255, default=True)

    project_image = models.ImageField(upload_to=project_images_file_path, blank=True, null=True)
    project_overview = models.TextField()
    elevator_pitch_video = models.FileField(upload_to=elevator_pitch_videos_file_path)    
    how_it_works_video = models.FileField(upload_to=how_it_works_videos_file_path)
    funding_goal = models.DecimalField(max_digits=20, decimal_places=2)
    equity = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    use_of_funds = models.TextField()

    business_plan = models.FileField(upload_to=business_plans_file_path)
    financial_statements = models.FileField(upload_to=financial_statements_file_path)
    other_documents = models.FileField(upload_to=other_documents_file_path)  
    time_limit = models.PositiveIntegerField(default=10)
    min_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.startup_name


class Founder(models.Model):
    project = models.ForeignKey(Project, related_name='founders', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    linkedin_profile = models.URLField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name