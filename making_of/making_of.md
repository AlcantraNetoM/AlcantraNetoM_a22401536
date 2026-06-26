# Making Of

Documento de apoio ao processo de modelação da aplicação.

## Objetivo

Registar a evolução do modelo, as decisões tomadas, os erros encontrados e as respetivas correções.

## Organização das imagens

As fotografias, capturas ou exportações do DER devem ser colocadas na pasta `imagens/`.

Exemplos de ficheiros esperados:
- `imagens/der_v1.png`
- `imagens/der_v2.png`
- `imagens/anotacoes_escola.jpg`

## Diário de bordo

### Versão 1

- Data:
- O que foi pensado inicialmente:
- Entidades consideradas:
- Relações previstas:
- Problemas encontrados:

### Versão 2

- Data:
- O que mudou:
- Novas entidades/atributos:
- Relações revistas:
- Correções aplicadas:

### Versão final

- Data:
- Resultado final do modelo:
- Principais decisões:
- Validações feitas:

## Erros identificados e correções

### Erro 1

- Descrição do erro:
- Como foi identificado:
- Correção aplicada:
- Resultado após a correção:

### Erro 2

- Descrição do erro:
- Como foi identificado:
- Correção aplicada:
- Resultado após a correção:

## Justificação das decisões de modelação

> Preencher com, pelo menos, 2 decisões por entidade.

### Curso e Unidades Curriculares

- Decisão 1: separar `Curso` de `UnidadeCurricular`.
- Justificação: a API devolve o detalhe do curso e o plano curricular como blocos diferentes, por isso a separação evita duplicação e facilita a manutenção.
- Decisão 2: ligar as UC ao curso através de uma relação `ForeignKey`.
- Justificação: as unidades curriculares pertencem ao contexto de um curso concreto e a relação permite navegar do curso para o respetivo plano curricular no admin e na importação.
- Decisão 3: guardar atributos de detalhe e de plano curricular na UC.
- Justificação: o JSON das UC mistura dados estruturais com conteúdos pedagógicos, e guardar ambos torna a aplicação mais útil para consulta e análise.
- Decisão 4: manter campos textuais largos para apresentação, objetivos, programa, metodologia, avaliação e bibliografia.
- Justificação: estes campos têm conteúdo longo e variável, pelo que `TextField` evita cortes desnecessários e suporta melhor a informação real da API.

### Pessoas

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

### Escola

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

### Ginásio

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

### Receita

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

### Loja

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

### Festivais

- Decisão 1:
- Justificação:
- Decisão 2:
- Justificação:

## Importação de Dados

- Foi descarregado um snapshot da Lusófona API para `data/ULHT260-PT.json` e para os ficheiros das respetivas unidades curriculares.
- Foi criado o comando `import_lusofona_course` para carregar o curso e as UC usando o ORM do Django.
- A modelação foi alargada com atributos adicionais para refletir melhor os dados reais devolvidos pela API.

## Anexos

- Inserir aqui as imagens do DER, esquemas intermédios e apontamentos relevantes.
- Se necessário, referir as versões dos modelos ou migrações associadas.
