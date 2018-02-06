from django.db import models

# Create your models here.
class Checklist(models.Model):
    name = models.CharField(max_length=40)
    date_of_creation = models.DateTimeField('date of creation')
    # date_of_obsolescence = models.DateTimeField('date of obsolescence')
    def no_of_items(self):
        items = ChecklistItem.objects.filter(checklist=self.id)
        return len(items)
    def no_of_items_done(self):
        items = ChecklistItem.objects.filter(checklist=self.id,done=True)
        return len(items)
    def no_of_items_not_done(self):
        items = ChecklistItem.objects.filter(checklist=self.id,done=False)
        return len(items)
    def __str__(self):
        return self.name
    
class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
