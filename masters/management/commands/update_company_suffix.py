from django.core.management.base import BaseCommand
from masters.models import Company

class Command(BaseCommand):
    help = "Update company_suffix for customer companies with no suffix, avoiding duplicates"

    def handle(self, *args, **options):
        # Fetch companies that are customers and have no suffix (null or empty)
        companies = Company.objects.filter(
            is_customer=True
        ).filter(
            company_suffix__isnull=True
        ) | Company.objects.filter(
            is_customer=True,
            company_suffix__exact=''
        )

        updated_count = 0

        for company in companies:
            # Generate acronym from company_name
            suffix = "".join([word[0].upper() for word in company.company_name.split() if word])
            
            if not suffix:
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Skipped {company.company_name}: could not generate suffix")
                )
                continue

            # Check if this suffix already exists in any other company
            if Company.objects.filter(company_suffix=suffix).exclude(id=company.id).exists():
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Skipped {company.company_name}: suffix '{suffix}' already exists")
                )
                continue

            # Update the company_suffix
            company.company_suffix = suffix
            company.save(update_fields=["company_suffix"])
            updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(f"✅ Updated {company.company_name} → suffix: {suffix}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Done! Updated {updated_count} companies.")
        )
