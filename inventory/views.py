from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm, InventoryItemsForm
from .models import InventoryItems, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name = 'inventory/index.html'


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch all items for the logged-in user
        items = InventoryItems.objects.filter(user=self.request.user.id).order_by('id')

        # Fetch low inventory items
        low_inventory = InventoryItems.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        )

        # Display a message if there are low inventory items
        if low_inventory.exists():
            count = low_inventory.count()
            item_word = "items" if count > 1 else "item"
            messages.error(request, f'{count} {item_word} have low inventory')

        # Get IDs of low inventory items
        low_inventory_ids = low_inventory.values_list('id', flat=True)

        # Render the dashboard template
        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids
        })
    
class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )

            login(request, user)
            return redirect ('index')
        
        
        
        return render(request, 'inventory/signup.html', {'form': form})


class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItems
    form_class = InventoryItemsForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItems
    form_class= InventoryItemsForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItems
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'