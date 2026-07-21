from django.core.management.base import BaseCommand
from shop.models import Fabric, Product


class Command(BaseCommand):
    help = "Seed the database with starter fabrics and products."

    def handle(self, *args, **options):
        fabrics_data = ["Khaddar", "Lawn", "Linen"]
        fabrics = {}
        for name in fabrics_data:
            f, _ = Fabric.objects.get_or_create(name=name, slug=name.lower())
            fabrics[name] = f

        products = [
            dict(name="Rustic Khaddar — Rust", slug="rustic-khaddar-rust", fabric=fabrics["Khaddar"],
                 description="Hand-loomed winter khaddar, 3.5 metre unstitched suit length. Warm, breathable, built for cold Punjab mornings.",
                 price=4200, stock=18, metres=3.5,
                 swatch_color_start="#8B4A3E", swatch_color_end="#4a2620"),
            dict(name="Summer Lawn — Saffron", slug="summer-lawn-saffron", fabric=fabrics["Lawn"],
                 description="Lightweight printed lawn, breathable weave designed for peak summer heat.",
                 price=3600, stock=25, metres=3.0,
                 swatch_color_start="#E0A23D", swatch_color_end="#8a5c1f"),
            dict(name="Everyday Linen — Olive", slug="everyday-linen-olive", fabric=fabrics["Linen"],
                 description="Structured linen blend that holds its shape through a full work day.",
                 price=5100, stock=12, metres=3.5,
                 swatch_color_start="#3f4a3a", swatch_color_end="#232922"),
            dict(name="Festive Khaddar — Maroon", slug="festive-khaddar-maroon", fabric=fabrics["Khaddar"],
                 description="Richer maroon khaddar with a subtle sheen, cut for festive wear.",
                 price=4800, stock=9, metres=3.5,
                 swatch_color_start="#6e1f1f", swatch_color_end="#2c0d0d"),
            dict(name="Pastel Lawn — Sage", slug="pastel-lawn-sage", fabric=fabrics["Lawn"],
                 description="Soft sage lawn with a fine floral micro-print, made for daily wear.",
                 price=3400, stock=20, metres=3.0,
                 swatch_color_start="#9fae8c", swatch_color_end="#4c5a3e"),
            dict(name="Formal Linen — Charcoal", slug="formal-linen-charcoal", fabric=fabrics["Linen"],
                 description="Charcoal linen with a crisp finish, suited for office and formal stitching.",
                 price=5400, stock=15, metres=3.5,
                 swatch_color_start="#4a4a4a", swatch_color_end="#1c1c1c"),
        ]

        created = 0
        for p in products:
            _, was_created = Product.objects.get_or_create(slug=p["slug"], defaults=p)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(fabrics)} fabrics, created {created} new products."))
