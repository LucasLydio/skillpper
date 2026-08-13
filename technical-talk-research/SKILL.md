---
name: technical-talk-research
description: Pesquisa e estrutura palestras técnicas em PT-BR com fontes atuais e verificáveis. Use ao pedir referências para uma explicação técnica, levantamento de artigos ou posts recentes, curadoria de fontes, roteiro ou slides de palestra, ou revisão da bibliografia de uma apresentação. Pesquisa somente no catálogo de fontes aprovado, mantém rastreabilidade de cada afirmação técnica e exige um slide final de Referências bibliográficas. Cria apresentações exclusivamente pelo MCP da Gamma, usando o template `nkhgcucv1lw00wc`.
---

# Pesquisa para Palestras Técnicas

Use esta skill para enriquecer uma palestra ou responder uma pesquisa pontual. Trabalhe em PT-BR, a menos que seja solicitado outro idioma.

## Regras inegociáveis

- Pesquise na web antes de afirmar que uma informação é nova, atual, quantitativa ou resultado de pesquisa. Registre a data de acesso.
- Use exclusivamente as fontes do [catálogo aprovado](references/source-catalog.md) como referências da palestra. Não use resultados de busca, resumos de IA ou conhecimento prévio como evidência.
- Em uma palestra, percorra todo o catálogo: busque cada fonte cuja categoria seja pertinente ao tema; quando não houver resultado útil, registre `sem resultado relevante`. Para pedidos rápidos, consulte as fontes mais adequadas, mas nunca fora do catálogo.
- Trate Hacker News, TechCrunch e X como sinais, descoberta de contexto ou opinião. Corrobore afirmações técnicas, de produto ou de mercado com uma fonte primária ou de pesquisa do catálogo sempre que ela existir.
- Não transforme hipótese, opinião ou correlação em fato. Marque como `opinião`, `hipótese`, `evidência preliminar` ou `sem consenso` quando aplicável.
- Não invente autores, datas, resultados, URLs, estatísticas ou citações. Se uma fonte estiver inacessível, anote a limitação e siga com fontes acessíveis.
- Gere toda apresentação usando o MCP da Gamma. Não use PowerPoint, Google Slides, HTML, PDF ou outra ferramenta para criar a apresentação final.
- Use obrigatoriamente o template Gamma `nkhgcucv1lw00wc` em toda apresentação. Não substitua nem omita o template.

## Escolher o modo de trabalho

### Pesquisa sob demanda

Use quando receber perguntas como “quais referências explicam RAG?”, “há novidades sobre agentes?” ou “me ajude a comprovar esta afirmação”.

1. Identifique a pergunta, o público e o nível técnico a partir do pedido; só peça contexto quando ele mudar materialmente a resposta.
2. Formule consultas curtas em português e inglês, combinando o tema com cada domínio pertinente do catálogo.
3. Priorize: artigos acadêmicos e repositórios de papers; depois laboratórios e documentação técnica; depois análises de especialistas; por último notícias e sinais sociais.
4. Para cada resultado útil, extraia: `S-id`, título, autor ou organização, data de publicação, URL canônica, data de acesso, tipo de evidência, afirmação que ele sustenta e ressalvas.
5. Entregue uma síntese com links, separando fatos sustentados, opiniões e lacunas. Inclua uma seção `Fontes` com a bibliografia completa dos itens usados.

### Construir ou revisar uma palestra

Use quando o pedido incluir roteiro, estrutura, slides, palestra, keynote, apresentação ou revisão de referências.

1. Defina a tese, público, duração e resultado desejado. Se o usuário não fornecer, faça uma suposição explícita e siga.
2. Liste as afirmações técnicas antes de desenhar os slides. Pesquise cada uma e atribua IDs como `S01`, `S02`.
3. Crie o arco: problema → modelo mental → evidência/demonstração → limites e trade-offs → conclusão acionável.
4. Coloque os IDs das fontes que sustentam cada afirmação técnica no próprio slide ou em suas notas. Não deixe números, marcos históricos, comparações, resultados de estudos ou funcionamento de sistemas sem citação.
5. Reserve o último slide substantivo para `Referências bibliográficas`. Ele deve conter todas — e somente — as fontes citadas, em formato completo e legível. Não coloque conteúdo após esse slide, exceto créditos legais obrigatórios.
6. Materialize primeiro um blueprint Markdown seguindo [o modelo](references/blueprint-template.md). Rode o validador antes de gerar ou entregar a apresentação:

```bash
python3 .claude/skills/technical-talk-research/scripts/validate_references.py caminho/da/palestra.md
```

7. Antes de gerar os slides, confirme que o MCP da Gamma está disponível. Use o recurso exposto pelo MCP para criar a apresentação a partir do blueprint e passe o identificador de template exato `nkhgcucv1lw00wc`. Não invente nomes de ferramentas do MCP: use a ferramenta que ele disponibilizar para aplicar templates ou criar apresentações.
8. Se o MCP da Gamma não estiver conectado ou o template não puder ser aplicado, pare antes de gerar a apresentação e informe o bloqueio. Peça ao usuário para conectar/configurar o Gamma em Conductor, em **Settings → MCP**. Não faça fallback para outro gerador.
9. Faça a revisão final no resultado da Gamma: confirme o template `nkhgcucv1lw00wc`, as citações em slides técnicos, o slide final de referências e a ausência de slides após ele. Abra cada link, confirme que o texto sustenta a frase citada, confira data/autor e remova duplicatas.

## Padrão de citações

- Cite no slide com `[S01]` imediatamente após a afirmação ou como rodapé. Para vários suportes, use `[S01, S04]`.
- No slide final, use uma entrada por ID: `- [S01] Autor/organização. “Título”. Publicado em AAAA-MM-DD. URL. Acesso em AAAA-MM-DD.`
- Para paper acadêmico, acrescente versão, venue quando houver, e DOI/arXiv ID se disponível.
- Para post social, preserve o autor, data, URL do post e rotule `opinião` quando não houver uma evidência técnica independente.
- Uma referência pode apoiar mais de um slide; não use uma única referência para justificar alegações que ela não faz.
- Slides de título, agenda, transição ou exercício sem alegação técnica devem conter `[sem-afirmacao-tecnica]` para documentar a exceção.

## Critérios de qualidade da pesquisa

- Prefira a fonte original de um resultado: paper para experimento, laboratório para anúncio ou metodologia, documentação oficial para comportamento de produto.
- Dê contexto operacional: condições do experimento, versão do sistema, população/amostra, métricas e limitações relevantes.
- Compare fontes quando houver discordância e explique de onde ela vem; não escolha silenciosamente a que confirma a tese.
- Dê mais espaço às fontes que sustentam a tese central. Um painel de referências não compensa uma narrativa sem evidência.
- Se uma referência for antiga, mantenha-a apenas por valor histórico/fundacional e procure uma atualização no catálogo.

## Entrega esperada

Para pesquisa, entregue: resposta direta, evidências ligadas a cada ponto, limitações e bibliografia.

Para palestra, entregue: premissas, título e tese, sequência de slides com textos/citações, notas de limites e o slide final de referências. Crie a apresentação final exclusivamente pelo MCP da Gamma com o template `nkhgcucv1lw00wc`. Inclua o resultado do validador e corrija qualquer erro antes da entrega.

## Recursos

- [Catálogo aprovado de fontes](references/source-catalog.md): domínios, perfis e função de cada fonte.
- [Modelo de blueprint](references/blueprint-template.md): formato que o validador lê.
- `scripts/validate_references.py`: verifica o contrato mínimo de citações e bibliografia do blueprint.
