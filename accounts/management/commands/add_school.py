from django.core.management.base import BaseCommand , CommandError
from django.contrib.auth.models import User
from accounts.models import School

class Command(BaseCommand):
    help = 'Add a new sschool'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='name of the school'),
        parser.add_argument('--address', type=str, help= "address of school", default='')

        parser.add_argument("--creator", type=str, help="add userUsername of the creator (required if no request context is available")
        parser.add_argument('--auto_id', type=str, help= "id")


    def handle(self, *args, **options):
        name = options['name']
        address = options ['address']
        creator = options['creator']
        auto_id = options['auto_id']


        if not creator:
            self.stderr.write(self.style.ERROR('creator is required'))
            return
        
        try:
            creator = User.objects.get(username=creator)

        except User.DoesNotExist:
            raise CommandError(f"User with username '{creator}' does not exist.")
        

        try:
            school = School(name=name,address=address, creator=creator,updater=creator, auto_id=auto_id)
            school.save()
            self.stdout.write(self.style.SUCCESS(f"School '{school.name}' added successfully!"))
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")