# Somake Spells 1.0.9 — Blood Cut: métodos e cadeia de dano compilada

**Evidência:** ✅ SHA-EXACT (classe/método/símbolos), ⚠️ causalidade parcial e host runtime NÃO VERIFICADO, ⛔ nenhuma mutação por perk homologada. Java 21 [#39546058075](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39546058075) **SUCCESS**: 16 testes sintéticos (7 legados + 9 novos), JAR SHA-1 físico/publisher verificado, 2 classfiles.

## Identidade física / escopo

- Registry `somakespells:blood_cut`, uma das 83 identidades exatas do Somake 1.0.9.
- `somakespells-1.0.9-1.21.1.jar`, CurseForge File `8867079`, SHA-1 `171841ac9f802be9309ecc166c1d972ac6d404c0`.
- Spelling confirmado por leitura de classfile, sem supor a FQCN: `com.somake.somakespells.spells.blood.BloodCutSpell` (**7 métodos focalizados**) e `com.somake.somakespells.effect.blood.BloodCutEffect` (**2 métodos focalizados**).
- Provas limitadas à inspeção de descritores e referências JVM com `javap`. Os métodos do efeito têm **5** branches em `onLivingDamage` e **2** em `getDamageModifier`; estes fluxos condicionais não foram decompostos para estabelecer tabela verdade.

## Mapa de classes e chamadas reais

| Classe / assinatura relevante | Símbolos JVM certificados | Informação utilizável / limite |
|---|---|---|
| `BloodCutSpell.getCastType():CastType` | `CastType.INSTANT` | A classe retorna a modalidade de cast por constante referenciada; duração efetiva e settlement não medidos |
| `BloodCutSpell.onCast(Level,int,LivingEntity,CastSource,MagicData):void` | `getSpellPower`, `ModMobEffects.BLOOD_CUT`, construtor `MobEffectInstance`, `LivingEntity.addEffect` e `AbstractSpell.onCast` | Caminho de aplicação nominal de efeito, sem inferir receptor, duração, amplifier, sucesso nem custo |
| `BloodCutSpell.getDamageSource(Entity,Entity):SpellDamageSource` | `AbstractSpell.getDamageSource`, `SpellDamageSource.setLifestealPercent(float)` | Ajuste de parâmetro de lifesteal identificado; valor, origem e recebimento de cura NÃO comprovados |
| `BloodCutSpell.getUniqueInfo(int,LivingEntity):List` | `BloodCutEffect.getDamageModifier`, `getSpellPower`, `Utils.timeFromTicks`, `Utils.stringTruncation` | Referências informativas/scaling, sem fórmula numérica comprovada |
| `BloodCutSpell.getDefaultConfig():DefaultConfig` / `getSpellResource():ResourceLocation` | Campos `defaultConfig` e `spellId` | Identidade e config simbólicas; valores efetivos não extraídos |
| `BloodCutSpell.getCastStartAnimation():AnimationHolder` | `SpellAnimations.SELF_CAST_ANIMATION` | Apresentação do cast; animação não prova geometria ou alvo |
| `BloodCutEffect.onLivingDamage(LivingDamageEvent.Post):void` | `event.getSource/getNewDamage/getEntity`, `DamageSource.getEntity`, `LivingEntity.getEffect`, `MobEffectInstance.getAmplifier`, `getDamageModifier`, `ModSpells.BLOOD_CUT`, `BloodCutSpell.getDamageSource`, `DamageSources.applyDamage`, `LivingEntity.invulnerableTime`, `BloodSlashParticleOptions` / `MagicManager.spawnParticles` | Caminho *potencial* de resposta a dano e aplicação secundária, com cinco branches; não afirmar resultado de proc, filtro do próprio Blood Cut, invulnerabilidade, dano efetivo ou listener registrado |
| `BloodCutEffect.getDamageModifier(int,LivingEntity):float` | `ModSpells.BLOOD_CUT`, `BloodCutSpell.getEntityPowerMultiplier` | Fórmula e ceiling ainda dependem da auditoria do fluxo de dois branches |

## Engenharia de perks, targeting e recursos

| Eixo | Situação demonstrável |
|---|---|
| Cast | ✅ `CastType.INSTANT`; `onCast` referencia a criação de `MobEffectInstance` |
| Targeting e LOS | ⚠️ Receptor de `addEffect`, distância, linha de visão, host target gate e filtros de equipe não reconstruídos |
| Tipo de ação | ⚠️ Buff/debuff `BLOOD_CUT` com evento posterior de dano possível; receptor e acionamento efetivo desconhecidos |
| Dano, lifesteal e tipo | ⚠️ Referências a `getNewDamage`, `getDamageModifier`, `applyDamage`, `setLifestealPercent`; nenhum multiplicador numérico, `DamageType` ou cura aplicada comprovado |
| Geometria / projéteis | ⚠️ Efeito visual de partículas referenciado; raio, cone, projétil, hitbox, velocidade, distância e world-effects desconhecidos |
| Tempo | ⚠️ `Utils.timeFromTicks` referenciado; duração exata, tick e cooldown desconhecidos |
| Multiplicidade | ⚠️ Branches, recast, evento registrado, causalidade/proc-count por vítima e prevenção de recursão não comprovados |
| Custo e progressão | ⚠️ Config efetiva Iron's, mana, cooldown, mastery e aquisição Survival requerem exame próprio |
| Possibilidade de mutação por perks | ⛔ `FAIL_CLOSED`: assinatura/constante ou chamada do evento não implica hook público mutador por caster |

**Risco causal prioritário:** `BloodCutEffect.onLivingDamage` referencia um evento `Post` e `DamageSources.applyDamage` dentro da mesma rotina. Não deduzir recursão nem proteção antirrecursão: auditar condições, registro do listener e tag/fonte do dano secundário antes de qualquer perk que amplie dano, adicione projéteis ou conceda Mastery. Uma perk não deve aplicar segundo dano ou cobrar recursos novamente para o mesmo evento sem contrato canônico.

## Reprodutibilidade e limites

O [verificador](../../../../../docs/qa/somake_109_blood_cut_refs.py), seus [testes](../../../../../docs/qa/somake_109_blood_cut_refs_test.py) e o [workflow](../../../../../.github/workflows/somake-109-blood-cut-refs.yml) conferem hash, mod ID, unicidade dos dois classfiles, descritores e símbolos. A evidência exportada é JSON derivado; JAR/bytecode proprietário não é versionado.

**Próxima auditoria física:** registrar inscrição do `onLivingDamage` no event bus; extrair fluxo de branches e os operandos de `getDamageModifier`/lifesteal; vincular dano original ao dano secundário, caster/vítima e condição de reaplicação; conferir host 3.16.3 e testes em dedicated server/client. Isto não substitui QA de Survival nem cria uma nova raiz semântica.

**Autoridades:** Somake produz efeito e regras específicas; Iron's mantém casting, custo e cooldown; RPG Skill Tree só fornece progressão e perks por contrato real; Black Arcana não reimplementa esse pipeline.

**Outras fontes:** [registry física](../EXACT-1.0.9-REGISTRY-AUDIT.md), [lista 1.0.9](../SPELL-CATALOG-1.0.9.md), [padrão editorial](../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
