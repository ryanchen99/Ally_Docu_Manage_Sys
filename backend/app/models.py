from django.db import models

# Create your models here.
class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


from django.db import models

class Docu_of_Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    armed_forces_id_card = models.BooleanField(default=False)
    birth_certificate = models.BooleanField(default=False)
    death_certificate_copy = models.BooleanField(default=False)
    death_notification_entry = models.BooleanField(default=False)
    divorce_decree = models.BooleanField(default=False)
    drivers_license = models.BooleanField(default=False)
    executor_documents = models.BooleanField(default=False)
    google_maps_usps_address_search = models.BooleanField(default=False)
    latest_best_data_provided_by_customer = models.BooleanField(default=False)
    legal_name_change_document = models.BooleanField(default=False)
    lexisnexis = models.BooleanField(default=False)
    lexisnexis_minor_spelling_corrections = models.BooleanField(default=False)
    marriage_certificate = models.BooleanField(default=False)
    medicare_card = models.BooleanField(default=False)
    notice_of_reclamation = models.BooleanField(default=False)
    obituary = models.BooleanField(default=False)
    original_death_certificate = models.BooleanField(default=False)
    permanent_resident_card = models.BooleanField(default=False)
    signed_social_security_card = models.BooleanField(default=False)
    signed_ssn_card_new_name = models.BooleanField(default=False)
    state_issued_id = models.BooleanField(default=False)
    us_military_card = models.BooleanField(default=False)
    us_passport_card = models.BooleanField(default=False)
    w_2 = models.BooleanField(default=False)
    w_9 = models.BooleanField(default=False)

    
class Driver_Licenses(models.Model):
    dl_id = models.AutoField(primary_key=True)
    license_number = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    sex = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    zip = models.CharField(max_length=100, default='')
    expired_date = models.DateField()
    issued_date = models.DateField()
    dob = models.DateField()
    license_class = models.CharField(max_length=100)
    image_url = models.ImageField(max_length=300)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)

class Divorce_Decrees(models.Model):
    dd_id = models.AutoField(primary_key=True)
    case_number = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    expired_date = models.DateField()
    issued_date = models.DateField()
    dob = models.DateField()
    image_url = models.ImageField(upload_to='images/')
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE)

