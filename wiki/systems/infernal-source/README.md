# Fonte Infernal — Lava Infernal e Reservatório

## Estado

`CONCEITO / PESQUISA — NÃO IMPLEMENTADO`

## Modelo

A fonte infernal é uma economia física semelhante em legibilidade ao reservatório hemático, mas com recurso e regras próprias.

`CASTER ⇄ INFERNAL LINK ⇄ NETHER RESERVOIR ⇄ INFERNAL LAVA (mB)`

## Invariantes

1. Lava Infernal só existe validamente no Nether.
2. Capacidade não equivale a conteúdo.
3. Não há regeneração gratuita só porque o tanque existe.
4. Nenhum portal, pipe, contraption, bucket ou container pode exportar a fonte para outra dimensão.
5. Um link não cria fluido; apenas autoriza consumo de uma reserva real.
6. Transações são server-authoritative e exatamente-once.

## HUD conceitual

Exemplo:

- capacidade: `140.000 mB`;
- armazenado: `22.500 mB`;
- display: `22.500 / 140.000 mB`;
- barra proporcional, sem simular regeneração.

## Geração/obtenção

A Wiki não fecha ainda se a Lava Infernal nascerá em pools próprias ou será produzida por ritual Nether-only. A opção preferencial para evitar worldgen excessivo é uma transformação ritual/infrastrutural bounded de lava do Nether usando catalisador infernal raro/provider-native. Isso precisa ser validado contra Cataclysm/Ignis/Soulfire e progressão antes de virar receita.

## Armazenamento

O reservatório deve:

- validar multiblock e dimensão;
- possuir capacidade derivada de estrutura/material;
- persistir volume real;
- impedir duplicação em break/move/rebuild;
- negar chunk-unloaded remote draw;
- ter owner/permissions;
- expor leitura de volume ao HUD;
- liquidar custo de spell atomicamente.

## Política dimensional

Ao sair do Nether:

- o link fica `SUSPENDED` ou inválido;
- spells que exigem Lava Infernal falham fechado;
- nenhuma quantidade é drenada remotamente;
- voltar ao Nether só reativa o link após revalidação de owner, estrutura, chunk e volume.

## Interação com Immersive Portals

Ver o reservatório através de um portal não o torna local. A superfície contínua não remove a fronteira de dimensão. O caster no Overworld não pode drenar uma fonte no Nether apenas porque há um portal aberto entre os locais.

## Dano ambiental

Contato com o fluido pode aplicar dano infernal/térmico e efeitos próprios, mas números, resistências e interaction tags serão fechados após deduplicação e Stage 08. O recurso não deve apagar item/NBT/entidade de forma arbitrária.

## Anti-abuso

- sem infinite loop de conversão lava → infernal → lava com ganho;
- sem storage duplication por chunk unload;
- sem export via nested containers;
- sem bypass por Create/Sable movement;
- sem remote drain cross-dimension;
- sem cobrança se o cast não commitar;
- sem cast se o recurso foi consumido por outra transação antes do commit.
