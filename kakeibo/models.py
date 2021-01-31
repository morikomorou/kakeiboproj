from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name ="カテゴリ"
        verbose_name_plural ="カテゴリ"
    
    choice = (('in', '収入'), ('out', '支出'))
    category_name = models.CharField(max_length=255, unique=True)
    category_type = models.CharField(max_length=3, choices=choice, verbose_name="収支")

    def __str__(self):
       return self.category_name


class KakeiboManager(models.Manager):
    
    def get_month(self):
        return self.get_queryset().dates('date', 'month', order='DESC')
    
    def month_filter(self, **kwargs):
        return self.filter(**kwargs).order_by('-date')
    
    def sum_all(self):
        return self.aggregate(Sum('money'))


class KakeiboQuerySet(models.QuerySet):
    def get_month(self, **kwargs):
        return self.filter(**kwargs).dates('date', 'month', order='DESC')
    
    def get_month_list(self, **kwargs):
        month_list = []
        results = self.filter(**kwargs).dates('date', 'month', order='ASC')
        for result in results:
            month_list.append(result.strftime('%Y-%m'))
        return month_list
    
    def month_filter(self, **kwargs):
        return self.filter(**kwargs).select_related('category').order_by('-date')
    
    def sum_all(self, **kwargs):
        category_in_list = []
        category_out_list = []
        sum_dict = {}
        sum_dict['in'] = {}
        sum_dict['out'] = {}
        category_data = Category.objects.all()
        for item in category_data:
            if item.category_type == 'in':
                category_in_list.append(item.category_name)
                sum_dict['in'][item.category_name] = 0
            elif item.category_type == 'out':
                category_out_list.append(item.category_name)
                sum_dict['out'][item.category_name] = 0

        results = self.filter(**kwargs).select_related('category').values('category', 'category__category_name', 'category__category_type').annotate(total_price=Sum('money'))
        for result in results:
            if result['category__category_type'] == 'in':
                sum_dict['in'][result['category__category_name']] = result['total_price']
            elif result['category__category_type'] == 'out':
                sum_dict['out'][result['category__category_name']] = result['total_price']
            else:
                pass
        return sum_dict
    
    def sum_in_out(self, **kwargs):
        total_dict = {}
        total_dict['in'] = 0
        total_dict['out'] = 0
        results = self.filter(**kwargs).select_related('category').values('category__category_type').annotate(total_price=Sum('money'))
        for result in results:
            if result['category__category_type'] == 'in':
                total_dict['in'] = result['total_price']
            elif result['category__category_type'] == 'out':
                total_dict['out'] = result['total_price']
            else:
                pass
        total_dict['total'] = total_dict['in'] - total_dict['out']
        return total_dict
    
    def sum_month(self, month_list, **kwargs):
        month_dict = {}
        for i, month in enumerate(month_list):
            month_dict[month] = i
        category_in_list = []
        category_out_list = []
        sum_dict = {}
        sum_dict['in'] = {}
        sum_dict['out'] = {}
        category_data = Category.objects.all()
        for item in category_data:
            if item.category_type == 'in':
                category_in_list.append(item.category_name)
                sum_dict['in'][item.category_name] = [0 for i in month_list]
            elif item.category_type == 'out':
                category_out_list.append(item.category_name)
                sum_dict['out'][item.category_name] = [0 for i in month_list]

        results = self.filter(**kwargs).values('date__year', 'date__month', 'category__category_name', 'category__category_type').annotate(total_price=Sum('money'))
        for result in results:
            result_month_dt = datetime(result['date__year'], result['date__month'], 1)
            result_month = result_month_dt.strftime('%Y-%m')
            if result['category__category_type'] == 'in':
                sum_dict['in'][result['category__category_name']][month_dict[result_month]] = result['total_price']
            elif result['category__category_type'] == 'out':
                sum_dict['out'][result['category__category_name']][month_dict[result_month]] = result['total_price']
            else:
                pass
        return sum_dict

    def sum_month_total(self, month_list, **kwargs):
        month_dict = {}
        for i, month in enumerate(month_list):
            month_dict[month] = i
        total_dict = {}
        total_dict['in'] = [0 for i in month_list]
        total_dict['out'] = [0 for i in month_list]
        results = self.filter(**kwargs).values('date__year', 'date__month', 'category__category_type').annotate(total_price=Sum('money'))
        for result in results:
            result_month_dt = datetime(result['date__year'], result['date__month'], 1)
            result_month = result_month_dt.strftime('%Y-%m')
            if result['category__category_type'] == 'in':
                total_dict['in'][month_dict[result_month]] = result['total_price']
            elif result['category__category_type'] == 'out':
                total_dict['out'][month_dict[result_month]] = result['total_price']
            else:
                pass
        total = [0 for i in month_list]
        for i in range(len(month_list)):
            total[i] = total_dict['in'][i] - total_dict['out'][i]
        return total


class Kakeibo(models.Model):
    class Meta:
        db_table = "kakeibo"
        verbose_name ="家計簿"
        verbose_name_plural ="家計簿"
    
    choice = (('in', '収入'), ('out', '支出'))
    date = models.DateField(verbose_name="日付", default=datetime.now)
    category = models.ForeignKey(Category, 
                on_delete=models.PROTECT, verbose_name="カテゴリ")
    in_out = models.CharField(max_length=3, choices=choice, verbose_name="収支")
    money = models.IntegerField(verbose_name="金額", help_text="単位は日本円")
    memo = models.CharField(verbose_name="詳細", max_length=500)
    objects = KakeiboQuerySet.as_manager()
    user = models.ForeignKey(User, 
                on_delete=models.PROTECT, verbose_name="ユーザー")

    def __str__(self):
       return self.memo