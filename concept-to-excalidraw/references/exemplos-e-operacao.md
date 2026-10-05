# Exemplos e operação

Consultar quando for necessário transformar uma explicação abstrata em mecanismo concreto ou editar uma cena existente. Os exemplos são escolhas didáticas; não são templates obrigatórios para todo conceito.

## Acoplamento: mostrar a mudança que se propaga

**Insuficiente:** “Matrículas → Email” versus “Matrículas → Notificador”, com caixas e setas. O aluno ainda não sabe o que a matrícula exige do e-mail, qual mudança foi pedida ou o que precisa editar.

**Construção mais clara, em telas separadas:**

1. Contexto: pagamento confirmado permite acesso; a escola deseja trocar aviso por e-mail por WhatsApp.
2. Antes: destacar `new Email()` e `email.enviar(...)` dentro da classe de matrícula. Marcar os trechos concretos que precisam mudar para usar o outro canal.
3. Contrato: apresentar a operação esperada, por exemplo `Notificador.enviar(...)`, e o significado que as implementações devem preservar.
4. Depois: mostrar no main `Notificador notificador = new WhatsApp();` e a referência entregue a `new Matriculas(notificador)`. Marcar a montagem alterada e o código de matrícula preservado.

Adaptar assinaturas ao código real da aula. Não inserir pseudocódigo como se fosse um recorte literal de um arquivo existente.

**Precisão causal:** se o problema mostrado for queda do e-mail impedindo acesso, desenhar a ordem e o tratamento da exceção. A continuação do fluxo vem dessas decisões; uma interface sozinha não resolve indisponibilidade. Separar a explicação de substituição de implementações da explicação de tolerância à falha.

## Singleton: identidade e estado

Definir o padrão primeiro. Depois apresentar um contador didático compartilhado nesta execução:

- Desenhar **um único objeto** com `quantidade` dentro.
- Duas referências, `registroAna` e `registroBia`, apontam para ele.
- Mostrar a sequência: Ana registra → 0 para 1; Bia registra → 1 para 2.
- Mostrar a identidade `registroAna == registroBia` e explicar por que ambos leem 2.
- Em outra tela, mostrar o limite de escopo: outro processo começa com seu próprio contador; reiniciar perde o estado em memória.

Não desenhar dois objetos e chamar isso de Singleton. Não sugerir sincronização automática entre processos, persistência ou segurança de operações concorrentes. Mostrar construtor privado, campo que guarda a instância e método de acesso em uma tela dedicada, se esse mecanismo fizer parte da aula.

## Adapter: fazer a tradução aparecer

Após definir o padrão, contextualizar as interfaces e suas unidades:

- Aplicação: `9_000` centavos, equivalentes a R$ 90.
- SDK simulado: recebe reais como texto.
- Conversão ingênua: `9000` → `"9000"` → SDK interpreta R$ 9.000.
- Adaptação correta: `9000` → `"90.00"` → SDK interpreta R$ 90; retorno convertido para centavos.

Manter os valores e componentes equivalentes nas duas telas. Mostrar o cálculo que transforma a unidade. O cálculo correto explica o resultado; Adapter organiza a tradução junto da integração.

## Aprendizados operacionais do Excalidraw

Estas orientações vêm da execução do assistente nesta sessão. Usar APIs e documentação disponíveis no ambiente atual; nomes de botões e comportamentos podem mudar.

### Preservação e edição

- Antes de editar um quadro existente, obter uma cópia da cena. Identificar elementos/frames dentro e fora do escopo.
- Para acrescentar conteúdo, usar IDs novos e preservar os elementos anteriores, suas relações e ordem. Comparar o conteúdo preservado; contagem igual não prova preservação.
- Em fluxos por clipboard, o formato usado foi `{ "type": "excalidraw/clipboard", "elements": [...], "files": {} }`. Incluir arquivos referenciados quando houver imagens; não presumir `files` vazio em cenas existentes.
- Não acessar estado interno oculto da página para editar. Usar ferramentas específicas, interface e recursos de importação/exportação suportados.
- Ao substituir slides autorizados, atenção: apagar um frame pode deixar os filhos no canvas. Inspecionar o resultado antes de inserir a nova versão. Não repetir a exclusão cegamente, nem apagar o quadro todo quando somente uma seção foi autorizada.
- Aguardar o resultado observável de cada mutação antes da próxima ação dependente. Colagens repetidas sem conferir o estado já causaram duplicação de conteúdo.

### Slides nativos e revisão

- Frames podem ajudar a organizar a apresentação. Na geração local desta sessão, `customData.slidesOrder` foi usado para ordenação, mas a aceitação aconteceu na **lista de slides e no modo de apresentação do produto**. Tratar esse campo como detalhe observado, não contrato público estável.
- Confirmar o total e a ordem dos slides. Conferir capa, telas intermediárias e fechamento, uma a uma, em escala legível.
- Capturar o slide após a transição terminar, evitando julgar um frame da animação.
- Uma apresentação aberta anteriormente pode mostrar uma versão antiga. Se o editor e a apresentação divergirem, verificar a sessão em uso e iniciar a apresentação da versão atual pelo fluxo do produto. Não encerrar sessões de outras pessoas sem autorização.
- Não fixar quantidades como 10, 17 ou 18 slides: foram resultados de aulas específicas.

### Exportação e entrega

- Exportar a cena final revisada para `.excalidraw`; preservar elementos editáveis e arquivos associados.
- Conferir correspondência entre a cena online e a entrega local: textos, frames, ordem, quantidade e ausência de duplicações/órfãos decorrentes da edição.
- Salvar captura representativa no destino da tarefa e fornecer link editável quando disponível.
- Distinguir arquivo criado, importado, organizado em slides, revisado visualmente e aprovado pela usuária. Só declarar os estados efetivamente observados.
