from django.core.management.base import BaseCommand
from users.models import Team,User
from django.db.models import Q

class Command(BaseCommand):
    help = 'Ensure all team names are unique and save them'

    def handle(self, *args, **kwargs):
        teams = Team.objects.all()
        for team in teams:
            original_name = team.name
            unique_name = original_name
            counter = 1

            while Team.objects.filter(~Q(id=team.id), name=unique_name).exists():
                unique_name = f"{original_name}-{counter}"
                counter += 1

            if unique_name != team.name:
                team.name = unique_name
                team.save()
                self.stdout.write(self.style.SUCCESS(f'Updated team name from "{original_name}" to "{unique_name}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Team name "{team.name}" is already unique'))
