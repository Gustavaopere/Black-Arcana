# Companions! 1.3.4 — matriz de engenharia causal dos nove Magic Books

**Checkpoint 17/10/2026 — PR #825 (draft).** Este documento complementa o inventário físico e as fichas individuais, sem alterar contagem semântica nem runtime.

## Proveniência e medidas separadas

- Modlist física do sibling: posição **#104**, JAR `companions-neoforge-1.21.1-1.3.4.jar`, mod ID `companions`, SHA-1 `23f6e4f27a457a8d016412e495e417c0b36fdcc1`; KnightLib instalado 2.0.1; Minecraft 1.21.1, NeoForge.
- Auditoria binária de registro das **9/9** subclasses de `AbstractMagicBook`: [EXACT-BINARY-MAGIC-BOOKS-1.3.4.md](EXACT-BINARY-MAGIC-BOOKS-1.3.4.md), [CI de evidência física #38458161666](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38458161666) (SUCCESS). **COUNTED_EXACT restringe-se ao registry/factories comprovados**.
- Código-fonte público da versão correlacionada: [Xylonity/Companions@95c9445e1514648418064ea90b5c373e81375d2f](https://github.com/Xylonity/Companions/tree/95c9445e1514648418064ea90b5c373e81375d2f). Os métodos e os parâmetros listados abaixo são **SOURCE-CAUSALITY**, não prova de igualdade binária do corpo de cada método.
- **Barra por provider — inventário Magic Books: 9/9 = 100%**; **barra por provider — fichas com aprofundamento causal source-pinned nesta tranche: 9/9 = 100%**. **Adapters RPG homologados neste trabalho: nenhum**; não converter documentação em alteração de perks.
- **Barra global — —%**: ledger de identidade semântica registra **mínimo 1.856 (1.854 escopo estrito)**, com denominador global ainda aberto. Não somar os nove livros novamente: `NEW_SEMANTIC_ROOTS=0` nesta tranche. O catálogo dos Magic Books não é auditoria de todas as habilidades de mobs do modpack.
- Ownership: Companions!/KnightLib governam livros, projéteis, cooldowns, AI Soul Mage e settlement; RPG Skill Tree só progressão/atributos/Mastery/perks/gates via boundary real; Black Arcana exclusivamente seu runtime mágico/WorldEffectPolicy. Nada aqui transfere ownership de dano ou WorldEffectPolicy a terceiros.

## Fichas individuais auditadas

| ID físico `companions:book_*` | Ficha técnica | Geometria / efeito / causalidade | Situação de mutação |
|---|---|---|---|
| `ice_shard` | [Ice Shard](magic-books/ice-shard.md) | Big shard após 25 ticks cria até 5 small shards; alvos/homing, `indirectMagic`, freeze após tentativa de `hurt`. | `CONFIG_NATIVE` dano e freeze globais; `SEM_HOOK_SEGURO` geometria, homing e fan-out |
| `ice_tornado` | [Ice Tornado](magic-books/ice-tornado.md) | Um tornado com trajetória paramétrica, push e dano por tick a entidades na AABB ampliada. | `CONFIG_NATIVE` dano global; `SEM_HOOK_SEGURO` trajetória/target/hitbox |
| `fire_mark` | [Fire Mark](magic-books/fire-mark.md) | Raycast em blocos até 50, fallback no jogador; anel AABB, status FIRE_MARK em entidades elegíveis. | `CONFIG_NATIVE` raio/cooldown globais; `SEM_HOOK_SEGURO` re-target/tempo |
| `heal_ring` | [Heal Ring](magic-books/heal-ring.md) | Um anel, uma rodada local de efeito em AABB do dono; cura ou `indirectMagic` em entidades heal-inverted. | `CONFIG_NATIVE` cura/cooldown globais; `SEM_HOOK_SEGURO` pulses/alvos |
| `stone_spikes` | [Stone Spikes](magic-books/stone-spikes.md) | 10+3+3 spawns tentados em três fileiras; atraso por índice, varredura vertical, múltiplas tentativas de dano e POISON. | `CONFIG_NATIVE` dano global; `SEM_HOOK_SEGURO` geometria/quantidade/ticks |
| `brace` | [Brace](magic-books/brace.md) | Projétil ricocheteia entre entidades e blocos; no máximo 5 entity hits por cache local, fogo e dano `indirectMagic`. | `CONFIG_NATIVE` dano/cooldown globais; `SEM_HOOK_SEGURO` bounce e tipo |
| `magic_ray` | [Magic Ray](magic-books/magic-ray.md) | Até 30 peças de feixe; circle imediata, outras scheduladas após 3 ticks; primeira LivingEntity em cada AABB/segmento/tick. | `CONFIG_NATIVE` dano/cooldown; `SEM_HOOK_SEGURO` range/AOE/tempo |
| `black_hole` | [Black Hole](magic-books/black-hole.md) | Projétil com gravidade, trava e atração por curva quadrática; AABB com default raio 12 e força 1,45, **sem `hurt` local**. | `CONFIG_NATIVE` parâmetros globais; `SEM_HOOK_SEGURO` per-player |
| `naginata` | [Naginata](magic-books/naginata.md) | Raycast 80; 6 projéteis normal vs 2 crouch, spread/speed distinto, `dealtDamage` antes de tentativa de `hurt`. | `CONFIG_NATIVE` dano/cooldown; `SEM_HOOK_SEGURO` targeting/spawn |

**Definição de status:** `CONFIG_NATIVE` indica configuração provider global documentada e **não** setter por personagem. `SEM_HOOK_SEGURO` significa que não foi comprovado seam apropriado para per-caster mutation; **fail-closed**, sem inventar mixins/hook/event bus. A ausência de `hurt` em uma classe não prova ausência de efeitos causais externos.

## Alertas transversais priorizados

1. **Sidedness:** `FireMarkBook` e `StoneSpikesBook` invocam spawn/scheduler fora do guard server-only em seus corpos; `HealRingProjectile`, `TornadoProjectile` e `StoneSpikeProjectile` manipulam vida, movimento/status sem um guard server-only explícito nos trechos examinados. Isso **não comprova duplicação em servidor**; exige inspeção do caminho KnightLib e cliente.
2. **Dano confirmado vs tentativa:** `MagicRayPieceProjectile` chama `hurt` a cada tick elegível; `SmallIceShardProjectile` adiciona frozen ticks mesmo sem inspecionar o retorno de `hurt`; `StoneSpikeProjectile` e `BraceProjectile` podem adicionar POISON/fire após a tentativa, sem gate de sucesso local. Perks on-hit/Mastery exigem settlement observado por alvo e deduplicação por cast pai.
3. **Alcance e performance:** Magic Ray até 30 peças com AABB por tick; Stone Spikes até 16 varreduras verticais e scheduler; Tornado/Black Hole varrem entidades periodicamente; Naginata lança até 6 projéteis e pode selecionar entidade antes de avaliar block LOS. Caps da API host, proteção/claims, efeitos de mundo e PvP precisam de QA.
4. **Balanceamento configurável:** `hasFullSetOn` conta peças equipadas (apesar do nome) e cada livro reduz cooldown via `pieces × MAGE_SET_COOLDOWN_REDUCTION` (default 0,15). `player.getCooldowns().addCooldown` não comprova gate de cooldown per-caster no runtime de outros callers; não alterar cooldown da Mage armor por cópia do próprio cast.
5. **AI e multiplayer:** Soul Mage reutiliza os nove `AbstractMagicBook` e não duplica objetos mágicos; custo real, skill XP, owner, team, DeathEvent/reconnect, reload, target desaparecido e efeitos PvP exigem cenários de QA. `KnightLib` pode modificar scheduler/lifetime, ainda não homologado nesta pesquisa.

## Aceitação técnica antes de implementações RPG

**PENDENTE:** confrontar esses métodos com o JAR físico exato 1.3.4 e KnightLib 2.0.1; realizar servidor dedicated + cliente conectado; capturar dano/cura efetivos, cooldowns, lançamento, custos, PvP, claims e side effects; testar save/restart, chunk unload, presença de Soul Mage e colaboração com mods do pack. Em cada perk pretendida, exigir método/evento/assinatura/fase realmente inspecionados e teste determinístico com opt-out; documentar `SEM_HOOK_SEGURO` até aprovação. Nenhum valor default substitui a configuração implantada.

## Próxima prioridade

Provider Companions! fica **✅ catalogado por identidade 9/9** e **🟡 em engenharia/validação funcional**. O próximo gate é prova provider-loaded dos casos de sidedness e atribuição de efeitos, não um aumento artificial de porcentagem global. Este checkpoint não promove Stage 06.05 nem Stage 09, não cria spells e não faz runtime merge.
