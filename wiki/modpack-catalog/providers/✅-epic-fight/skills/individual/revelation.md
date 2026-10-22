# Revelation

## Ficha individual para engenharia de perks — 21/10/2026

**Descrição para o jogador (resumo original):** Acumula estado contra um alvo por bloqueios, aparos e esquivas.

### Identidade, versão e origem por campo

- **ID exato:** `epicfight:revelation`; campo de registry `REVELATION`. Categoria/disposição: [registro completo](../SKILL-DISPOSITION-21.17.3.1.md). `EXCLUDED` somente da métrica de magia; continua no catálogo técnico de perks.
- **Runtime físico registrado:** Epic Fight `21.17.3.1`, Minecraft `1.21.1`, NeoForge do pack `21.1.250`; arquivo `epic-fight-21.17.3.1-mc1.21.1-neoforge.jar`.
- **JAR publisher conferido nesta rodada:** SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0`; SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526`; 8.578.288 bytes. A equivalência é ao hash registrado na modlist; não houve leitura da instalação ao vivo.
- **Modlist consultada:** `Gustavaopere/neoforge-rpg-skilltree@ed5b65b890767b406ce41127bcb793775263c7bd`, dossiê `✅-epic-fight v21.17.3.1.md`.
- **Dados empacotados:** `data/epicfight/skill_parameters/revelation.json`, lido diretamente do ZIP SHA-exato; config implantada NÃO VERIFICADA.
- **Implementação comparativa:** [`yesman.epicfight.skill.identity.RevelationSkill`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/identity/RevelationSkill.java); fonte `a78aa24b72e90a9d09f5fd61925e4369d117abaf` declara **21.17.3**, versão adjacente. Equivalência integral de métodos com **21.17.3.1 NÃO VERIFICADA**.
- **Registro na fonte comparativa:** [`EpicFightSkills.REVELATION`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/registry/entries/EpicFightSkills.java#L147); identidade binária tem prova própria, não deriva apenas dessa linha.
- **Estado técnico:** ⚠️ `EXACT_PACKAGED_PARAMETERS + SOURCE_ADJACENT_CAUSALITY`; ⛔ mutação externa por perks sem contrato validado; gameplay/Survival **PENDING**. Casos binários posteriores já registrados nesta ficha/dossiê prevalecem apenas nos campos que verificam.

### Parâmetros do JAR exato

| Campo | Valor e fronteira da evidência |
|---|---|
| `max_duration` | `20` |
| `block_stacks` | `3` |
| `parry_stacks` | `6` |
| `dodge_stacks` | `8` |
| `default_revelation_stacks` | `20` |
| `max_revelations.minecraft:cave_spider` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:drowned` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:enderman` | `30` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:husk` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:iron_golem` | `30` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:piglin` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:piglin_brute` | `20` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:zombified_piglin` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:pillager` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:player` | `30` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:skeleton` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:spider` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:stray` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:vindicator` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:wither_skeleton` | `20` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:zombie` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.minecraft:zombie_villager` | `10` (dado serializado; resolução efetiva pendente). |
| `max_revelations.epicfight:wither_skeleton_minion` | `10` (dado serializado; resolução efetiva pendente). |

**Unidades:** `consumption` é um número no recurso do provider, não automaticamente mana, stamina ou segundos. Stacks são contagens. Unidades de tempo, percentuais e geometria só são atribuídas abaixo quando o consumidor correspondente foi auditado; dados RAW não medem o valor final do jogador.

### Código e pipeline causal

- [`public void loadDatapackParameters(CompoundTag parameters)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/identity/RevelationSkill.java#L75) — declaração na fonte **21.17.3 adjacente**.
- [`public void onInitiate(SkillContainer skillContainer, EntityEventListener eventListener)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/identity/RevelationSkill.java#L98) — declaração na fonte **21.17.3 adjacente**.
- [`public void executeOnServer(SkillContainer container, CompoundTag arguments)`](https://github.com/Antikythera-Studios/epicfight/blob/a78aa24b72e90a9d09f5fd61925e4369d117abaf/src/main/java/yesman/epicfight/skill/identity/RevelationSkill.java#L172) — declaração na fonte **21.17.3 adjacente**.

**Fluxo na fonte adjacente, salvo prova binária específica já vinculada:** RevelationSkill carrega limites por entidade com EntityType.byString; target novo zera stacks. ON_DODGE/TAKE_DAMAGE_INCOME BLOCKED credita stacks conforme source/target. Ao limiar ativa maxDuration e limpa stacks. CAST_SKILL pode encaminhar solicitação nativa de innate; não é segunda magia.

**Análise detalhada:** [dossiê causal de origem](../technical/REVELATION-21.17.3-SOURCE-ADJACENT.md). A existência de classe/método/evento ou configuração não autoriza automaticamente escrita por perk.

**Contratos existentes no sibling:** [RPG Skill Tree `main@ed5b65b`](../RPG-SIBLING-BOUNDARIES-ed5b65b.md) já contém modificação de custo via `CONSUME_SKILL`/`setAmount` quando o recurso do evento é `STAMINA`, além de observadores de dodge e damage para progressão. Pendências desta ficha referem-se a novos mutadores/validação por campo e não negam esse runtime já presente. Não duplicar desconto, débito ou Mastery.

### Matriz de campos para integração

| Eixo | Valor, consumidor e limite conhecido | Viabilidade atual |
|---|---|---|
| Dano / tipo | N/A — stacks não são dano numérico. | `CONTRATO_CONDICIONAL`; conversão de DamageType: `SEM_HOOK_SEGURO`. |
| Alcance / LOS | Alvo rastreado/directEntity; 18 limites por EntityType empacotados. | `NÃO_VERIFICADO` para extensão por jogador/perk. |
| Alvo / área / máximo de alvos | Alvo rastreado/directEntity; 18 limites por EntityType empacotados. Seleção, dano e colisão são eixos distintos. | `SEM_HOOK_SEGURO` para single→AOE/retarget externo. |
| Projétil / hitbox / escala / velocidade | N/A no fluxo próprio auditado; não há projétil ofensivo independente identificado nesta skill. | `SEM_HOOK_SEGURO` para aumentar hitbox/escala externa. |
| Tempo / duração / cast / cooldown | max_duration=20 ticks empacotado; não cast time. | `CONFIG_NATIVE` apenas para campos JSON existentes; mutação per-player não homologada. |
| Custos / recursos / refunds | Recurso e ordem de consumo descritos no pipeline; consumption isolado não identifica stamina/mana/segundos. | [`HOOK_VERIFICADO` no código sibling](../RPG-SIBLING-BOUNDARIES-ed5b65b.md) somente para evento com `Resource.STAMINA`; demais recursos e composição final condicionados. Respeitar cancelamento/consumer. |
| Status / summons / mundo | Efeitos e estados descritos no pipeline/dossiê; alcance de bloco, claims/PvP e rollback efetivos NÃO VERIFICADOS. | Sem replay externo de efeito; proteção do provider e WorldEffectPolicy do Black Arcana preservadas. |
| Scaling / caps / causalidade | Coeficientes/stacks/limites acima pertencem aos consumidores documentados; VFX, fase, proc ou callback não criam novo root. | `SEM_HOOK_SEGURO` para award/alteração sem correlação e deduplicação. |

### Autoridades e verificação restante

- **Epic Fight:** skill/combat state, animações, stamina/gauge, target/hits e settlement. Não cobrar recurso, gerar dano ou executar ação outra vez.
- **RPG Skill Tree:** progressão, atributos, Mastery e perks/gates por contrato real; evento preflight, input, FX e simples tentativa não comprovam resultado.
- **Black Arcana:** seu casting/rituais/domains, hazards/Strain/Corruption, persistência e world safety. **Enshrouded:** seu Shroud/exposure; afinidade temática não cria bridge.
- **QA pendente:** método/ABI/campos não certificados no JAR, configuração final, order/side/cancelamento, player conectado, equip/unequip, reload/relog/respawn, multiplayer, claims/PvP e provider no modpack. Stage 06.05/09 não avança por esta ficha.
- **Provas correlatas:** [parâmetros binários](../../EXACT-BINARY-PERK-PARAMETERS-21.17.3.1.md), [checkpoint técnico com QA posterior](../PERK-TECHNICAL-CHECKPOINT-2026-10-16.md), [índice individual](../INDIVIDUAL-SKILL-CARDS-21.17.3.1.md).
