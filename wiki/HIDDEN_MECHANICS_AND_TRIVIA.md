# Mecânicas não óbvias e trivia

## O cast não paga antes de saber se pode acontecer

A engine valida identidade, replay, progressão, cooldown, alvo, disponibilidade de custo e política de mundo **antes** da reserva. Mesmo após reservar, o custo só é confirmado se o efeito tiver sucesso.

## Falha de observer não desfaz um cast concluído

Observers de sucesso rodam depois de efeito, commit e início de cooldown. Uma exceção nesse observer é isolada porque tentar refundar nesse ponto poderia duplicar recursos ou criar inconsistência entre efeito e custo.

## O radial não conjura por si só

O radial escolhe. A execução passa novamente pelo server ingress. Isso evita que uma tela client-side seja uma fonte de autoridade.

## Quick slots começam sem tecla

Existem oito quick casts, mas nenhum possui binding padrão. É deliberado para reduzir colisão com modpacks grandes.

## Não existe resource bar permanente própria

O Stage 05 escolheu HUD contextual. Recursos podem vir de Iron's, Ars ou Malum, e o Black Arcana não tenta substituir permanentemente as barras/interfaces dos hosts.

## `particleDensity`, `reducedMotion` e `reducedFlashes` não são buffs/debuffs

São opções client-only. Elas nunca participam da validação server-side e algumas são reservas para apresentação futura.

## Um spell id e um cooldown group não precisam representar a mesma coisa

Cooldowns são agrupados por `groupId`. Isso permite criar famílias de ações que compartilham bloqueio sem forçar um único spell id.

## O teto de 30 dias é uma guarda, não um balanceamento

`ArcanaCooldownSpec` aceita até 30 dias de ticks. Esse é um limite absoluto de estrutura para impedir valores absurdos/overflow, não uma indicação de que exista atualmente magia com cooldown de semanas.

## Custos percentuais são frações

`PERCENT_OF_MAX` usa `0.0–1.0`, não `0–100`. Um valor `0.25` representa 25% do máximo.

## Targeting e permissão são separados

Resolver “quem seria atingido” não significa autorizar o efeito. A world/entity safety layer pode negar um alvo já encontrado.

## Integrações usam conteúdo de probe

Classes como `IronsArcanaProbeSpell` e `EidolonArcanaProbeRitual` existem para demonstrar/testar que os hosts conseguem atravessar as bridges. Elas não devem ser contadas como o catálogo final de magia negra.

## Os 32 candidatos são matéria-prima, não release content

Stage 01 congelou 32 candidate specifications para evitar perder o trabalho de referência. Isso não alterou o fato de que Spell Domains e Rituals ainda são stages posteriores.
