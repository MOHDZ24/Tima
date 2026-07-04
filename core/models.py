from django.db import models
from django.core.files.storage import default_storage


class SiteSettings(models.Model):
    """إعدادات الموقع العامة - Singleton pattern"""
    store_name = models.CharField('اسم المتجر', max_length=200, default='رواق المسلم')
    store_subtitle = models.CharField('وصف المتجر', max_length=300, default='متجر الملابس والكتب الإسلامية', blank=True)
    logo = models.ImageField('اللوقو', upload_to='site/', blank=True, null=True)
    favicon = models.ImageField('أيقونة المتصفح', upload_to='site/', blank=True, null=True)

    # الألوان
    primary_color = models.CharField('اللون الرئيسي', max_length=20, default='#1a5632')
    secondary_color = models.CharField('اللون الثانوي', max_length=20, default='#c8a951')
    accent_color = models.CharField('لون التمييز', max_length=20, default='#dc3545')

    # معلومات التواصل
    phone = models.CharField('رقم الهاتف', max_length=30, blank=True)
    email = models.EmailField('البريد الإلكتروني', blank=True)
    address = models.TextField('العنوان', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    tiktok = models.URLField('TikTok', blank=True)
    facebook = models.URLField('Facebook', blank=True)
    whatsapp = models.CharField('WhatsApp', max_length=30, blank=True)

    # نصوص
    hero_title = models.CharField('عنوان الرئيسية', max_length=200, default='رواق المسلم', blank=True)
    hero_subtitle = models.CharField('وصف الرئيسية', max_length=300, default='أفضل الملابس والكتب الإسلامية بجودة عالية', blank=True)
    hero_button_text = models.CharField('نص زر الرئيسية', max_length=50, default='تسوق الآن', blank=True)
    footer_text = models.CharField('نص الفوتر', max_length=300, default='جميع الحقوق محفوظة', blank=True)

    # الشحن
    free_shipping_min = models.DecimalField('الحد الأدنى للشحن المجاني', max_digits=10, decimal_places=2, default=5000)
    default_shipping_cost = models.DecimalField('تكلفة الشحن الافتراضية', max_digits=10, decimal_places=2, default=500)

    # إعدادات أخرى
    maintenance_mode = models.BooleanField('وضع الصيانة', default=False)
    show_special_offers = models.BooleanField('عرض العروض الخاصة', default=True)
    show_new_products = models.BooleanField('عرض المنتجات الجديدة', default=True)
    products_per_page = models.IntegerField('عدد المنتجات في الصفحة', default=20)
    whatsapp_float = models.BooleanField('زر WhatsApp عائم', default=True)

    updated_at = models.DateTimeField('آخر تحديث', auto_now=True)

    class Meta:
        verbose_name = 'إعدادات الموقع'
        verbose_name = 'إعدادات الموقع'

    def __str__(self):
        return f'إعدادات {self.store_name}'

    def save(self, *args, **kwargs):
        # Singleton: always use ID 1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def css_variables(self):
        return f"""
        :root {{
            --primary: {self.primary_color};
            --primary-dark: {self.darken_color(self.primary_color, 30)};
            --gold: {self.secondary_color};
            --gold-dark: {self.darken_color(self.secondary_color, 20)};
        }}
        """

    @staticmethod
    def darken_color(hex_color, percent):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * (100 - percent) / 100))
        g = max(0, int(g * (100 - percent) / 100))
        b = max(0, int(b * (100 - percent) / 100))
        return f'#{r:02x}{g:02x}{b:02x}'


class DeliveryPrice(models.Model):
    """أسعار التوصيل حسب الولاية"""
    wilaya = models.CharField('الولاية', max_length=100, unique=True)
    price = models.DecimalField('سعر التوصيل', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('نشط', default=True)
    estimated_days = models.IntegerField('أيام التوصيل المقدرة', default=3)

    class Meta:
        verbose_name = 'سعر توصيل'
        verbose_name = 'أسعار التوصيل'
        ordering = ['wilaya']

    def __str__(self):
        return f'{self.wilaya} - {self.price} د.ج'


class SliderImage(models.Model):
    """صور السلايدر في الرئيسية"""
    title = models.CharField('العنوان', max_length=200, blank=True)
    subtitle = models.CharField('الوصف', max_length=300, blank=True)
    image = models.ImageField('الصورة (ديسكتوب)', upload_to='slides/')
    mobile_image = models.ImageField('الصورة (موبايل)', upload_to='slides/phones/', blank=True, null=True)
    link = models.URLField('رابط', blank=True)
    button_text = models.CharField('نص الزر', max_length=50, blank=True, default='تسوق الآن')
    is_active = models.BooleanField('نشط', default=True)
    order = models.IntegerField('ترتيب العرض', default=0)

    class Meta:
        verbose_name = 'صورة سلايدر'
        verbose_name = 'صور السلايدر'
        ordering = ['order']

    def __str__(self):
        return self.title or f'سلايدر {self.pk}'
