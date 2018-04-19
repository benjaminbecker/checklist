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
    def get_all_items(self):
        return ChecklistItem.objects.filter(checklist=self.id)
    def copy_items_to_list(self,list_id):
        source_items = self.get_all_items()
        destination = Checklist.objects.get(id=list_id)
        for this_item in source_items:
            item_name = this_item.name
            new_item = ChecklistItem(checklist=destination, name=item_name, done=False)
            new_item.save()
    #def remove_dublettes(self):
        # todo: implement
    def __str__(self):
        return self.name
    
class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
