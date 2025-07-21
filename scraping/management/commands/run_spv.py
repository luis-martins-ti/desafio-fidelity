from django.core.management.base import BaseCommand
from scraping.services.spv_spider import SPVAutomatico


class Command(BaseCommand):
    help = "Executa SPV automático para um filtro específico ou todos (0 a 3)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filtro",
            type=int,
            choices=[0, 1, 2, 3],
            help="Filtro a ser executado (0: CPF, 1: RG, 2: Nome, 3: RG alternativo)",
        )

    def handle(self, *args, **options):
        filtro = options.get("filtro")
        if filtro is not None:
            self.stdout.write(self.style.NOTICE(f"Executando filtro único: {filtro}"))
            spv = SPVAutomatico(filtro)
            spv.pesquisar()
        else:
            self.stdout.write(self.style.NOTICE("Executando todos os filtros (0 a 3)"))
            for f in range(4):
                spv = SPVAutomatico(f)
                spv.pesquisar()
