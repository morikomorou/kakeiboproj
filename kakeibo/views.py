from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Kakeibo, Category
from datetime import datetime
from django.db.models import Sum, Count

# Create your views here.
@login_required
def month_listfunc(request, year=datetime.now().year, month=datetime.now().month):
    model = Kakeibo
    user = request.user
    month_list = model.objects.get_month(user=user)
    object_list = model.objects.month_filter(user=user, date__year=year, date__month=month)
    sum_dict =  model.objects.sum_all(user=user, date__year=year, date__month=month)
    total_dict =  model.objects.sum_in_out(user=user, date__year=year, date__month=month)
    return render(request, 'month_list.html', {'object_list':object_list,
                                                'year':year,
                                                'month':month,
                                                'month_list':month_list,
                                                'total_dict':total_dict,
                                                'sum_dict':sum_dict,
                                                })


@login_required
def month_choicefunc(request):
    if request.method == 'POST':
        if 'month' not in request.POST.keys():
            return redirect('list')
        else:
            month_choice = datetime.strptime(request.POST['month'], '%Y/%m')
            return redirect('month_list', year=month_choice.year, month=month_choice.month)
    return redirect('list')


@method_decorator(login_required, name='dispatch')
class KakeiboCreateIn(CreateView):
    template_name = 'create_in.html'
    model = Kakeibo
    fields = ('date', 'category', 'money', 'memo')

    def get_success_url(self):
        return reverse_lazy('month_list', kwargs={'year': self.object.date.year,
                                                    'month': self.object.date.month})

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput(format='%Y-%m-%d')
        form.fields['category'].queryset = Category.objects.filter(category_type='in')
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
        return form

    def form_valid(self, form):
        form.instance.in_out = 'in'
        form.instance.user = self.request.user
        messages.success(self.request, '登録内容を保存しました。')
        return super(KakeiboCreateIn, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class KakeiboCreateOut(CreateView):
    template_name = 'create_out.html'
    model = Kakeibo
    fields = ('date', 'category', 'money', 'memo')

    def get_success_url(self):
        return reverse_lazy('month_list', kwargs={'year': self.object.date.year,
                                                    'month': self.object.date.month})

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput(format='%Y-%m-%d')
        form.fields['category'].queryset = Category.objects.filter(category_type='out')
        for field in form.fields.values():
            field.widget.attrs["class"] = "form-control"
        return form

    def form_valid(self, form):
        form.instance.in_out = 'out'
        form.instance.user = self.request.user
        messages.success(self.request, '登録内容を保存しました。')
        return super(KakeiboCreateOut, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class KakeiboUpdate(UpdateView):
    template_name = 'update.html'
    model = Kakeibo
    fields = ('date', 'category', 'money', 'memo')

    def get_success_url(self):
        return reverse_lazy('month_list', kwargs={'year': self.object.date.year,
                                                    'month': self.object.date.month})

    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput(format='%Y-%m-%d')
        if self.object.in_out == 'in':
            form.fields['category'].queryset = Category.objects.filter(category_type='in')
        elif self.object.in_out == 'out':
            form.fields['category'].queryset = Category.objects.filter(category_type='out')
        else:
            pass
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.object.in_out == 'in':
            form.instance.in_out = 'in'
        elif self.object.in_out == 'out':
            form.instance.in_out = 'out'
        else:
            pass
        messages.success(self.request, '登録内容を保存しました。')
        return super(KakeiboUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class KakeiboDelete(DeleteView):
    template_name = 'delete.html'
    model = Kakeibo
    success_url = reverse_lazy('list')


@login_required
def logoutfunc(request):
    logout(request)
    return redirect('login')


@login_required
def historyfunc(request):
    model = Kakeibo
    user = request.user
    month_list = model.objects.get_month_list(user=user)
    sum_dict =  model.objects.sum_month(month_list, user=user)
    total = model.objects.sum_month_total(month_list, user=user)
    return render(request, 'history.html', {'month_list':month_list,
                                            'sum_dict':sum_dict,
                                            'total':total,
                                            })