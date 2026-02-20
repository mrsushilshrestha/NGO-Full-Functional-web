from django.core.management.base import BaseCommand
from django.db import models
from apps.team.models import Member


class Command(BaseCommand):
    help = 'Generate member IDs for all members that are missing them'

    def handle(self, *args, **options):
        members_without_id = Member.objects.filter(
            models.Q(member_id__isnull=True) | models.Q(member_id='')
        )
        
        count = 0
        for member in members_without_id:
            if not member.member_id or member.member_id.strip() == '':
                old_id = member.member_id
                member.member_id = member.generate_member_id()
                member.save(update_fields=['member_id'])
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Generated ID for {member.name}: {old_id} -> {member.member_id}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully generated {count} member IDs.')
        )
