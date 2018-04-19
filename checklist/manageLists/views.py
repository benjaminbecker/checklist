from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Checklist, ChecklistItem
from django.urls import reverse


def index(request):
    list_of_latest_lists = Checklist.objects.order_by('-date_of_creation')[:5]
    context = {'list_of_latest_lists': list_of_latest_lists}
    return render(request, 'manageLists/index.html', context)
    

def show_list_by_name(request, list_name):
    checklist = get_object_or_404(Checklist, name=list_name)
    return render(request, 'manageLists/show_list.html', {'checklist': checklist, 'editMode':False})
    

def show_list(request, list_id):
    checklist = get_object_or_404(Checklist, pk=list_id)
    return render(request, 'manageLists/show_list.html',
        {'checklist': checklist, 'editMode':False})
    
    
def edit_list(request, list_id, item_id=-1):
    checklist = get_object_or_404(Checklist, pk=list_id)
    return render(request, 'manageLists/show_list.html', 
        {'checklist': checklist, 'editMode':True, 'editItemNo':item_id})
    
    
def submit_changes(request, list_id):
    selected_keys = request.POST.keys()
    
    # delete button:
    idDel = map(lambda x: 'deleteItemButton' in x,selected_keys)
    idEditItem = map(lambda x: 'editItemButton' in x,selected_keys)
    if max(idDel):
        for key in list(selected_keys):
            if 'deleteItemButton' in key:
                delete_ID = int(str(key).replace('deleteItemButton ',''))
                this_item = ChecklistItem.objects.get(id=delete_ID)
                this_item.delete()
                return HttpResponseRedirect(reverse('manageLists:edit', args=(list_id,)))
    
    # editItem button:
    elif max(idEditItem):
        for key in list(selected_keys):
            if 'editItemButton' in key:
                edit_ID = int(str(key).replace('editItemButton ',''))
                return HttpResponseRedirect(reverse('manageLists:edit_item', args=(list_id,edit_ID)))
    
    # edit button
    elif "editButton" in selected_keys:
        return HttpResponseRedirect(reverse('manageLists:edit', args=(list_id,)))
        
    # edit button if in edit mode
    elif "uneditButton" in selected_keys:
        return HttpResponseRedirect(reverse('manageLists:lists', args=(list_id,)))
    
    # submit button
    elif "submitButton" in selected_keys:
        items = ChecklistItem.objects.filter(checklist=list_id)
        item_ids = (it.id for it in items)
        for key_of_item in item_ids:
            this_item = ChecklistItem.objects.get(id=key_of_item)
            if str(key_of_item) in selected_keys:
                this_item.done = True
            else:
                this_item.done = False
            this_item.save()
        return HttpResponseRedirect(reverse('manageLists:lists', args=(list_id,)))
    else:
        return HttpResponse("Unimplemented Button: "+str(request.POST.keys()))
    
    
def add_item(request, list_id):
    # add new item
    # todo: check for errors
    thisList = Checklist.objects.get(id=list_id)
    items = request.POST['new_item_name']
    items = items.split('&')
    items = [this_item.strip() for this_item in items]
    for item_name in items:
        if len(item_name):
            # add another list if item_name starts with '/'
            if item_name[0]=='/':
                try:
                    source_list = Checklist.objects.get(name=item_name[1:])
                # if list does not exist add new item with /
                except Checklist.DoesNotExist:
                    new_item = ChecklistItem(checklist=thisList, name=item_name, done=False)
                    new_item.save()
                else:
                    source_list.copy_items_to_list(list_id)
            # else add item
            else:
                new_item = ChecklistItem(checklist=thisList, name=item_name, done=False)
                new_item.save()
    # redirect to updated list
    return HttpResponseRedirect(reverse('manageLists:lists', args=(list_id,)))
    
