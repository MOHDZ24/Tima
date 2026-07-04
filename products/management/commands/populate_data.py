"""
Management command to populate the database with products from رواق المسلم.
Usage: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Category, Product
import urllib.request
import tempfile
import os


class Command(BaseCommand):
    help = 'Populate database with sample products from رواق المسلم'

    def handle(self, *args, **options):
        self.stdout.write('🕌 جاري إنشاء البيانات...')
        self.create_categories()
        self.create_products()
        self.stdout.write(self.style.SUCCESS('✅ تم إنشاء البيانات بنجاح!'))

    def create_categories(self):
        # Main categories
        books, _ = Category.objects.get_or_create(
            slug='books',
            defaults={'name': 'الكتب', 'icon': 'fas fa-book', 'order': 1}
        )
        bundles, _ = Category.objects.get_or_create(
            slug='bundles',
            defaults={'name': 'باقات متنوعة', 'icon': 'fas fa-gift', 'order': 2}
        )
        clothing, _ = Category.objects.get_or_create(
            slug='clothing-accessories',
            defaults={'name': 'ملابس واكسسوارات', 'icon': 'fas fa-tshirt', 'order': 3}
        )
        tools, _ = Category.objects.get_or_create(
            slug='muslim-tools',
            defaults={'name': 'وسائل المسلم', 'icon': 'fas fa-mosque', 'order': 4}
        )

        # Subcategories for Books
        subcategories_books = [
            ('quran', 'القرآن : علومه وتفسيره', 'fas fa-quran'),
            ('hadith', 'كتب الحديث والسنة', 'fas fa-scroll'),
            ('seerah', 'كتب السيرة النبوية', 'fas fa-book-open'),
            ('aqeedah', 'كتب العقيدة والتوحيد', 'fas fa-star-and-crescent'),
            ('fiqh', 'كتب الفقه واصوله', 'fas fa-balance-scale'),
            ('women-books', 'كتب المرأة المسلمة 🎀', 'fas fa-female'),
        ]
        for slug, name, icon in subcategories_books:
            Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon, 'parent': books, 'order': subcategories_books.index((slug, name, icon))}
            )

        # Subcategories for Clothing
        subcategories_clothing = [
            ('accessories', 'اكسسوارات', 'fas fa-glasses'),
            ('clothes', 'الملابس', 'fas fa-tshirt'),
        ]
        for slug, name, icon in subcategories_clothing:
            Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'icon': icon, 'parent': clothing}
            )

        self.stdout.write('  ✓ الفئات')

    def create_products(self):
        products_data = [
            {
                'name': 'تيشرت موحد',
                'slug': 'tshirt-muwahhad',
                'description': 'تيشرت موحد بجودة عالية، مناسب للاستخدام اليومي. متوفر بعدة ألوان ومقاسات.',
                'price': 2300,
                'old_price': 3500,
                'is_new': True,
                'is_on_sale': True,
                'stock': 50,
                'category_slug': 'clothes',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_5943.jpeg',
            },
            {
                'name': 'البداية والنهاية -ابن كثير-',
                'slug': 'bidaya-wa-nihaya',
                'description': 'كتاب البداية والنهاية للإمام ابن كثير. من أعظم كتب التاريخ الإسلامي. طباعة ممتازة.',
                'price': 12000,
                'old_price': 20000,
                'is_new': True,
                'is_on_sale': True,
                'stock': 20,
                'category_slug': 'seerah',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_4861.jpeg',
            },
            {
                'name': 'الداء والدواء',
                'slug': 'al-da-wa-al-dawa',
                'description': 'كتاب الداء والدواء لابن القيم. كتاب نفيس في علاج الأمراض الروحية والنفسية.',
                'price': 1200,
                'is_new': True,
                'stock': 30,
                'category_slug': 'aqeedah',
                'image_url': 'https://riwaqi.com/media/products/main/copy_C1F1A2DE-9CAF-49FB-8565-F578BFEC60D6.jpeg',
            },
            {
                'name': 'كتاب التوحيد',
                'slug': 'kitab-al-tawhid',
                'description': 'كتاب التوحيد للإمام محمد بن عبد الوهاب. كتاب أساسي في العقيدة الإسلامية.',
                'price': 1900,
                'is_new': True,
                'stock': 40,
                'category_slug': 'aqeedah',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_5239.jpeg',
            },
            {
                'name': 'متون طالب العلم',
                'slug': 'mutun-talib-al-ilm',
                'description': 'مجموعة متون طالب العلم. تشمل أهم المتون في مختلف العلوم الشرعية.',
                'price': 1750,
                'old_price': 2500,
                'is_new': True,
                'is_on_sale': True,
                'stock': 35,
                'category_slug': 'books',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_3066.webp',
            },
            {
                'name': 'صحيح البخاري',
                'slug': 'sahih-al-bukhari',
                'description': 'صحيح الإمام البخاري. أصح كتاب بعد كتاب الله. طباعة ممتازة مع شرح ميسر.',
                'price': 2500,
                'is_new': True,
                'stock': 25,
                'category_slug': 'hadith',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_1853.webp',
            },
            {
                'name': 'الرحيق المختوم -السيرة النبوية-',
                'slug': 'al-raheeq-al-makhtum',
                'description': 'الرحيق المختوم. كتاب مميز في السيرة النبوية الشريفة. حائز على جائزة ملك فيصل.',
                'price': 1600,
                'is_new': True,
                'stock': 30,
                'category_slug': 'seerah',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_1857.webp',
            },
            {
                'name': 'شرح الأربعين النووية',
                'slug': 'sharh-arbaeen-al-nawawiya',
                'description': 'شرح الأربعين النووية. أربعون حديثاً نبوياً شريفاً مع شرح ميسر.',
                'price': 900,
                'is_new': True,
                'stock': 45,
                'category_slug': 'hadith',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_1859.webp',
            },
            {
                'name': 'تفسير السعدي',
                'slug': 'tafsir-al-saadi',
                'description': 'تفسير السعدي. تفسير ميسر للقرآن الكريم. من أفضل كتب التفسير المبسط.',
                'price': 2500,
                'is_new': True,
                'stock': 20,
                'category_slug': 'quran',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_1649.webp',
            },
            {
                'name': 'حزمة رواقي الخاصة',
                'slug': 'riwaqi-special-bundle',
                'description': 'حزمة رواقي الخاصة تشمل مجموعة مختارة من الكتب والمنتجات بسعر مميز.',
                'price': 1900,
                'is_new': True,
                'is_on_sale': True,
                'stock': 15,
                'category_slug': 'bundles',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_5261.jpeg',
            },
            {
                'name': 'كحل الاثمد الاصفهاني الاصلي',
                'slug': 'kohl-isfahani',
                'description': 'كحل الاثمد الاصفهاني الاصلي. كحل طبيعي أصلي من إيران. مفيد للعينين.',
                'price': 1200,
                'is_new': True,
                'stock': 40,
                'category_slug': 'accessories',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_9499.webp',
            },
            {
                'name': 'الجامع لاحكام المرأة المسلمة',
                'slug': 'jami-ahkam-al-mara',
                'description': 'الجامع لاحكام المرأة المسلمة. مرجع شامل في أحكام المرأة في الإسلام.',
                'price': 1200,
                'is_new': True,
                'stock': 25,
                'category_slug': 'women-books',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_9703.webp',
            },
            {
                'name': 'رياض الصالحين',
                'slug': 'riyad-al-salihin',
                'description': 'رياض الصالحين للإمام النووي. من أشهر كتب الحديث وأكثرها انتشاراً.',
                'price': 1500,
                'is_new': True,
                'stock': 30,
                'category_slug': 'hadith',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_5335.jpeg',
            },
            {
                'name': 'كتاب الطب النبوي',
                'slug': 'al-tibb-al-nabawi',
                'description': 'كتاب الطب النبوي لابن القيم. كتاب شامل في الطب النبوي والأعشاب.',
                'price': 1200,
                'is_new': True,
                'stock': 35,
                'category_slug': 'books',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0200.webp',
            },
            {
                'name': 'حزمة الطب النبوي',
                'slug': 'tibb-bundle',
                'description': 'حزمة الطب النبوي تشمل مجموعة من الكتب المتعلقة بالطب النبوي.',
                'price': 2500,
                'is_new': True,
                'stock': 15,
                'category_slug': 'bundles',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0199.webp',
            },
            {
                'name': 'Ensemble موحد',
                'slug': 'ensemble-muwahhad',
                'description': 'طقم موحد كامل (تيشرت + بنطلون). جودة عالية وتصميم أنيق.',
                'price': 3900,
                'old_price': 5700,
                'is_new': True,
                'is_on_sale': True,
                'stock': 20,
                'category_slug': 'clothes',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_3665.webp',
            },
            {
                'name': 'نظارات شمسية',
                'slug': 'sunglasses',
                'description': 'نظارات شمسية أنيقة. حماية من الأشعة فوق البنفسجية.',
                'price': 1700,
                'is_new': True,
                'stock': 30,
                'category_slug': 'accessories',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0851.webp',
            },
            {
                'name': 'صفة صلاة النبي من التكبير الى التسليم',
                'slug': 'sifat-salat-al-nabi',
                'description': 'صفة صلاة النبي ﷺ من التكبير إلى التسليم. كتاب مصور يشرح كيفية الصلاة.',
                'price': 950,
                'is_new': True,
                'stock': 40,
                'category_slug': 'fiqh',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_9283.webp',
            },
            {
                'name': 'شرح الدروس المهمة لعامة الامة',
                'slug': 'sharh-durus-muhimma',
                'description': 'شرح الدروس المهمة لعامة الامة. كتاب مبسط في أصول الدين وعقيدة المسلم.',
                'price': 950,
                'is_new': True,
                'stock': 35,
                'category_slug': 'aqeedah',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0202.webp',
            },
            {
                'name': 'ضمان ممتد',
                'slug': 'extended-warranty',
                'description': 'خدمة ضمان ممتد لجميع المنتجات. حماية إضافية لمشترياتك.',
                'price': 500,
                'is_new': True,
                'stock': 100,
                'category_slug': 'muslim-tools',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0775.webp',
            },
            {
                'name': 'شحن سريع',
                'slug': 'fast-shipping',
                'description': 'خدمة شحن سريع. وصول الطلب في أقل وقت ممكن.',
                'price': 300,
                'is_new': True,
                'stock': 100,
                'category_slug': 'muslim-tools',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0851.webp',
            },
            {
                'name': 'مساعد رواقي',
                'slug': 'riwaqi-helper',
                'description': 'مساعد رواقي - خدمة عملاء على مدار الساعة لمساعدتك في أي استفسار.',
                'price': 0,
                'is_new': True,
                'stock': 100,
                'category_slug': 'muslim-tools',
                'image_url': 'https://riwaqi.com/media/products/main/IMG_0775.webp',
            },
        ]

        for data in products_data:
            category = None
            if 'category_slug' in data:
                category = Category.objects.filter(slug=data.pop('category_slug')).first()

            image_url = data.pop('image_url', None)
            product, created = Product.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'category': category}
            )

            if created and image_url:
                try:
                    response = urllib.request.urlopen(image_url, timeout=10)
                    image_data = response.read()
                    ext = 'jpeg' if 'jpeg' in image_url else 'webp' if 'webp' in image_url else 'png'
                    filename = f"{data['slug']}.{ext}"
                    product.image.save(filename, ContentFile(image_data), save=True)
                    self.stdout.write(f'  ✓ {data["name"]} (مع صورة)')
                except Exception as e:
                    self.stdout.write(f'  ⚠ {data["name"]} (بدون صورة: {e})')
            elif created:
                self.stdout.write(f'  ✓ {data["name"]}')
            else:
                self.stdout.write(f'  - {data["name"]} (موجود)')

        self.stdout.write(f'  📦 {Product.objects.count()} منتج')
