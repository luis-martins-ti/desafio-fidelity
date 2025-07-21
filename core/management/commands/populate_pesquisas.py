from django.core.management.base import BaseCommand
from core.models import Pesquisa, Cliente, Estado, Servico
from faker import Faker
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Popula Cliente, Estado, Servico e Pesquisa com dados fake coerentes"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")

        # Cria Estados se não existirem
        estados = []
        if Estado.objects.count() == 0:
            estados_data = [
                (35, "SP"),
                (33, "RJ"),
                (31, "MG"),
            ]
            for cod_uf, sigla in estados_data:
                estado = Estado.objects.create(cod_uf=cod_uf, sigla=sigla)
                estados.append(estado)
            self.stdout.write(f"Estados criados: {len(estados)}")
        else:
            estados = list(Estado.objects.all())

        # Cria Clientes se não existirem
        clientes = []
        if Cliente.objects.count() == 0:
            for _ in range(10):
                cliente = Cliente.objects.create(nome=fake.company())
                clientes.append(cliente)
            self.stdout.write(f"Clientes criados: {len(clientes)}")
        else:
            clientes = list(Cliente.objects.all())

        # Cria Serviços se não existirem
        servicos = []
        if Servico.objects.count() == 0:
            for _ in range(5):
                servico = Servico.objects.create(
                    civel=random.choice([True, False]),
                    criminal=random.choice([True, False]),
                )
                servicos.append(servico)
            self.stdout.write(f"Serviços criados: {len(servicos)}")
        else:
            servicos = list(Servico.objects.all())

        # Cria Pesquisas
        for _ in range(200):
            cliente = random.choice(clientes)
            estado = random.choice(estados)
            servico = random.choice(servicos)

            nascimento = fake.date_of_birth(minimum_age=18, maximum_age=90)
            data_entrada = fake.date_between(
                start_date=nascimento + timedelta(days=18 * 365), end_date=date.today()
            )
            data_conclusao = (
                None
                if random.random() < 0.5
                else fake.date_between(start_date=data_entrada, end_date=date.today())
            )

            pesquisa = Pesquisa.objects.create(
                cod_cliente=cliente,
                cod_uf=estado,
                cod_servico=servico,
                tipo=random.choice([0, 1, 2, 3]),
                cpf=fake.cpf(),
                cod_uf_nascimento=estado,
                cod_uf_rg=estado,
                data_entrada=data_entrada,
                data_conclusao=data_conclusao,
                nome=fake.name(),
                nome_corrigido=None,
                rg=str(fake.random_number(digits=9, fix_len=True)),
                rg_corrigido=None,
                nascimento=nascimento,
                mae=fake.name_female(),
                mae_corrigido=None,
                anexo=None,
            )
            self.stdout.write(f"Pesquisa criada: {pesquisa}")

        self.stdout.write(
            self.style.SUCCESS("População inicial concluída com sucesso.")
        )
