# ISS: Magic From The East 1.1.5 — technical audit

**Checkpoint histórico de identidade (2026-10-13):** ✅ [22/22 registros estáticos](EXACT-BINARY-SPELLS-1.1.5.md), [Java 21 #38449995162](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38449995162) **SUCCESS**; CurseForge file `7385201`, **1680780 bytes**, SHA-1 `e3552ea6b7b32b843c48bf0d857237d4b7129ab0` = JAR da modlist física #346. `MFTESpellRegistries` tem **11 Symmetry + 11 Spirit**, classes e IDs literais verificados sem branches; `ISS_MagicFromTheEast` liga o registrar no bootstrap. **COUNTED_EXACT** apenas para registro binário: **20/39 exatos / 19/39 pendentes**, **+0** raízes, mínimos **1857 global / 1855 escopo**. Fonte de parâmetros, runtime, Iron's 3.16.3, configuração e Survival continuam ⚠️. O workflow de auditoria fica fora da `main`.


## Reconciliação atual — 27/10/2026

As **22/22 fichas** passam a usar `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88` como **RELEASE_BOUNDED_SOURCE**. A fonte declara MC 1.21.1/mod 1.1.5/NeoForge 21.1.187/Iron’s 3.14.8; o host consultado é Iron’s 3.16.3 e o pack usa NeoForge 21.1.250. O JAR publisher foi revalidado por tamanho, SHA-1 e SHA-256 e coincide com o hash físico histórico. A [reconciliação](RELEASE-SOURCE-RECONCILIATION-1.1.5.md) contém cronologia e alcance dos confrontos binários; o [contrato comum](SPELL-PERK-BOUNDARIES-1.1.5.md) explica eventos, fórmulas herdadas e ownership.

O pin posterior `13208302c9fdf5beb171a328558cbef07a25ba46` não é referência geral da implementação instalada. O candidato `904a011b04cc33c45b5c4c79f97e2f7345ebeffb` também antecede mudanças presentes no JAR. As constatações abaixo são da fonte candidata salvo a prova binária estreita indicada; **não são defeitos reproduzidos no modpack**.

## Correções que afetam o design de perks

| Superfície | Informação útil e limite | Ficha com consumidores e referências |
|---|---|---|
| Sword Dance | Cooldown default **90 s**, confirmado no JAR; speed getter não determina sozinho o delta utilizado; callbacks recursivos e iFrames exigem dedup por fase | [Sword Dance](symmetry/sword-dance.md) |
| Cloud Ride | Recast **2** e chamadas ao lifecycle de summon confirmados no JAR; não aplicar modelo da fonte antiga sem recast | [Cloud Ride](symmetry/cloud-ride.md) |
| Drapes of Reflection | Campos binários de power **2 + (L−1)** e HP **1 + P**; reflexão/owner e remoção têm consumidores próprios | [Drapes](symmetry/drapes-of-reflection.md) |
| Underworld Aid / Impermanence | Config da fonte candidata tem cap default **20%** do max HP, não os 40% da fonte intermediária; dano pedido, cap e relógio são dimensões separadas | [Underworld Aid](symmetry/underworld-aid.md) |
| Jade Bullet | Dano direto e onda radial são tentativas separadas; alvo direto pode ser elegível na onda e callbacks herdados podem produzir caminhos adicionais | [Jade Bullet](symmetry/jade-bullet.md) |
| Anchoring Kunai | Tooltip e coeficiente entregue ao proxy usam escalas distintas; manter a divergência explícita e testar eventos de teleporte/posição/owner | [Anchoring Kunai](spirit/anchoring-kunai.md) |
| Phantom Charge | Informação exibida e dano gravado na entidade não são o mesmo valor; separar alocação da onda, colisão e aplicação | [Phantom Charge](spirit/phantom-charge.md) |
| Soul Catalyst / Soulburn | Crânios, dano inicial, efeito periódico e reset de iFrames têm consumidores diferentes; o guard posterior de imunidade por tag de entidade e a configuração posterior de aplicação por contato com blocos não integram a fonte candidata | [Soul Catalyst](spirit/soul-catalyst.md) e [Soul Burst](spirit/soul-burst.md) |
| Bone Hands | Lifecycle e recast locais precisam ser distinguidos dos summons que publicam `SpellSummonEvent`; não inferir hook a partir do tipo visual da entidade | [Bone Hands](spirit/bone-hands.md) |
| Kitsune / demais summons | Classes, quantidade, variações por instância, posição, ownership, finalização, atributos, recast e remoção variam por produtor; o JAR não contém classe `KitsuneAlpha` | [Kitsune Pack](spirit/kitsune-pack.md), [Jiangshi](symmetry/jiangshi-invoke.md), [Punishing Heaven](symmetry/punishing-heaven.md), [Revenant](spirit/revenant-of-honor.md), [Ashigaru](spirit/ashigaru-squad.md) |

## Registry, escolas e configuração

Continuam **11 Symmetry + 11 Spirit = 22 spells**. `LaunchSpell` e `QigongControllingSpell` estão comentadas no registry candidato e ausentes das inscrições ativas comprovadas. O JAR também declara **Dune como escola**, conforme confronto do inicializador `MFTESchoolRegistries`; não há spell Dune entre as 22. A antiga afirmação de escola comentada era baseada no source posterior.

A config MFTE é **SERVER**. Defaults da fonte: `impermanencePercentLimit=0.2`, `passChallenging=false`, `maxSoulburnDamage=10.0`, `soulburnDamageScaling=5`. `allowBlockProvidingSoulburn` não consta dessa versão de referência. `worldRestart()` é especificado por entrada, não universal. Valores do servidor implantado permanecem **NÃO VERIFICADOS**.

## Integração dos três projetos

O RPG atual foi consultado em `59ff2a0e827fd08faa603f4482f8104ac433383c`. Suas escolas custom normalizadas contêm `/`, que o contrato atual de `MasteryLaneCatalog.ironsDiscipline` rejeita; a chamada isolada foi conferida, sem reproduzir falha de jogo. Enshrouded permanece `a41dbb51aacb94b7b5db6517f1514b0b7aee3e83`, com classificação por IDs/tags concretos e um redutor de resistência. Ver os [métodos e limites documentados](SPELL-PERK-BOUNDARIES-1.1.5.md).

Não duplicar mana, cooldown, dano, cura, reflexão, lifecycle, iFrames, DOT, vínculo do proxy ou split de projéteis. Um evento de observação não oferece automaticamente mutação de targeting/área/tipo/hitbox. Sem seam demonstrado e adapter validado, manter **⛔ SEM_HOOK_SEGURO**.

## Progresso e QA

**22/22 dossiês editoriais reconciliados; 0/22 certificados estritos; +0 identidades semânticas.** Não há promoção automática no manifesto. O [índice global](../INDEX.md) mantém **138/2075 fichas observadas certificadas**, todas de Ars, e **0/164 providers integralmente certificados**. Os mínimos semânticos e as frações 20/39 do checkpoint de 13/10 acima são históricos; o índice atual usa outro recorte.

Permanecem **PENDING**: correspondência binária dos campos não auditados, configuração/datapacks, aquisição Survival, casts reais, servidor/cliente/multiplayer, claims/PvP/aliados, budgets e comportamento com múltiplos callbacks, spawn recusado, morte/unload/relog/restart, persistência, sync, autoria e integração de perks. A CI do Black Arcana verifica o projeto e a consistência documental; não certifica a execução das magias do addon no pack. Nenhum Stage, runtime ou dependência foi alterado.
