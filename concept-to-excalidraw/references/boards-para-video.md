# Boards para vídeo: aprendizados da revisão System One

Consultar ao criar um board para gravação, reduzir um diagrama excessivamente textual ou analisar uma referência audiovisual. Consolida as correções de Fernanda e os resultados observados na produção em 05/10/2026. Os exemplos são escolhas didáticas, não limites de tamanho ou templates obrigatórios.

## O problema que a revisão resolveu

O primeiro board tinha caixas repetidas, títulos, explicações e diagramas arranjados como slides. Mesmo com formas editáveis e pouco conteúdo por área, a explicação dependia demais da leitura. Fernanda pediu “mais diagramas do que textos” e que o funcionamento do conceito aparecesse visualmente.

**Critério:** o aluno deve conseguir seguir o que entra, o que acontece, o que muda e o que sai. Apagar frases sem desenhar essas relações não resolve o problema. Uma seta genérica entre nomes também não explica o mecanismo.

## Escolher a composição pela intenção

| Pedido | Composição e entrega |
|---|---|
| Board para vídeo | Canvas contínuo, núcleos de explicação com tamanhos próprios, relações entre eles, zoom e espaço para desenhar ao vivo. Arquivo `.excalidraw` editável. |
| Diagrama isolado | Somente o mecanismo solicitado, com o contexto mínimo necessário. |
| Apresentação | Slides nativos no produto, sequência conferida e uma ideia por slide; conservar arquivo editável portátil. |

Em um board, evitar grade uniforme de cartões, molduras de slide e repetição de rodapés. Uma comparação pode ter duas colunas alinhadas ou faixas pretas, se isso ajuda a comparar operações. Assimetria é uma opção funcional, não uma exigência estética.

Abrir com definição breve ou introdução do tema. Antes do caso concreto, situar o sistema e os atores, mesmo quando a história foi usada em outra aula. Manter essa entrada nas comparações para o aluno enxergar a mudança relevante.

## Fazer a explicação acontecer no desenho

| Conceito | Desenho que demonstra o mecanismo | Evitar |
|---|---|---|
| Geração autorregressiva | Entrada inicial; token produzido; seta desse token até sua posição no contexto ampliado da próxima etapa. Repetir poucas etapas legíveis. | Setas que terminam em espaços vazios ou só um bloco “gera texto”. |
| Distribuição de probabilidades | Opções com cores estáveis, valores e barras proporcionais na mesma escala. | Barras iguais para valores diferentes; trocar a cor de uma opção entre diagramas. |
| Decisão do software | Resultado do modelo entrando em uma condição; caminhos SIM/NÃO até ações concretas e diferentes. Comparar entrada concentrada com ambígua. | Dizer que “a IA decide tudo” ou deixar o destino das setas abstrato. |
| Formato versus correção | Resposta permitida atravessando a validação e chegando ao destino errado; valor fora do conjunto visivelmente rejeitado. | Selo de schema válido que pareça garantir veracidade. |
| Custo | Lotes de tokens contáveis, soma e preço com denominador explícito. | Número solto ou confusão entre dólar, centavo e milhão de tokens. |
| Latência | Faixa sobre uma escala temporal com unidade e origem identificadas. | Cronômetro decorativo sem mostrar o intervalo ou prometer tempo fixo. |
| Benchmark | Origem dos rótulos de referência → comparação → barras em escala comum; distinguir concordância de verdade verificada. | Percentual de “precisão” sem dizer o que foi medido. |

Os exemplos probabilísticos são ilustrativos até serem executados. Confiança e probabilidade da classe podem ser medidas diferentes; conferir a definição da fonte antes de desenhar números. Limiares escolhidos pelo software não são propriedades universais do modelo. Não transformar números de preço, latência ou benchmark deste caso em fatos permanentes da skill.

## Dividir board e guia da professora

No board: título, frase explicativa curta, dados, operações, rótulos, unidades e exceções indispensáveis para interpretar o desenho. No guia, quando solicitado ou já existente: explicação longa, nuances, perguntas de condução, fontes completas e limites das afirmações.

Não remover uma ressalva necessária para tornar uma comparação enganosa. Por exemplo, um chat também pode restringir o formato de saída; a comparação precisa identificar qual mecanismo está sendo comparado. Na ausência de guia, preservar a precisão no próprio material ou na entrega.

## Ler referências audiovisuais

Inspecionar quadros de momentos conceituais e acompanhar a progressão: o que aparece antes da explicação, o que a professora aponta, como os dados se transformam e para onde o zoom se move. Usar transcrição para a fala e imagens para o desenho. Se o vídeo não estiver acessível, registrar essa limitação; não afirmar que foi assistido.

Referências usadas nesta produção:

- [Tokens](https://www.youtube.com/watch?v=tAhmBB_LSsc): em aproximadamente 6:17, a mesma palavra sob vocabulários distintos, com partes coloridas. O trecho indicado pela usuária começa em [8:13](https://www.youtube.com/watch?v=tAhmBB_LSsc&t=493s). A continuidade da entrada torna a comparação compreensível.
- [Harness Engineering](https://www.youtube.com/watch?v=FNYA82Fn5m4): em aproximadamente 5:48, contexto → LLM → ferramentas → resultado, com retorno ao contexto. O desenho acompanha um processo e suas dependências.

Essas observações são pontuais, não uma transcrição integral nem análise de todos os quadros. Aplicar o princípio ao novo conceito, sem copiar a história, os números ou todos os rabiscos.

## Revisão visual antes de entregar

1. Conferir o board inteiro: ordem de leitura, espaço, agrupamentos e conexões entre ideias.
2. Aproximar cada núcleo na escala de gravação. O panorama com tudo minúsculo não comprova legibilidade.
3. Seguir cada seta da origem ao destino e comparar seu significado com a explicação. Nos loops, verificar qual dado volta a qual posição.
4. Inspecionar especialmente barras abaixo de frases, valores nas extremidades, notas embaixo de setas e títulos junto à barra de ferramentas. Corrigir sobreposições no elemento, sem mascará-las com zoom.
5. Após corrigir, rever as regiões afetadas. Manter agrupamentos que permitam selecionar e aproximar um mecanismo completo.
6. Conferir a cena final e o arquivo exportado. Em uma revisão total autorizada, comparar a cena atual com o backup antes de substituir para identificar intervenções posteriores do usuário.
7. Quando for necessário confirmar persistência, recarregar depois do salvamento e conferir o resultado. Exportar a versão final do produto; contagem de elementos sozinha não comprova que textos, relações e imagens coincidem.

Nesta produção, funcionaram os atalhos `Shift+1` para enquadrar tudo, seleção do grupo + `Shift+2` para aproximar e `Esc` para remover a seleção. São observações do produto naquela versão: usar a documentação e interface atuais se mudarem.

A entrega deve distinguir arquivo editável salvo, cena atualizada, revisão visual e aprovação da professora. Uma captura representativa demonstra o trabalho online; não substitui o `.excalidraw` nem uma exportação limpa solicitada. Não afirmar compatibilidade testada na edição gratuita se ela não foi aberta ali. Não substituir outro board pessoal para testar importação.
