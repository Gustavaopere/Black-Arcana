# Hexalia 1.3.7 — delta técnico de Bloodlust, Spikeskin e Siphon

**Escopo:** três brews **já inventariados**, sem adicionar receitas, magias, IDs ou numeradores. Análise documental de interoperabilidade *clean-room*, em 27/10/2026. **Estado ⚠️ source release-pinned; QA do JAR e do jogador não executado**.

## Autoridades e limite da prova

- **JAR reportado na modlist física do catálogo:** `hexalia-neoforge-1.3.7.jar`, mod ID `hexalia`, Minecraft 1.21.1/NeoForge, SHA-1 `ca90edf1664cf6d44fe7e5318c71069050499c7e`. Esta rodada **não abriu o JAR instalado**.
- **Fonte 1.3.7 correlacionada à release:** `AstralyaStudios/Hexalia@98c22aaf70e069c616fed5ad2dc56d2b37fcd283` ([commit](https://github.com/AstralyaStudios/Hexalia/commit/98c22aaf70e069c616fed5ad2dc56d2b37fcd283)); versionamento documentado no [README do provider](../README.md). A igualdade byte a byte source↔JAR 1.3.7 **não é demonstrada**.
- **Fonte de comparação 1.3.6:** `AstralyaStudios/Hexalia@4952c65233bf31e9f0d3e55ff76be7fa1007ee3d` ([commit](https://github.com/AstralyaStudios/Hexalia/commit/4952c65233bf31e9f0d3e55ff76be7fa1007ee3d)). O recorte histórico 1.3.6 das fichas individuais permanece válido **apenas para aquela versão**.
- O commit de manutenção 1.3.7 posterior ao pin da release não foi usado para inferir comportamento do JAR instalado.

## Diferença confirmada em `ModMobEffects`

Comparação direta dos arquivos `ModMobEffects.java` 1.3.6 vs 1.3.7, sem extrapolar valores *effective* de `AttributeInstance`:

| Effect e atributo | 1.3.6: amount declarado | 1.3.7: amount declarado | Operation | Leitura permitida |
|---|---:|---:|---|---|
| `hexalia:bloodlust` → `ATTACK_DAMAGE` | `0.0F` | **`3.0F`** | `ADD_VALUE` | o registro de atributo mudou; dano final de ataque não foi medido |
| `hexalia:spikeskin` → `ARMOR` | `0.0F` | **`3.0F`** | `ADD_VALUE` | o registro de atributo mudou; armor efetivo não medido |
| `hexalia:spikeskin` → `MOVEMENT_SPEED` | `-0.10F` | `-0.10F` | `ADD_MULTIPLIED_TOTAL` | operação e amount do template são estáveis; aplicação runtime pendente |
| `hexalia:siphon` → `ATTACK_SPEED` | `+0.4F` | `+0.4F` | `ADD_VALUE` | sem alteração no registro desse atributo |

**Fontes localizadas:** [registro 1.3.6](https://github.com/AstralyaStudios/Hexalia/blob/4952c65233bf31e9f0d3e55ff76be7fa1007ee3d/common/src/main/java/net/astralya/hexalia/effect/ModMobEffects.java) e [registro 1.3.7 linhas 50–86](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/effect/ModMobEffects.java#L50-L86). A alteração do `amount` de `0` para `3` em **Bloodlust e Spikeskin** invalida descrições do registro 1.3.6 se apresentadas como sendo da instalação 1.3.7.

## Consumidores e riscos reais para perks

**Bloodlust.** O corpo da classe [`BloodlustEffect` 1.3.7](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/effect/custom/BloodlustEffect.java#L11-L36) é textualmente idêntico ao de 1.3.6: em cada oportunidade de tick remove efeitos ativos cujo *path* de registry contém `regeneration`. Seu parâmetro de construção `3.0D` não é usado pela classe, mas **o valor registrado de ATTACK_DAMAGE agora é `3.0F`** — canais diferentes. O método não contém `heal` nem processamento de dano ofensivo; **isso não basta para provar ausência de um consumidor separado de lifesteal em todo o mod**. Registrar lifesteal como **NÃO COMPROVADO**. Não sintetizar autocura externa.

**Spikeskin.** A classe [`SpikeskinEffect` 1.3.7](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/effect/custom/SpikeskinEffect.java#L7-L18) também é textualmente igual à de 1.3.6: define `adjustModifierAmount(amplifier, modifier)` com retorno `3.0 * (amplifier + 1)` **sem distinguir qual atributo/modifier recebeu**. Isso coexiste com dois *templates* distintos, `ARMOR ADD_VALUE +3.0` e `MOVEMENT_SPEED ADD_MULTIPLIED_TOTAL -0.10`. **Não afirmar que a velocidade final corresponde a −10%, nem que o override é aplicado identicamente a ambos, sem seguir/verificar a versão exata da API Minecraft e o `AttributeInstance` efetivo em runtime.** Um possível resultado não-intencional por valor sobrescrito exige teste. Nenhum handler de reflexão de dano foi demonstrado por esta auditoria; não criar dano reflexivo via adapter.

**Siphon.** A implementação [`SiphonEffect` 1.3.7](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/effect/custom/SiphonEffect.java#L14-L64) é textualmente igual à de 1.3.6: consulta `HexaliaConfig.siphonRadius()+amplifier`, busca `ItemEntity` na AABB expandida por tick somente para Player não agachado, chama `item.playerTouch(player)` com slot disponível e, no caminho de inventário cheio, movimenta o **primeiro** item encontrado antes de retornar. `getFreeSlot() == -1` não é sinônimo de impossibilidade de *stacking* com todos os itens. O campo `SIPHON ATTACK_SPEED +0.4 ADD_VALUE` permanece declarado [no registry](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/effect/ModMobEffects.java#L77-L86). Não transformar *pickup* ou loop per-tick em cast/XP/Mastery.

## Receita, item, duração e configuração

- Os três JSONs de receita `brew_of_bloodlust_from_small_cauldron`, `brew_of_spikeskin_from_small_cauldron` e `brew_of_siphon_from_small_cauldron` foram comparados nos dois commits e se mostraram **textualmente idênticos**. Cada receita usa tipo `hexalia:small_cauldron`, `duration=4800` e mantém os quatro ingredientes já documentados nas fichas históricas: [Bloodlust](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/hexalia/recipe/brew_of_bloodlust_from_small_cauldron.json), [Spikeskin](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/hexalia/recipe/brew_of_spikeskin_from_small_cauldron.json), [Siphon](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/generated/resources/data/hexalia/recipe/brew_of_siphon_from_small_cauldron.json).
- [`ModItems` 1.3.7 linhas 391–433](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/ModItems.java#L391-L433) instancia os três `BrewItem` com `durationTicks=20*240` e `amplifier=0`; [`BrewItem` 1.3.7](https://github.com/AstralyaStudios/Hexalia/blob/98c22aaf70e069c616fed5ad2dc56d2b37fcd283/common/src/main/java/net/astralya/hexalia/item/custom/BrewItem.java#L18-L53) calcula duração com `1.5` apenas para set Moonweave completo, no servidor. Duração **base 4.800 ticks** e **com set completo 7.200 ticks** são parâmetros de criação do efeito, **não comprovação de duração efetiva no player** (hooks, imunidades, substituições e config final não testados).
- Não houve leitura da configuração efetivamente instalada nem do resultado real de equipar/desequipar os atributos. Valores declarados em source não autorizam alterar parâmetros de Hexalia por perks per-player.

## Matriz de aceitação

| Gate | Status | Observação |
|---|---|---|
| Contagem de três brews | ✅ já inventariados | +0 IDs, +0 certificações |
| Source 1.3.7 vs 1.3.6 em effect/registry/recipes | ✅ evidência documental verificada | Somente arquivos listados, não varredura exaustiva do repo |
| Registro exato 1.3.7 no classfile instalado | ⛔ não testado | Hash do JAR registrado; equivalência de bytecode pendente |
| Spikeskin `adjustModifierAmount` vs armor/speed efetivos | ⛔ não testado | Verificar API, amplificadores, extensão, remoção de efeito/relogin |
| Bloodlust lifesteal + ataque efetivo | ⚠️/⛔ | ATTACK_DAMAGE declarado +3; heal/settlement externo não provado |
| Siphon pickup/attraction e mining/exhaustion efetivos | ⚠️/⛔ | Admissão item por tick source-pinned; mineração/exaustão sem consumidor aqui |
| Perk mutadora / double settlement / claims | ⛔ fail-closed | Hexalia permanece autoridade da consumação e do efeito; RPG Skill Tree controla perks/Mastery |

**Resultado:** correção de versões de três fichas e análise de risco, sem permissão para adicionar atributo, refletir dano, inventar cura, multiplicar procs ou modificar mundo por bridge. **Hexalia permanece 0/38** no índice perk-ready observado; catálogo global **138/2075** e providers integrais **0/164** são checkpoints lidos da `main@87e8c090ec5fc18a018d854cc608ebe43a4cf4fc`, e não numeradores de objetos completamente auditados. Stage 06.05 e QA físico permanecem independentes.
