# Direcionamentos didáticos

Origem: pedidos e correções de Fernanda Kipper durante a preparação de aulas de arquitetura e do board System One, em setembro/outubro de 2026. As regras abaixo são reutilizáveis; duração e quantidade de slides pertencem ao pedido atual.

| Direcionamento | Consequência no blueprint |
|---|---|
| O primeiro slide não pode ser um exemplo solto | Capa com tema/tópicos ou conceito introdutório antes do caso concreto. |
| Não é garantido que o aluno veja as aulas em sequência | Apresentar sistema, atores, entrada, regra e resultado novamente. |
| O conceito não pode ficar inteiramente restrito ao caso de matrícula | Definir o modelo geral antes de aplicá-lo ao exemplo. |
| Cada slide explica um conceito | Separar as definições e reservar a síntese para depois. |
| Preservar uma história ao longo da aula | Comparar entradas equivalentes e manter cores, nomes e contexto. |
| Caixas conectadas não tornam o acoplamento evidente | Especificar dependência concreta, alteração solicitada e propagação até o trecho afetado. |
| Mostrar instanciação e injeção claramente | Explicitar quem cria/obtém cada objeto e quem o recebe; poucos recortes de código reais. |
| O aluno deve bater o olho e entender como funciona | Planejar dados, transformação e efeito que a skill visual deverá desenhar. |
| Mais diagramas do que textos | Texto de tela curto; explicações longas nas notas; desenho carrega o mecanismo. |
| O momento WOW precisa aparecer na execução | Preparar uma previsão e uma mudança com resultado observável, distinguindo esperado de executado. |
| Usar slides do próprio Excalidraw quando pedidos | Conferir a apresentação nativa; arquivo com quadros/frames sozinho não comprova slides configurados. |
| O resultado visual precisa ser um .excalidraw | Solicitar arquivo editável e distinguir arquivo local, cena online e slides conferidos. |

## Referências audiovisuais fornecidas

- [Introdução à arquitetura](https://www.youtube.com/watch?v=jwBpiEoo8rI): referência para contexto e explicação técnica.
- [Explicação de código](https://www.youtube.com/watch?v=UKSj5VJEzps): referência de didática de conceitos de código.
- [Tokens](https://www.youtube.com/watch?v=tAhmBB_LSsc): continuidade do exemplo, comparação visual e demonstração prática.
- [Harness Engineering](https://www.youtube.com/watch?v=FNYA82Fn5m4): processos e ciclos representados no board.

Esta lista registra o papel das referências. Não prova que o agente atual assistiu aos vídeos; declarar os trechos realmente observados e quaisquer limitações. Os prints, exemplos visuais e aprendizados de edição estão no pacote `concept-to-excalidraw`.

## Divisão das skills

`prepare-technical-slides` define o que explicar, em qual ordem, com que contexto, evidências, tempo e notas. `concept-to-excalidraw` decide como tornar o mecanismo visível, produz o arquivo editável e opera a apresentação no produto quando houver acesso. Gerar áudio, configurar autenticação ou produzir uma demo completa não faz parte automaticamente desse handoff.
