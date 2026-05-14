from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users_app.models import UserProfile
from products_app.models import Category, Product


class Command(BaseCommand):
    help = 'Creates sample categories, products, users'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...\n')

        # 1. Admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@shilposhop.com',
                password='admin123'
            )
            UserProfile.objects.create(user=admin, phone='01700000000', address='Dhaka')
            self.stdout.write('  Created admin  (username: admin | password: admin123)')
        else:
            self.stdout.write('  Admin already exists')

        # 2. Customer
        if not User.objects.filter(username='rahim').exists():
            rahim = User.objects.create_user(
                username='rahim',
                email='rahim@example.com',
                password='user1234'
            )
            UserProfile.objects.create(user=rahim, phone='01811111111', address='Chittagong')
            self.stdout.write('  Created customer (username: rahim | password: user1234)')

        # 3. Categories
        cat_names = [
            'Sarees', 'Panjabis', 'Western Wear',
            'Jewelry', 'Home Decor', 'Leather Goods',
            'Pottery', 'Nakshikantha Embroidery',
        ]
        cats = {}
        for name in cat_names:
            cat, _ = Category.objects.get_or_create(name=name)
            cats[name] = cat
        self.stdout.write(f'  {len(cat_names)} categories ready')

        # 4. Products
        products = [
            # Sarees
            {'category': cats['Sarees'], 'product_name': 'Muslin Jamdani Saree',
             'description': 'Handwoven Jamdani Muslin Saree crafted by artisans in Demra, Dhaka. GI-tagged heritage textile with intricate floral motifs. Lightweight and breathable, perfect for weddings and festivals.',
             'price': 4500, 'stock': 15},
            {'category': cats['Sarees'], 'product_name': 'Tangail Cotton Saree',
             'description': 'Soft hand-loomed Tangail cotton saree with traditional stripe pattern. Made by weavers cooperative in Tangail district. Fair trade certified.',
             'price': 1800, 'stock': 25},
            {'category': cats['Sarees'], 'product_name': 'Rajshahi Silk Saree',
             'description': 'Pure Rajshahi Mulberry silk saree with zari border. Produced by women weavers in Rajshahi. Rich texture and vibrant colour.',
             'price': 6800, 'stock': 10},
            # Panjabis
            {'category': cats['Panjabis'], 'product_name': 'Handloom Cotton Panjabi - White',
             'description': 'Classic white panjabi made from pure handloom cotton. Stitched by tailors trained under a vocational programme. Comfortable for daily wear and Eid.',
             'price': 950, 'stock': 40},
            {'category': cats['Panjabis'], 'product_name': 'Block-Print Panjabi - Indigo',
             'description': 'Indigo block-print panjabi using natural vegetable dyes. Printed by artisan women in Rajshahi. Each piece is slightly unique.',
             'price': 1350, 'stock': 30},
            # Western Wear
            {'category': cats['Western Wear'], 'product_name': 'Organic Cotton Kurta Top',
             'description': 'Loose-fit organic cotton kurta top for women. Naturally dyed in earthy tones. GOTS certified organic cotton. Perfect with jeans or skirts.',
             'price': 1200, 'stock': 35},
            {'category': cats['Western Wear'], 'product_name': 'Handloom Linen Shirt - Men',
             'description': 'Casual linen shirt woven on traditional handlooms. Breathable and lightweight for summer. Made in Bangladesh under fair-wage employment.',
             'price': 1500, 'stock': 28},
            # Jewelry
            {'category': cats['Jewelry'], 'product_name': 'Conch-Shell Bangles (Set of 6)',
             'description': 'Traditional shankha (conch shell) bangles — a symbol of Bengali heritage. Hand-carved by Shankhari artisans of Old Dhaka. Ivory-white and elegant.',
             'price': 650, 'stock': 50},
            {'category': cats['Jewelry'], 'product_name': 'Terracotta Necklace - Floral',
             'description': 'Handmade terracotta necklace with floral motifs painted by women artisans. Lightweight and eco-friendly. No two pieces are identical.',
             'price': 480, 'stock': 60},
            {'category': cats['Jewelry'], 'product_name': 'Brass Dokra Earrings',
             'description': 'Dokra lost-wax cast brass earrings — ancient tribal craft. Bold geometric design with hypoallergenic hooks.',
             'price': 550, 'stock': 45},
            # Home Decor
            {'category': cats['Home Decor'], 'product_name': 'Bamboo Wall Basket - Set of 3',
             'description': 'Handwoven bamboo wall baskets in graduated sizes. Made using sustainably harvested bamboo from Sylhet. Minimalist Bangladeshi aesthetic.',
             'price': 1100, 'stock': 22},
            {'category': cats['Home Decor'], 'product_name': 'Jute Macrame Table Runner',
             'description': 'Hand-knotted jute macrame table runner, 180 cm long. Eco-friendly golden jute — Bangladesh\'s own golden fibre.',
             'price': 750, 'stock': 30},
            {'category': cats['Home Decor'], 'product_name': 'Hand-Painted Wooden Wall Clock',
             'description': 'Round wall clock with a hand-painted Ricksha Art design. Silent quartz movement, 30 cm diameter. Made by Dhaka street-art collective.',
             'price': 1800, 'stock': 18},
            # Leather Goods
            {'category': cats['Leather Goods'], 'product_name': 'Full-Grain Leather Wallet - Brown',
             'description': 'Slim bifold wallet in full-grain cowhide leather, stitched by hand. Fair labour certified. Holds 6 cards and cash. Ages beautifully with use.',
             'price': 1200, 'stock': 35},
            {'category': cats['Leather Goods'], 'product_name': 'Leather Tote Bag - Tan',
             'description': 'Spacious handcrafted leather tote with canvas lining. Each bag hand-stitched by women leather workers in a cooperative.',
             'price': 3500, 'stock': 12},
            {'category': cats['Leather Goods'], 'product_name': 'Hand-Stitched Leather Journal',
             'description': 'A5 leather-cover journal with 200 pages of recycled paper. Saddle-stitch binding by artisan bookbinders. Perfect gift for students.',
             'price': 900, 'stock': 40},
            # Pottery
            {'category': cats['Pottery'], 'product_name': 'Terracotta Tea-Cup Set (4 pieces)',
             'description': 'Rustic terracotta tea cups hand-thrown on potter\'s wheel in Rajshahi. Food-safe glaze, holds 150 ml. Brings warmth to your morning chai.',
             'price': 720, 'stock': 30},
            {'category': cats['Pottery'], 'product_name': 'Blue Pottery Flower Vase',
             'description': 'Hand-painted cobalt-blue pottery vase, 25 cm tall. Geometric patterns inspired by Mughal tile work. Individually fired and painted.',
             'price': 1100, 'stock': 25},
            {'category': cats['Pottery'], 'product_name': 'Terracotta Piggy Bank - Elephant',
             'description': 'Charming hand-moulded elephant piggy bank in natural terracotta. Painted with traditional floral motifs. Great as a gift.',
             'price': 350, 'stock': 55},
            # Nakshikantha
            {'category': cats['Nakshikantha Embroidery'], 'product_name': 'Nakshikantha Cushion Cover (Set of 2)',
             'description': 'Pair of cotton cushion covers with traditional Nakshikantha running-stitch embroidery. Motifs: fish, lotus, peacock. Made by women artisans in Jamalpur.',
             'price': 1400, 'stock': 20},
            {'category': cats['Nakshikantha Embroidery'], 'product_name': 'Nakshikantha Kantha Quilt - Small',
             'description': 'Hand-stitched Nakshikantha kantha in 100% cotton, 90x120 cm. Traditional motifs: sun, tree of life, rural scenery. A Bengali heirloom.',
             'price': 5500, 'stock': 8},
            {'category': cats['Nakshikantha Embroidery'], 'product_name': 'Nakshikantha Embroidered Sling Bag',
             'description': 'Canvas sling bag with Nakshikantha embroidery panel on front. Interior zip pocket, adjustable strap. Urban design meets village artistry.',
             'price': 2200, 'stock': 18},
        ]

        count = 0
        for data in products:
            _, created = Product.objects.get_or_create(
                product_name=data['product_name'],
                defaults=data
            )
            if created:
                count += 1
        self.stdout.write(f'  {count} products created ({len(products) - count} already existed)')


        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('  Sample data created!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('  Admin    -> username: admin    password: admin123')
        self.stdout.write('  Customer -> username: rahim    password: user1234')
        self.stdout.write('')
        self.stdout.write('  Run: python manage.py runserver')
        self.stdout.write('  Open: http://127.0.0.1:8000/')
