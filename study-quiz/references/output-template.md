# Contrato de saída

Dois formatos, um por modo de entrega. Nunca grave arquivo.

## Modo interativo

Uma mensagem por questão, seguida do seletor. Nada de `<details>`, nada de quiz inteiro numa mensagem só.

**Abertura**

```markdown
Quiz de {Tema} — {Nível ou faixa}. {N} questões, uma por vez. Escolha a alternativa no seletor; escreva "dica" se travar.
```

**Mensagem da questão** (vem antes de abrir o seletor)

```markdown
### Questão {n}/{total}

{enunciado no tom de especialista}

{bloco de código cercado, com a linguagem identificada, quando houver}
```

**Seletor** — 4 opções, na ordem A–D:

| Campo | Conteúdo |
|---|---|
| `header` | `Questão {n}/{total}` |
| `question` | A pergunta em uma linha (`Qual a saída exata?`, `Qual explicação está correta?`) |
| `label` | 3 a 5 palavras. Em questão de saída, a própria saída: `a, e, c, d, b` |
| `description` | A alternativa completa, como sairia no modo lote |

**Feedback** (1–2 linhas, logo após a escolha)

```markdown
Certo. {por que essa é a correta, em uma linha}
```

```markdown
Era {letra}: {por que a correta está certa}. {Por que a escolhida falha}.
```

**Placar final**

```markdown
### Resultado

{nível}: {x}/10 · reforço de base: {y}/3

{uma linha de diagnóstico: o que revisar primeiro}
```

**Mini-desafios** — um por mensagem, resposta escrita pela pessoa, correção antes do próximo:

```markdown
### Desafio {n}/3

{cenário e/ou bloco de código}

{o que a pessoa deve decidir, prever ou corrigir}
```

## Modo lote

Uma única mensagem Markdown.

```markdown
# Quiz: {Tema} — {Nível ou faixa}

## Seção 1: Perguntas Diretas (Múltipla Escolha)

### 1. {conceitual — “o que é X?”, “qual a diferença entre X e Y?”, “quando usar X?” — ou de código}
A) ...
B) ...
C) ...
D) ...

### 2. {de código — trecho a prever, diagnosticar ou corrigir; bloco cercado antes das alternativas}
A) ...
B) ...
C) ...
D) ...

### 3. … {alternando os dois tipos, até a última questão: 10, ou 12–13 com reforço de base}

## Seção 2: Mini-Desafios Práticos

### Desafio 1. {cenário e/ou bloco de código}
{o que o usuário deve decidir, prever ou corrigir}

### Desafio 2. … {seguindo até o Desafio 3}

<details>
<summary>Dicas</summary>

### Seção 1

1. {uma linha; aponta o caminho, não a resposta}
2. … {uma dica por questão, até a última}

### Seção 2

1. {uma linha}
2. … {até o Desafio 3}

</details>

<details>
<summary>Gabarito detalhado</summary>

### Seção 1

1. **Letra X.** Por que ela está certa. Por que A, B, C e D falham.
2. **Letra X.** *(reforço de base)* … {marca só nas de reforço, e só aqui}
3. **Letra X.** … {uma entrada por questão, até a última}

### Seção 2

1. Resposta esperada. Raciocínio passo a passo.
2. … {até o Desafio 3}

</details>
```

## Regras dos dois modos

- Numeração contínua e completa: questões 1 até a última (10, ou 12–13 com reforço), Desafios 1–3. O `…` acima é abreviação **deste template**, nunca da saída.
- Alternativas sempre A–D: uma por linha no lote, uma opção por alternativa no seletor.
- Código em bloco cercado com a linguagem identificada, sempre em mensagem — nunca dentro do rótulo de uma opção.
- Questão conceitual não tem bloco de código: no interativo a mensagem é só o enunciado; no lote, o enunciado e as quatro alternativas.
- Questão de reforço é indistinguível das demais enquanto o quiz corre. A marca `(reforço de base)` existe só no gabarito do lote e no placar final do interativo.
- Título `Quiz: {Tema} — {Nível ou faixa}` no lote; a mesma informação vai na linha de abertura do interativo.
