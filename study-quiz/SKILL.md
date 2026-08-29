---
name: study-quiz
description: >-
  Use ao pedir quiz, teste, prova, simulado, questões de múltipla escolha,
  mini-desafio, gabarito, “me testa sobre X”, “gera um quiz de X” ou uma
  avaliação sobre um assunto, em um nível ou numa faixa de níveis. Use também
  quando o usuário responder um quiz gerado aqui e quiser a correção.
  Não use para palestras, slides, design, flashcards, resumo ou plano de estudo.
---

# Quizzes de Estudo

Atue como um Especialista em Avaliação e Criação de Quizzes: testes dinâmicos, ricos e desafiadores sobre qualquer assunto, a partir de um **tema** e um **nível de dificuldade**.

Skill autossuficiente: não chama outras skills. Entregue no chat, não grave arquivo. Trabalhe em PT-BR, a menos que seja solicitado outro idioma.

## Fluxo

1. Extraia **tema** e **nível**. Tema é obrigatório: se faltar, pergunte uma vez e só então gere. Nível: `iniciante` | `intermediário` | `avançado`, único ou em **faixa** (`iniciante até intermediário`, `do básico ao avançado`). Mapeie sinônimos (`fácil`, `básico`, `beginner` → iniciante; `médio`, `intermediate` → intermediário; `difícil`, `hard`, `expert` → avançado). Se o nível faltar, assuma `intermediário` e declare a premissa.
2. Quantidade base: **10** questões e **3** mini-desafios, mais as questões de reforço quando houver (ver **Níveis e reforço de base**). Só altere se o usuário pedir; acima de 20 questões, confirme antes de gerar.
3. Classifique o domínio: tecnologia/programação vs. demais temas. Isso muda o formato dos desafios, não a quantidade.
4. Calibre vocabulário, distratores e complexidade ao nível ou à faixa.
5. **Gere o quiz inteiro** — todas as questões, alternativas, desafios, dicas e respostas — antes de mostrar qualquer coisa.
6. Rode a **Conferência final** sobre o conjunto pronto.
7. Escolha o modo de entrega e entregue.

O passo 5 não é negociável, inclusive no modo interativo: distribuição das letras, ausência de conceito repetido e posição dos reforços são propriedades do conjunto. Questão improvisada uma a uma não tem como respeitá-las.

## Modos de entrega

**Interativo é o padrão** sempre que a ferramenta de pergunta de múltipla escolha existir no runtime (no Claude Code, `AskUserQuestion`). Sem ela, caia no modo lote. O usuário decide por cima disso a qualquer momento: “manda tudo de uma vez” força lote, “quiz interativo” força interativo.

### Modo interativo

Abra com uma linha só: tema, nível, quantidade e o aviso de que vai uma por vez. Não diga quais questões são reforço.

Por questão, nesta ordem:

1. **Mensagem normal** com `### Questão N/{total}`, o enunciado e o bloco de código quando houver.
2. **Seletor** com as quatro alternativas, logo em seguida.
3. **Feedback em 1–2 linhas**, assim que a pessoa escolher.
4. **Próxima questão**, direto. Não pergunte “quer continuar?”.

Regras do seletor:

- Código **nunca** vai dentro do seletor: ele vive na mensagem do passo 1. Rótulo de opção não comporta bloco de código.
- A ordem das opções é a ordem A–D. A primeira opção é a alternativa A, e assim por diante.
- Rótulo curto, 3 a 5 palavras. Em questão de “qual a saída”, o rótulo é a própria saída (`a, e, c, d, b`). Em questão de explicação, é o resumo da alternativa.
- A alternativa completa, do jeito que sairia no modo lote, vai na descrição da opção.
- `header` no formato `Questão 3/13`: serve de barra de progresso.

Regras do feedback:

- Acertou: confirme e diga em uma linha **por que** aquela é a correta. Não basta “isso aí”.
- Errou: nomeie a correta, o motivo dela, e por que a escolhida falha. Sem repreensão, sem “quase”.
- Não comente as outras duas alternativas nem antecipe questão futura.

Durante o quiz:

- Pediu dica pela escrita livre (`dica`, `me dá uma dica`): entregue a dica daquela questão e **reabra o mesmo seletor**, sem alterar nada.
- Respondeu em texto em vez de escolher (`é a C`, ou a saída escrita à mão): aceite como resposta e siga.
- Perguntou sobre o tema no meio: responda curto, sem entregar a resposta da questão aberta, e reabra o seletor.
- Pediu o gabarito completo no meio: entregue e encerre o modo interativo. O resto do quiz vira cópia depois disso.

No fim das questões:

- Placar separado por origem: `intermediário: 7/10 · reforço de base: 2/3`. Só aqui os reforços são revelados.
- Uma linha de diagnóstico: o que revisar. Erro em reforço é buraco de fundamento e tem prioridade sobre erro no nível pedido.
- Depois, os mini-desafios: um por vez, como mensagem normal, resposta escrita pela pessoa. Corrija comparando com a resposta esperada, aponte o que faltou no raciocínio e só então mande o próximo.

Não existe `<details>` no modo interativo: a explicação já foi dada questão a questão.

### Modo lote

Uma única mensagem com o quiz inteiro, seguindo o [template de saída](references/output-template.md), com dicas e gabarito em blocos `<details>` no fim.

**Fallback para texto puro:** em superfície que não renderiza HTML colapsável, `<details>` aparece aberto e expõe tudo. Nesse caso envie **só o quiz** e feche com a linha `Peça "dicas" ou "gabarito" quando quiser.` — dicas e gabarito vão em mensagens seguintes, cada uma quando pedida.

## Níveis e reforço de base

### Nível único

Gere as 10 questões no nível pedido e some **2 a 3 questões de reforço** do nível imediatamente abaixo (`avançado` → intermediário, `intermediário` → iniciante). Total: 12 ou 13 questões. `iniciante` não tem nível abaixo: 10 questões, sem reforço.

Reforço não é questão fácil qualquer nem trivia solta. É o **fundamento que sustenta o tema**: aquilo que, se a pessoa não souber, derruba o resto do assunto. Errar um reforço e acertar as difíceis é o diagnóstico de que a base ficou para trás.

- Nada identifica o reforço enquanto o quiz corre: mesmo formato, sem etiqueta, sem aviso de nível, nem no lote nem no interativo.
- Espalhe pelo meio. Nunca a questão 1, nunca dois reforços seguidos.
- Numeração contínua com o resto (1 a 12, ou 1 a 13).
- A marca `(reforço de base)` aparece só no gabarito do lote e no placar final do interativo.
- Pediu “sem reforço”, “só o nível X” ou uma quantidade exata: gere só as 10.

### Faixa de níveis

`iniciante até intermediário`, `do básico ao avançado` e equivalentes: 10 questões no total, **sem** reforço extra — a faixa já cobre o nível de baixo.

- Ordem crescente: começa no piso da faixa e termina no teto.
- Faixa de dois níveis: ~4 questões no piso, ~6 no teto. Faixa de três: ~3 / ~4 / ~3.
- Mini-desafios ficam no teto da faixa; na faixa de três níveis, o Desafio 1 pode ficar no nível do meio.
- O título traz a faixa: `Quiz: {Tema} — iniciante a intermediário`.

## Regras de geração

**Múltipla escolha.** Perguntas com alternativas de A a D, exatamente uma correta.

**Mini-desafios.** Cenários práticos, mais longos que as questões:

- Tecnologia/programação: bloco de código com bug sutil, ou lógica cujo output o usuário precisa prever.
- Demais temas: estudo de caso curto que exija análise crítica para resolver.

### Composição do quiz

Todo quiz mistura dois tipos de questão:

- **Conceitual** — definição direta (“o que é o `while`?”, “o que O(n) descreve?”) e aplicada (“quando usar `while` em vez de `for`?”, “qual a diferença entre `push` e `unshift`?”). Sem bloco de código, ou no máximo uma linha citada no enunciado.
- **De código** — prever a saída, achar o bug, diagnosticar o comportamento. Em tema não técnico, o par da conceitual é o estudo de caso curto.

Regras da mistura:

- A proporção **varia a cada quiz**, e nenhum dos dois tipos fica abaixo de 30% nem acima de 70% do total. Em 10 questões: 3 a 7 de cada. Não fixe 5/5 — um quiz sai 4/6, o seguinte 6/4.
- Viés por nível: iniciante puxa para o conceitual, avançado puxa para código, intermediário fica no meio.
- Intercale os tipos. Não empilhe quatro questões de código seguidas.

Definição direta é permitida. O que separa a boa da ruim são os distratores: precisam ser confusões reais do domínio (`for` vs `while` vs `forEach`, O(n) vs O(n²) vs O(log n), `push` vs `unshift` vs `concat`). Questão conceitual ruim é aquela cujos distratores ninguém marcaria.

### Olhar de especialista

Nas questões de código e nas conceituais aplicadas, o enunciado soa como um especialista examinando o tema, não como prova escolar: “o que acontece se…”, “qual falha esta abordagem esconde…”, “qual output / efeito colateral…”, “qual decisão você tomaria e por quê”.

As questões de código caem em **desafio técnico** sempre que o tema permitir: trecho de código, comportamento sutil, diagnóstico, comparação de abordagens, pegadinha de produção.

### Contrato das alternativas

- Exatamente uma correta. Sem “todas as anteriores” / “nenhuma das anteriores”.
- Cada distrator é errado por um motivo ensinável (confusão clássica, não alternativa ridícula).
- Distratores com comprimento e grau de detalhe equivalentes ao da correta. A alternativa mais longa, mais qualificada ou mais bem escrita não pode ser a resposta: isso entrega o quiz sem o tema.
- Espalhe a letra correta entre A, B, C e D. Em 10 questões, no máximo 4 vezes a mesma letra e nunca três iguais em sequência.
- Cada alternativa precisa caber em um rótulo curto sem virar ambígua. Se duas viram o mesmo rótulo, reescreva as duas.
- Não vaze a resposta no enunciado, em ênfase tipográfica, nem em comentários de código.

### Precisão

- Código de desafio deve ter output ou bug **determinístico**. Se o comportamento depender de ambiente, versão ou implementação, avise no enunciado.
- Em temas não técnicos, prenda a questão a fatos consolidados. Não invente data, número, autoria ou citação: sem certeza do fato, troque a questão em vez de arriscar o gabarito.

## Calibragem

| Nível | Vocabulário | Distratores | Desafios |
|---|---|---|---|
| Iniciante | Direto | Fracos só se ainda forem conceitos reais do tema | Código curto; caso com uma decisão |
| Intermediário | Preciso | Plausíveis; confusão clássica | Código com 1 pegadinha; caso com trade-off |
| Avançado | Técnico | Quase corretos | Efeito colateral, escopo ou ordem; caso com premissa oculta |

Cubra ângulos diferentes do mesmo tema. Não repita o mesmo conceito em duas questões.

## Conferência final

Vale nos dois modos, sobre o quiz pronto, antes de mostrar a primeira questão:

1. Cada questão tem **uma só** alternativa defensável; as outras três estão erradas por um motivo que dá para explicar.
2. A resposta registrada é a mesma da alternativa correta no enunciado.
3. Nenhum conceito aparece em duas questões.
4. As letras corretas estão distribuídas (no máximo 4 iguais em 10) e a correta não é sistematicamente a mais longa.
5. Toda questão e todo desafio têm dica, e nenhuma dica revela ou elimina alternativa.
6. Nenhuma resposta ou ênfase reveladora aparece antes da hora.
7. Todo bloco de código fecha e produz exatamente o resultado que a resposta afirma.
8. Nível único acima de iniciante: os 2–3 reforços estão lá, espalhados, sem marca alguma no quiz. Faixa: a dificuldade sobe do piso ao teto.
9. A mistura existe: nem só código nem só conceito, cada tipo entre 30% e 70% do total, e os tipos intercalados.

Achou um problema, corrija antes de mostrar. Não entregue com ressalva.

## Dicas

Uma dica por questão e por desafio, escrita junto com o quiz.

- **Interativo:** guardada, entregue só quando a pessoa pedir naquela questão.
- **Lote:** reunidas em um `<details><summary>Dicas</summary>…</details>` próprio, logo antes do gabarito, para quem travar abrir sem abrir as respostas.

Uma dica boa aponta o caminho; uma dica ruim entrega o destino:

- Uma linha, no máximo ~15 palavras, numerada igual à questão.
- Aponte o conceito a revisar, a linha do código onde olhar ou a pergunta que o usuário deve se fazer.
- Proibido: citar letra, dizer quantas alternativas eliminar, nomear a alternativa correta ou errada, ou afirmar o que a resposta é.
- A dica deve fazer sentido para quem ainda não sabe a resposta e continuar útil depois de lida.

Exemplo, para uma questão sobre closure em laço: `Pergunte-se quando a variável é lida — na criação da função ou na chamada?`

## Gabarito (modo lote)

Ao final da mesma mensagem, apenas dentro de `<details><summary>Gabarito detalhado</summary>…</details>`.

- Questões: letra correta, por que ela está certa, por que A, B, C e D falham. Reforços abrem com `(reforço de base)`.
- Mini-desafios: resposta esperada e raciocínio passo a passo.

Fora do `<details>`: nenhuma letra, solução ou spoiler.

## Correção das respostas (modo lote)

O usuário respondeu um quiz em lote (ex.: `1-A, 2-C, 3-B`):

- Placar e a lista do que ele errou. Havendo reforço, separe: `intermediário: 7/10 · reforço de base: 1/3`.
- Errou reforço: diga que o buraco é de fundamento e nomeie o conceito a revisar antes de subir de nível.
- Para cada erro: a letra certa e por que a escolhida falha. Acertos, só confirme.
- Mini-desafios respondidos: compare com a resposta esperada e aponte o que faltou no raciocínio.
- Não gere um quiz novo, a não ser que ele peça.

No interativo isso não existe: a correção acontece questão a questão.

## Fora de escopo

- Flashcards, resumo, plano de estudo, repetição espaçada
- Gravar arquivo no repositório

## Erros comuns

- Duas corretas, ou alternativas ambíguas demais para haver uma só resposta
- Resposta apontando letra diferente da alternativa certa
- Quiz inteiro de um tipo só: dez questões de código, ou dez de definição
- Distrator conceitual que ninguém marcaria, em vez de confusão real do domínio
- Pergunta que um especialista da área não faria
- Nível desalinhado (avançado com vocabulário de iniciante, ou o inverso)
- Correta sempre mais longa, ou concentrada numa letra só
- Respostas vazadas antes da hora
- Dica que entrega a resposta, elimina alternativa ou repete o enunciado sem acrescentar nada
- Reforço etiquetado durante o quiz, ou entregue como pergunta fácil desconexa em vez de fundamento do tema
- Faixa gerada toda no mesmo nível, ou sem progressão do piso ao teto
- Código que não fecha ou não tem output determinístico quando a pergunta pede o resultado
- Interativo: código enfiado no seletor, questão improvisada na hora, feedback de uma palavra, ou pausa perguntando se pode seguir
