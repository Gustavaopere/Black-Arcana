# hunger steal — Ace's Spell Utils 1.2.7.2

**ID de atributo:** `aces_spell_utils:hunger_steal` · **Tipo:** `RangedAttribute` · **Status:** ⚠️ source-pinned / integração física e certificação de perk pendentes.

## Registro e parâmetros

- Default: `0`; mínimo do registro: `-100`; máximo: `100`; `setSyncable(true)`.
- Registrado em `ASAttributeRegistry` por `DeferredRegister<Attribute>`; adicionado a todos os entity types enumerados em `EntityAttributeModificationEvent`.
- [Fonte do registro e atributos, release pinada](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/registries/ASAttributeRegistry.java#L22-L106).
- Versão do provider: `1.2.7.2-1.21.1`. Artefato da modlist anotado: `aces_spell_utils-1.2.7.2-1.21.1.jar`, SHA-1 `8cbcd535a0b19bef49504c0b5ecafcbcd1cb1cca` (não confrontado com o source/JAR nesta tranche).

## Consumidor, causalidade, targeting e fórmula

**Consumidor do source:** `hungerStealEvent · LivingDamageEvent.Pre · L321–363`.

Requer directEntity como `ServerPlayer`, ataque com `getAttackStrengthScale(0)>=1` e atributo >0. Define fome do atacante como `int(clamp(foodLevel+attr,0,20))`. Se vítima é `Player`, define fome da vítima como `int(clamp(targetFoodLevel-attr,0,20))`.

A unidade é **ponto de fome** (`1=1 ponto`), sem escala pelo dano. Não altera saturação ou exaustão neste handler. Como a segunda conta usa a fome recém-escrita do atacante, H=19 e attr=5 solicitam atacante 20 e vítima 15, podendo aumentar a fome de uma vítima abaixo de 15; H=10 e attr=.5 solicitam atacante 10 e vítima 9. São derivações dos clamps/casts, sem carry de frações, não resultados medidos no pack ([unidade](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L315-L321), [duas escritas](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L345-L361)).

**Targeting / geometria:** Atacante direto em evento de dano `Pre`, vítima se for jogador; não cria dano mágico independente.

**Custo, cooldown, duração e projétil próprios:** não se trata de spell cast ou de registro de `AbstractSpell`. O atributo não define mana/cooldown/range/duração/projectile size autônomos; essas propriedades, quando aplicáveis, pertencem ao dano/cast/entidade de Iron's e/ou ao consumidor. Não interpretar como valor global de Black Arcana.

**Evidência localizada:** [`AcesSpellUtilsServerEvents.java` L316–363](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/events/AcesSpellUtilsServerEvents.java#L316-L363) · [auditoria causal complementar](../SOURCE-1.2.7.2-COMBAT-CAUSALITY-AND-DOUBLE-SETTLEMENT-20261027.md).

## Limitações, interoperabilidade e QA

O valor `targetFoodLevel` é obtido de `playerFood.getFoodLevel()` (atacante **após** a alteração), não de `targetFood.getFoodLevel()`. Assim há risco causal source-level para fome da vítima. Não é prova de efeito visto em servidor.

- Ace's Spell Utils controla o consumidor e o registro de atributo. Iron's é autoridade sobre spells e recursos nativos; Black Arcana preserva casting, segurança de mundo, Strain, Corruption e Arcane Danger; RPG Skill Tree fornece apenas progressão por integração comprovada.
- Build pinado do source usa Iron's `1.21.1-3.16.2`; o host físico informado no catálogo está em `3.16.3`. **Paridade binária e assinatura do hook atual: NOT_VERIFIED**.
- **Validação pendente:** confronto com JAR exato instalado, matriz de eventos com dano original/corrente/final, configuração real, side cliente/servidor, competição com atributos/perks de outros mods; `physical_qa=NOT_TESTED` e `mutating_hook=NOT_VERIFIED`.
- Nenhuma alteração de runtime, registro extra, segunda rolagem de proc ou recompensa Mastery foi autorizada por esta ficha.
