# Augere — Principle / sistema de progressão

**Provider:** Ypsilon's Fundamentalism / Fundamental Principles (`ypfundamentals`) · **tipo:** categoria/passiva, não spell registrado · **enum:** `AUGERE` · **chave técnica:** `usesPotentiation`. Não inventar `ypfundamentals:augere` como registry ID de magia: a chave de categoria é string do ledger. **+0 identidades mágicas.**

Acrescenta valor ao helper de dano de arma usado por spells e participa dos gates de Reinforcement; não soma diretamente a todo dano físico.

## Autoridade e evidência

JAR do inventário físico versionado: `ypfundamentals-1.1.7.1.jar`, SHA-1 `a2855c253202a8fcc2925fcf5b1bf86d64fbe4da`, modlist RPG #575. [Prova binária histórica dos 15 spells](../EXACT-BINARY-SPELLS-1.1.7.1.md) não valida os métodos da passiva. Esta ficha é `SOURCE_PARAMETERS / SOURCE_CAUSALITY`, pin oficial [a9b8f8222fb2a800edece8c1568984bd2a764fc2](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/gradle.properties#L33), Minecraft 1.21.1/Java21/NeoForge; source declara dependência de Iron's `1.21.1-3.16.2`, pack usa `3.16.3`. Config efetiva e aplicação dos mixins no JAR instalado **NÃO VERIFICADO**. Reauditoria documental: 22/10/2026.

## Matriz para perks

`l` é nível deste Principle, salvo quando explicitado outro; faixa normal de setLevel: 0–20. Defaults abaixo são de ServerConfig no source, não leitura da config implantada. `NATIVE` designa passiva/config já existente; `CONDITIONAL` exige versão, owner, fase e coexistência; `SEM_HOOK_SEGURO` registra ausência de seam externo demonstrado neste escopo, não impossibilidade universal.

| Eixo | Fórmula, fase e limites | Mutabilidade para integração |
|---|---|---|
| Dano / fórmula | Δ=l×addDamagePts, default 0,5l →0–10. Inject RETURN cancellable em Utils#getWeaponDamage; se original>0, entity instanceof Player e flags ativas, devolve original+Δ. Não é hurt e não troca DamageType. | NATIVE: parâmetro de helper; dano final depende da fórmula individual que o consome. |
| Fase / alvo | Callback não exige ServerPlayer nem guard explícito de lado; leitura do nível depende do manager (attachment server / dados client). Não consulta usesPotentiation por ID dentro do mixin. | CONDITIONAL: validar ambos lados e consumidor real; não chamar API de dano genérico. |
| Reinforcement / tempo | setLevel de Augere dispara Technique Reinforcement tiers: 5–9→2;10–14→3;15–19→4;20→5. Esse switch não implementa por si só mitigação/consumo de mana de Reinforcement. | SEM_HOOK_SEGURO para duplicar armor/escudo, tick ou recurso por analogia com unlock. |
| Outros eixos | Nenhum novo intent de cast, projétil, summon ou alteração de DamageType é criado pela identidade de Principle. Range, target/área, hitbox, duração e dano não descritos acima continuam provider-owned; campo não auditado = NÃO VERIFICADO, não setter presumido. | SEM_HOOK_SEGURO para transplantar modificações entre providers. |

**Origem dos valores:** [Util helper](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Util.java#L217) · [ServerConfig defaults](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/ServerConfig.java#L321).

## Pipeline e consumidores

Spell solicita Utils.getWeaponDamage → retorno positivo e Player elegível → +Δ → fórmula do spell continua nativa. Um valor maior no helper pode afetar diversos spells/campos sem garantir HP entregue. Trigger de technique é efeito de progressão distinto de acerto e não concede Mastery externo automaticamente.

**Símbolos exatos:** [AugereMixin#modifyAugerePotentiation](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/AugereMixin.java#L21) · [PrinciplesLevelsAttachment Augere gate](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L109).

## Progressão, power e deduplicação

A classificação por ASM é uma heurística do provider para o registry global, não prova de alvo/dano efetivo de cada spell. `SpellNerfCast(SpellOnCastEvent)` executa em ServerPlayer, concede XP às categorias retornadas quando PRINCIPLES_SYSTEM está ativo e CastSource é diferente de SCROLL. Não há filtro explícito de creative/spectator ou token pai/filho nesse trecho; não importar a elegibilidade de Mastery do RPG como se fosse do Ypsilon. `calculateXpFromSpell` depende de raridade e CONTINUOUS, depois multiplica principleXpMultiplier. O attachment inicializa em 0, setLevel limita 0–20, e custo de `n→n+1` usa `(int)(20+20×1,3^(n+1))` (primeiro 0→1 = 46), não 40. Persistência/sync e verificação de funcionamento estão no [contrato comum](README.md).

`PowerSpellsMixin` também altera getSpellPower para Player: soma um termo `Pbase×(basePower+levelAddition×nívelCategoria)` por categoria; as subcategorias usesShoot/createsAoeEntities/usesSummon/usesTargeting recebem metade se configurado. Depois multiplica pela razão de fatigue quando ativa. Defaults −0,10 e +0,01; não é substituição de P por apenas esse termo. A ativação de cada passiva não é checada individualmente nesse loop de power. Esse efeito compartilhado pode influenciar os demais campos do spell que consumam P e não é novo dano terminal.

**Referências comuns:** [enum dos 13 Principles](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/util/Principles.java#L3) · [nome técnico](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/PrinciplesProgressionManager.java#L165) · [setLevel/clamp](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/attachments/customAtt/PrinciplesLevelsAttachment.java#L88) · [XP/cast event](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/event/ModEvents.java#L567) · [power compartilhado](https://github.com/ypsilonM/FundamentalPrinciples-1.21.1/blob/a9b8f8222fb2a800edece8c1568984bd2a764fc2/src/main/java/com/ypsi/fundamentalism/mixins/principlesMixins/PowerSpellsMixin.java#L35).

RPG Skill Tree continua authority de seus atributos/perks/Mastery; Ypsilon mantém seu ledger, categorias, fatigue e efeitos. Black Arcana mantém seu runtime mágico/world safety; Enshrouded mantém Shroud/exposure. Não escrever attachment do provider, aplicar novamente sua passiva nem conceder XP paralelo sem contrato de integração comprovado. Mixin privado é localizador de comportamento, não API pública de perk.

## QA e próximos testes

Testar helper com original 0/positivo, armas/enchantments, cliente/servidor, níveis 0/20 e spell que usa o helper múltiplas vezes; distinguir valor base, damage source e dano terminal. Validar Reinforcement separadamente.

Estado: **source examinado; runtime/config/cliente/Survival/modpack PENDING**. Nenhum adapter/perk, cópia de código/assets ou promoção de Stage. Descrição é resumo original do código consultado; links servem para inspeção, não incorporam implementação. [Índice e licença](README.md).
