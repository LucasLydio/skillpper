---
name: concept-to-excalidraw
description: Transformar conceitos técnicos em diagramas e boards visuais editáveis no Excalidraw, entregando arquivo .excalidraw. Usar para explicar mecanismos, revisar visuais abstratos ou textuais e executar planos visuais de aulas; criar slides nativos e exportar imagens quando solicitados.
---

# Conceito → Excalidraw

Esta skill executa a produção visual e entrega **um arquivo `.excalidraw` editável como resultado principal**. Imagens exportadas e slides nativos são complementos conforme o pedido. O resultado deve explicar o mecanismo do conceito, com dados e relações visíveis.

O arquivo deve poder ser aberto no Excalidraw comum, sem conta Plus e sem depender do modo de apresentação. Para um board de vídeo, organizar áreas navegáveis com zoom, uma ideia por área e espaço para anotações ao vivo. Não converter automaticamente um pedido de board em slides. Se houver slides nativos, conservar também a versão portátil e distinguir o que foi verificado em cada produto.

Para a preparação completa de uma aula — pesquisa, fontes, duração e sequência — integrar com `prepare-technical-slides` quando ela estiver disponível e essa preparação fizer parte do pedido. A presente skill funciona sozinha: receber o conceito, o contexto e as referências diretamente da usuária ou de um blueprint. Para um pedido de diagrama isolado, produzir somente esse diagrama.

## 1. Ler o plano visual

Para cada diagrama ou slide, identificar no pedido/blueprint:

- Conceito ou pergunta central e a frase que o explica. Abrir a explicação com contexto conceitual; não começar por um exemplo sem introdução.
- Contexto mínimo: sistema, atores, entrada, regra e resultado.
- Elementos, operações, estados e valores que tornam o mecanismo visível.
- Mudança a destacar, comparação e consequência esperada.
- Textos, fontes, notas e ordem a preservar.

Se faltar contexto, completar apenas o necessário a partir dos materiais disponíveis. Se houver um problema conceitual ou de sequência, sinalizar à etapa de preparação e corrigi-lo antes de renderizar. Não inventar evidências, resultados de execução ou conteúdo técnico para preencher o layout.

## 2. Construir o mecanismo visual

Para boards de vídeo ou críticas a excesso de texto, ler [boards para vídeo](references/boards-para-video.md): composição, exemplos da revisão System One, análise audiovisual e revisão em escala de gravação.

- Para boards de vídeo, o desenho deve carregar a explicação: representar dados concretos, transformações, acumulação, distribuição, caminhos e resultados. Reduzir a fala escrita a uma frase de apoio e rótulos necessários. Não preencher caixas com parágrafos conceituais.
- Usar o espaço conforme o mecanismo: fluxo central com detalhes ao redor, comparações alinhadas e aproximações por zoom. Evitar grades de quadros iguais, fundos de slide, cabeçalhos repetitivos e rodapés em todas as áreas quando o pedido for um board.
- Rever o que acontece nas referências, além da aparência. Em tokens, a palavra se divide e as partes viram números; em um agente, contexto e resultados percorrem o ciclo. Produzir transformação equivalente para o novo conceito. Retirar texto sem acrescentar mecanismo visual não resolve a crítica.
- Colocar uma explicação breve **acima do desenho**. Abaixo, tornar visíveis entrada → operação/relação → transformação ou mudança → efeito.
- Desenhar cada parte com função reconhecível. Nomes de classes em caixas e setas entre elas não explicam, sozinhos, como o conceito funciona.
- Dar significado a cada seta: chamada, transformação, dependência de tipo, implementação, sequência ou referência a um objeto. Nomear relações que não sejam óbvias. Não confundir dependência no código com fluxo da execução.
- Mostrar o detalhe concreto que causa o efeito. Para acoplamento, explicitar o que uma parte conhece/exige da outra e qual alteração alcança qual trecho.
- Em comparações, manter entradas, posições e cores equivalentes; destacar a variável alterada e seu resultado. Usar valores, unidades e estados concretos quando ajudarem.
- Quando houver código, mostrar poucas linhas legíveis e alinhadas com os arquivos reais. Para DI, tornar visível quem obtém/cria os objetos e quem os recebe no construtor. Factory pode ter sua criação aberta em um diagrama próprio.
- Não atribuir à aparência do diagrama um comportamento que o código não produz. Diferenciar resultado esperado de resultado observado.

Consultar [exemplos e operação](references/exemplos-e-operacao.md) para acoplamento, Singleton e Adapter. O [contraexemplo criticado](assets/contraexemplo-acoplamento.png) mostra o tipo de abstração que Fernanda considerou insuficiente.

## 3. Aplicar o estilo das referências

Inspecionar [vocabulário](assets/referencia-vocabulario.png) e [encoding](assets/referencia-encoding.png) antes de desenhar. São os prints fornecidos por Fernanda.

| Elemento | Direção visual |
|---|---|
| Fundo | Branco, com respiro entre etapas e espaço para anotações durante a gravação |
| Título | Preto, manuscrito; pequena marca vertical roxa à esquerda |
| Explicação | Frase curta em cinza, abaixo do título e acima do diagrama |
| Caixas | Traço de desenho à mão; preenchimentos suaves e contornos coloridos |
| Cores | Azul, verde, lilás, amarelo/laranja e vermelho suave conforme a função; significado estável nas comparações |
| Cabeçalhos | Faixas pretas com texto claro quando ajudarem a identificar cenários |
| Etapas | Rótulos curtos; alinhar dados equivalentes e mostrar transformação |
| Ênfase | Setas, círculos, sublinhados e notas roxas quando ajudarem a explicação |
| Código | Monoespaçado, poucas linhas e tamanho legível na apresentação |

A paleta e a hierarquia acima são uma interpretação dos prints, não medidas exatas ditadas pela usuária. Reproduzir a linguagem visual, não copiar rabiscos incidentais ou afirmações técnicas das imagens. Não preencher espaço livre com decoração.

## 4. Montar slides nativos

Quando o plano for uma apresentação:

- Usar a funcionalidade de **slides nativos do Excalidraw** e preservar a sequência definida em `prepare-technical-slides`.
- Cada slide de conteúdo deve executar a mensagem central recebida. Se o conteúdo não couber com legibilidade, dividir a explicação sem reduzir tudo a texto minúsculo e sincronizar a alteração com o blueprint.
- Conferir lista, ordem e navegação no modo de apresentação. Um canvas organizado ou frames em um arquivo não provam, por si sós, que a apresentação foi configurada no produto.
- Preservar citações e notas fornecidas. Marcas administrativas do blueprint, como `[sem-afirmacao-tecnica]`, não são conteúdo visual para o aluno.
- Manter textos, formas, setas e trechos de código editáveis. Imagens exportadas acompanham o original; não substituir a cena inteira por uma imagem achatada.
- Não fixar dimensões, quantidade de slides ou duração a partir de uma aula passada. Usar a composição e o recorte do pedido atual.

## 5. Editar, exportar e entregar

- Em cenas existentes, guardar uma cópia antes de substituir conteúdo e preservar elementos/IDs fora do escopo autorizado.
- Usar ferramentas específicas ou interface/importação/exportação suportadas pelo produto. Consultar a seção operacional em [exemplos e operação](references/exemplos-e-operacao.md) para frames órfãos, duplicação, transições e apresentações antigas.
- Revisar cada diagrama e cada slide em escala de apresentação: texto sem corte/sobreposição, setas identificáveis, valores corretos, relações claras e espaço suficiente.
- Aplicar a pergunta de Fernanda: **o aluno bate o olho, lê a explicação acima e entende como funciona?** Se faltar uma causa ou dado, corrigir o desenho.
- Conferir a correspondência com o blueprint e os materiais atuais: termos, classes, unidades, estados, resultados, fontes e ordem.
- Salvar o `.excalidraw` final e sincronizá-lo com a cena online, quando houver. Confirmar ausência de duplicações e restos da versão anterior.
- Quando o pedido incluir imagens, exportar PNG/SVG dos diagramas ou slides solicitados, com textos legíveis e enquadramento completo; conferir o arquivo exportado. Não entregar apenas screenshot da interface como se fosse uma exportação limpa.
- Entregar arquivo editável, imagens pedidas e link da cena quando disponível. Para alterações online, incluir captura representativa como prova da versão final. Captura de conferência e imagem para uso da professora são entregas diferentes.
- Usar o destino escolhido pela usuária, respeitando as permissões atuais. Informar bloqueios concretos e o estágio real quando só for possível preparar arquivos locais.

## Origem e escopo

Consolidada dos pedidos e correções de Fernanda Kipper na preparação das aulas de arquitetura e na revisão do board System One, em setembro/outubro de 2026. Os três prints incluídos são as referências e o contraexemplo enviados por ela. A preferência por desenhos que mostrem o funcionamento e pela entrega `.excalidraw` é explícita; detalhes de paleta, composição e operação são aprendizados da produção. Os exemplos não fixam duração de aula, número de diagramas ou tema. Geração de áudio, autenticação em serviços e escrita de demos completas são tarefas separadas, não iniciadas por esta skill.
