from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
import json

class AdminHierarchy(models.Model):
    """Model for storing administrative hierarchy data"""
    dept_code = models.IntegerField(help_text="Department code")
    appln_code = models.IntegerField(help_text="Application code")
    code = models.IntegerField(help_text="Administrative code")
    type = models.CharField(max_length=50, help_text="Administrative type")
    
    # Response fields
    district_name = models.CharField(max_length=200, blank=True, null=True)
    district_code = models.CharField(max_length=50, blank=True, null=True)
    taluk_name = models.CharField(max_length=200, blank=True, null=True)
    taluk_code = models.CharField(max_length=50, blank=True, null=True)
    hobli_name = models.CharField(max_length=200, blank=True, null=True)
    hobli_code = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=200, blank=True, null=True)
    village_code = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.district_name} - {self.taluk_name} - {self.hobli_name}"
    
    class Meta:
        verbose_name = "Administrative Hierarchy"
        verbose_name_plural = "Administrative Hierarchies"
        indexes = [
            models.Index(fields=['district_code']),
            models.Index(fields=['taluk_code']),
            models.Index(fields=['hobli_code']),
            models.Index(fields=['village_code']),
        ]

class District(models.Model):
    """Model for storing district information"""
    name = models.CharField(max_length=200, unique=True, help_text="District name")
    code = models.CharField(max_length=50, unique=True, help_text="District code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ['name']

class Taluk(models.Model):
    """Model for storing taluk information"""
    name = models.CharField(max_length=200, help_text="Taluk name")
    code = models.CharField(max_length=50, help_text="Taluk code")
    district = models.ForeignKey(
        District, 
        on_delete=models.CASCADE, 
        related_name='taluks',
        blank=True, 
        null=True
    )
    district_name = models.CharField(max_length=200, blank=True, null=True)
    district_code = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.district_name}"
    
    class Meta:
        verbose_name = "Taluk"
        verbose_name_plural = "Taluks"
        unique_together = ['name', 'district_code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['district_code']),
        ]

class Hobli(models.Model):
    """Model for storing hobli information"""
    name = models.CharField(max_length=200, help_text="Hobli name")
    code = models.CharField(max_length=50, help_text="Hobli code")
    taluk = models.ForeignKey(
        Taluk, 
        on_delete=models.CASCADE, 
        related_name='hoblis',
        blank=True, 
        null=True
    )
    district_name = models.CharField(max_length=200, blank=True, null=True)
    district_code = models.CharField(max_length=50, blank=True, null=True)
    taluk_name = models.CharField(max_length=200, blank=True, null=True)
    taluk_code = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.taluk_name}"
    
    class Meta:
        verbose_name = "Hobli"
        verbose_name_plural = "Hoblis"
        unique_together = ['name', 'taluk_code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['taluk_code']),
            models.Index(fields=['district_code']),
        ]

class LocationDetails(models.Model):
    """Model for storing location details based on coordinates"""
    TYPE_CHOICES = [
        ('point', 'Point'),
        ('polygon', 'Polygon'),
        ('line', 'Line'),
    ]
    
    coordinates = models.TextField(help_text="Coordinates string")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    aoi = models.CharField(max_length=200, blank=True, null=True, help_text="Area of Interest")
    
    # Location geometry
    location = models.GeometryField(srid=4326, blank=True, null=True)
    
    # Response fields
    message = models.TextField(blank=True, null=True)
    district_code = models.CharField(max_length=50, blank=True, null=True)
    district_name = models.CharField(max_length=200, blank=True, null=True)
    town_code = models.CharField(max_length=50, blank=True, null=True)
    town_name = models.CharField(max_length=200, blank=True, null=True)
    zone_code = models.CharField(max_length=50, blank=True, null=True)
    zone_name = models.CharField(max_length=200, blank=True, null=True)
    ward_code = models.CharField(max_length=50, blank=True, null=True)
    ward_name = models.CharField(max_length=200, blank=True, null=True)
    lgd_ward_code = models.CharField(max_length=50, blank=True, null=True)
    hobli_code = models.CharField(max_length=50, blank=True, null=True)
    hobli_name = models.CharField(max_length=200, blank=True, null=True)
    village_code = models.CharField(max_length=50, blank=True, null=True)
    village_name = models.CharField(max_length=200, blank=True, null=True)
    lgd_village_code = models.CharField(max_length=50, blank=True, null=True)
    taluk_code = models.CharField(max_length=50, blank=True, null=True)
    taluk_name = models.CharField(max_length=200, blank=True, null=True)
    survey_num = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Location: {self.district_name} - {self.taluk_name}"
    
    class Meta:
        verbose_name = "Location Detail"
        verbose_name_plural = "Location Details"
        indexes = [
            models.Index(fields=['district_code']),
            models.Index(fields=['taluk_code']),
            models.Index(fields=['hobli_code']),
            models.Index(fields=['village_code']),
        ]

class PinCodeDistance(models.Model):
    """Model for storing distance calculations between pin codes"""
    pincodes = models.CharField(max_length=200, help_text="Pin codes for distance calculation")
    key_msg = models.TextField(help_text="Key message from API")
    distance = models.CharField(max_length=100, blank=True, null=True, help_text="Distance between pin codes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Distance calculation: {self.pincodes}"
    
    class Meta:
        verbose_name = "Pin Code Distance"
        verbose_name_plural = "Pin Code Distances"

class NearbyHierarchy(models.Model):
    """Model for storing nearby administrative hierarchy data"""
    coordinates = models.TextField(help_text="Coordinates string")
    distance = models.CharField(max_length=50, help_text="Search distance")
    type = models.CharField(max_length=50, help_text="Search type")
    aoi = models.CharField(max_length=200, help_text="Area of Interest")
    
    # Location geometry
    location = models.PointField(srid=4326, blank=True, null=True)
    
    # Response fields
    district_name = models.CharField(max_length=200, help_text="District name")
    district_code = models.CharField(max_length=50, help_text="District code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Nearby: {self.district_name} ({self.distance})"
    
    class Meta:
        verbose_name = "Nearby Hierarchy"
        verbose_name_plural = "Nearby Hierarchies"
        indexes = [
            models.Index(fields=['district_code']),
        ]

class GeometricPolygon(models.Model):
    """Model for storing geometric polygon data for survey numbers"""
    COORD_TYPE_CHOICES = [
        ('utm', 'UTM'),
        ('geographic', 'Geographic'),
        ('projected', 'Projected'),
    ]
    
    village_id = models.IntegerField(help_text="Village ID")
    survey_no = models.IntegerField(help_text="Survey number")
    coord_type = models.CharField(max_length=20, choices=COORD_TYPE_CHOICES, help_text="Coordinate system type")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Survey {self.survey_no} - Village {self.village_id}"
    
    class Meta:
        verbose_name = "Geometric Polygon"
        verbose_name_plural = "Geometric Polygons"
        unique_together = ['village_id', 'survey_no', 'coord_type']
        indexes = [
            models.Index(fields=['village_id']),
            models.Index(fields=['survey_no']),
        ]

class PolygonGeometry(models.Model):
    """Model for storing individual polygon geometries"""
    geometric_polygon = models.ForeignKey(
        GeometricPolygon,
        on_delete=models.CASCADE,
        related_name='polygons'
    )
    message = models.TextField(help_text="Polygon message or description")
    geometry_data = models.TextField(help_text="Geometry data as text")
    geometry = models.GeometryField(srid=4326, blank=True, null=True, help_text="Actual geometry field")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Polygon for {self.geometric_polygon}"
    
    class Meta:
        verbose_name = "Polygon Geometry"
        verbose_name_plural = "Polygon Geometries"

# Abstract model for common API request logging
class APIRequest(models.Model):
    """Abstract model for logging API requests"""
    endpoint = models.CharField(max_length=100, help_text="API endpoint called")
    request_data = models.JSONField(default=dict, help_text="Request payload")
    response_data = models.JSONField(default=dict, help_text="Response data")
    status_code = models.IntegerField(default=200, help_text="HTTP status code")
    execution_time = models.FloatField(blank=True, null=True, help_text="Execution time in seconds")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

class KGISAPILog(APIRequest):
    """Model for logging KGIS API calls"""
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.endpoint} - {self.created_at}"
    
    class Meta:
        verbose_name = "KGIS API Log"
        verbose_name_plural = "KGIS API Logs"
        indexes = [
            models.Index(fields=['endpoint']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status_code']),
        ]