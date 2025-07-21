from django.core.management.base import BaseCommand
from core.models import PesquisaSPV


class Command(BaseCommand):
    help = "Lista os registros da tabela PesquisaSPV no terminal"

    def handle(self, *args, **kwargs):
        spvs = PesquisaSPV.objects.select_related(
            "cod_pesquisa", "cod_funcionario", "website"
        ).all()[:200]
        if not spvs:
            self.stdout.write("Nenhum registro encontrado em PesquisaSPV.")
            return

        for spv in spvs:
            self.stdout.write(
                f"Pesquisa: {spv.cod_pesquisa.nome} | "
                f"Funcionário: {spv.cod_funcionario.nome} | "
                f"Website: {spv.website.url} | "
                f"Resultado: {spv.resultado} | "
                f"Filtro: {spv.filtro}"
            )
