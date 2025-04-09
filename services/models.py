from django.db import models
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

    def _str_(self):
        return f"{self.name}"

class Services(models.Model):
    TIME_SLOT_OPTIONS = (
        ('8:00am-10:00am', '8:00am-10:00am'),
        ('10:00am-12:00pm', '10:00am-12:00pm'),
        ('12:00pm-2:00pm', '12:00pm-2:00pm'),
        ('2:00pm-4:00pm', '2:00pm-4:00pm'),
        ('4:00pm-6:00pm', '4:00pm-6:00pm'),
        ('6:00pm-8:00pm', '6:00pm-8:00pm'),
    )

    SERVICE_DURATION_OPTIONS = (
        ('30min', '30min'),
        ('1hr', '1hr'),
        ('1hr 30min', '1hr 30min'),
        ('2hr', '2hr'),
        ('3hr', '3hr'),
    )
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name='description')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='price', default=5.00)
    duration = models.CharField(max_length=20, choices=SERVICE_DURATION_OPTIONS, default='30min')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    time_slot = models.CharField(max_length=20, choices=TIME_SLOT_OPTIONS, default='8:00am-10:00am')
    image = models.ImageField(upload_to='services', default='services/default.jpg')

    class Meta:
        verbose_name='Service'
        verbose_name_plural='Services'

    def delete(self):
        self.image.delete()
        super().delete()

    def _str_(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'service_id': self.pk})
    
    def formatted_price(self):
        return f"${self.price:.2f}"
    
    def available_time_slots(self):
        return self.time_slot.replace("-", " to ")
    
    def category_name(self):
        return self.category.name
    
    def short_description(self):
        if self.description and len(self.description) > 50:
            return self.description[:50] + "..."
        return self.description