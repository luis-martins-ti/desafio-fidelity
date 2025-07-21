from django.db import models


class Estado(models.Model):
    cod_uf = models.PositiveSmallIntegerField(primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)  # Ex: 'SP'

    def __str__(self):
        return self.sigla


class Fornecedor(models.Model):
    cod_fornecedor = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    cod_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    cod_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Website(models.Model):
    website_id = models.AutoField(primary_key=True)
    url = models.URLField()

    def __str__(self):
        return self.url


class Servico(models.Model):
    cod_servico = models.AutoField(primary_key=True)
    civel = models.BooleanField(default=False)
    criminal = models.BooleanField(default=False)

    def __str__(self):
        return f"Cível: {self.civel}, Criminal: {self.criminal}"


class Pesquisa(models.Model):
    cod_pesquisa = models.AutoField(primary_key=True)
    cod_cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="pesquisas"
    )
    cod_uf = models.ForeignKey(
        Estado, on_delete=models.PROTECT, related_name="pesquisas_uf"
    )
    cod_servico = models.ForeignKey(
        Servico, on_delete=models.PROTECT, related_name="pesquisas"
    )
    tipo = models.IntegerField()
    cpf = models.CharField(max_length=14)
    cod_uf_nascimento = models.ForeignKey(
        Estado, on_delete=models.SET_NULL, null=True, related_name="nascimento_uf"
    )
    cod_uf_rg = models.ForeignKey(
        Estado, on_delete=models.SET_NULL, null=True, related_name="rg_uf"
    )
    data_entrada = models.DateField()
    data_conclusao = models.DateField(null=True, blank=True)
    nome = models.CharField(max_length=255)
    nome_corrigido = models.CharField(max_length=255, null=True, blank=True)
    rg = models.CharField(max_length=20)
    rg_corrigido = models.CharField(max_length=20, null=True, blank=True)
    nascimento = models.DateField()
    mae = models.CharField(max_length=255)
    mae_corrigido = models.CharField(max_length=255, null=True, blank=True)
    anexo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Lote(models.Model):
    cod_lote = models.AutoField(primary_key=True)
    cod_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.PROTECT, related_name="lotes"
    )
    cod_lote_prazo = models.IntegerField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    tipo = models.IntegerField()
    prioridade = models.IntegerField()

    def __str__(self):
        return f"Lote {self.cod_lote}"


class LotePesquisa(models.Model):
    cod_lote_pesquisa = models.AutoField(primary_key=True)
    cod_lote = models.ForeignKey(
        Lote, on_delete=models.CASCADE, related_name="lote_pesquisas"
    )
    cod_pesquisa = models.ForeignKey(
        Pesquisa, on_delete=models.CASCADE, related_name="lotes"
    )
    cod_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.PROTECT, related_name="pesquisas_atribuídas"
    )
    cod_fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.PROTECT, related_name="lote_pesquisas"
    )
    cod_uf = models.ForeignKey(
        Estado, on_delete=models.PROTECT, related_name="lote_pesquisas"
    )
    cod_funcionario_conclusao = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pesquisas_concluidas",
    )
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"LotePesquisa {self.cod_lote_pesquisa}"


class PesquisaSPV(models.Model):
    cod_pesquisa = models.ForeignKey(
        Pesquisa, on_delete=models.CASCADE, related_name="spv"
    )
    cod_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.PROTECT, related_name="pesquisas_spv"
    )
    website = models.ForeignKey(
        Website, on_delete=models.PROTECT, related_name="pesquisas_spv"
    )
    cod_spv = models.IntegerField()
    cod_spv_computador = models.IntegerField()
    cod_spv_tipo = models.IntegerField()
    filtro = models.IntegerField()
    resultado = models.IntegerField()

    def __str__(self):
        return f"SPV {self.cod_pesquisa_id} - Resultado: {self.resultado}"
