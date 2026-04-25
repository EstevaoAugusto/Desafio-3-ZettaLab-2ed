**<u>Inicio</u>** | [Data](./data/README.md) | [Features](./features/README.md) | [Notebooks](./notebooks/README.md) | [Scripts](./scripts/README.md) | [Reports](./reports/README.md) | [Interactive Reports](./interactive_reports/README.md) | [Dashboard](./dashboard/README.md) | [Models](./models/README.md) | [Metrics](./metrics/README.md) | [API](./api/README.md)

# Desafio-3-ZettaLab-2ed
Combate e Prevenção de Incêndios

## Índices

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Metodologia CRISP-DM](#metodologia-crisp-dm)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Execução com Docker (Recomendado)](#execução-com-docker-recomendado)
- [Responsáveis](#responsáveis)

## Estrutura do Projeto

* [Data](./data/README.md): Conjuntos de dados brutos e processados.
* [Features](./features/README.md): Dados transformados para treinamento de modelos.
* [Scripts](./scripts/README.md): Scripts de automação e pipelines.
* [Notebooks](./notebooks/README.md): Exploração e experimentos rápidos.
* [Dashboard](./dashboard/README.md): Visualização de métricas em tempo real.
* [Reports](./reports/README.md): Relatórios estáticos e documentos de análise.
* [Models](./models/README.md): Modelos treinados e arquivos serializados.
* [API](./api/README.md): Interface para consumo dos modelos e serviços.

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/) 
- [UV](https://github.com/astral-sh/uv) (Gerenciador de dependências)
- [Docker & Docker Compose](https://www.docker.com/)

## Instalação e Execução

### Configuração Local
1. Clone o repositório:
```bash
git clone git@github.com:EstevaoAugusto/fire-control-data-science.git
cd fire-control-data-science/
```

2. Instale as dependências com o `uv`:
```bash
uv sync
```

3. Configure o ambiente:
```bash
# Cria todos os diretorios necessarios do projeto caso nao estejam pre
python config_path.py

# O projeto usa o datalake da biblioteca 'BaseDosDados' a qual necessita do ID projeto Google Cloud.
echo "GOOGLE_CLOUD_ID_PROJECT='<id-projeto-aqui>'" > .env 
```

4. Caso deseja visualizar os notebooks, execute-os sequencialmente no diretório 'notebooks'

---

## Execução com Docker (Recomendado)

O projeto está configurado para rodar via Docker, garantindo que o ambiente da API e dos modelos seja idêntico ao de desenvolvimento.

### Passos para rodar a API:

1. **Construir a imagem**:
   O Docker utilizará o `uv` para instalar as dependências de forma otimizada através de *multi-stage builds*.
   ```bash
   docker-compose build
   ```

2. **Subir os serviços**:
   Este comando iniciará a API na porta `8000`. Graças aos volumes configurados, alterações no código em `api/` ou `scripts/` serão refletidas em tempo real (Hot Reload).
   ```bash
   docker-compose up
   ```

3. **Verificar integridade**:
   Acesse o endpoint de saúde para confirmar o funcionamento: `http://localhost:8000/health`.

### Notas de Implementação Docker:
- **PYTHONPATH**: A raiz do projeto (`/app`) está incluída no PATH para permitir que a API importe módulos de `scripts/` e arquivos de configuração globais.
- **Persistência**: As pastas `data/`, `models/`, `metrics/` e `features/` são montadas como volumes, garantindo que os resultados gerados no container persistam na sua máquina local.

---

## Metodologia CRISP-DM
O projeto segue as etapas de Entendimento de Negócio, Compreensão, Preparação, Modelagem, Avaliação e Implementação (Deployment).

## Responsáveis
- Luciana Laibe Santos Silva (Comunicação e Marketing) 
- Estevão Augusto da Fonseca Santos (Ciência e Governança de Dados) 
- Hugo Dias Pontello (Desenvolvimento de Software) 
- Lorrana Verdi Flores (Desenvolvimento de Software) 
- Bruna Oliveira Pereira (Geotecnologia) 
- Geovanna Alexandre Possidonio (Gestão de Projetos) 