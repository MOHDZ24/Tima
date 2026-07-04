from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('اسم الفئة', max_length=200)
    slug = models.SlugField('الرابط', unique=True, allow_unicode=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children', verbose_name='الفئة الأب'
    )
    icon = models.CharField('أيقونة Font Awesome', max_length=100, blank=True,
                            help_text='مثال: fas fa-book')
    is_active = models.BooleanField('نشط', default=True)
    order = models.IntegerField('ترتيب العرض', default=0)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)

    class Meta:
        verbose_name = 'فئة'
        verbose_name = 'فئات'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/category/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products', verbose_name='الفئة'
    )
    name = models.CharField('اسم المنتج', max_length=300)
    slug = models.SlugField('الرابط', unique=True, allow_unicode=True)
    description = models.TextField('الوصف', blank=True)
    price = models.DecimalField('السعر', max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        'السعر القديم', max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    image = models.ImageField('الصورة الرئيسية', upload_to='products/main/')
    image_2 = models.ImageField(
        'صورة ثانية', upload_to='products/extra/',
        null=True, blank=True
    )
    image_3 = models.ImageField(
        'صورة ثالثة', upload_to='products/extra/',
        null=True, blank=True
    )
    is_new = models.BooleanField('جديد', default=True)
    is_on_sale = models.BooleanField('عرض خاص', default=False)
    is_active = models.BooleanField('نشط', default=True)
    stock = models.IntegerField('المخزون', default=0)
    views_count = models.IntegerField('عدد المشاهدات', default=0)
    order = models.IntegerField('ترتيب العرض', default=0)
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)

    class Meta:
        verbose_name = 'منتج'
        verbose_name = 'منتجات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if self.old_price and self.old_price > self.price:
            self.is_on_sale = True
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/product/{self.pk}/'

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def savings(self):
        if self.old_price and self.old_price > self.price:
            return self.old_price - self.price
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images', verbose_name='المنتج'
    )
    image = models.ImageField('الصورة', upload_to='products/gallery/')
    alt_text = models.CharField('نص بديل', max_length=200, blank=True)
    order = models.IntegerField('ترتيب', default=0)

    class Meta:
        verbose_name = 'صورة منتج'
        verbose_name = 'صور المنتجات'
        ordering = ['order']

    def __str__(self):
        return f'{self.product.name} - صورة {self.order}'
