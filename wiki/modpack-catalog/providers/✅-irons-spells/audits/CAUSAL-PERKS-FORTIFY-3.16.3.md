# Iron's 3.16.3 — Fortify: AoE de aliados, MAX_ABSORPTION e lifecycle de HP temporário

**Identidade:** `irons_spellbooks:fortify` · Holy · níveis 1–10 · Iron's 1.21.1-3.16.3. ✅ ID anteriormente catalogado; 🟡 novo aprofundamento causal; ⚠️ código-fonte fixo inspecionado, **sem nova prova classfile/GameTest**; ⛔ mutação de raio, seleção ou absorção sem seam seguro. **+0 objeto semântico.**

**Source pin:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252` · [descrição player-facing](https://iron.wiki/spells/). Ambiente físico documentado: NeoForge 21.1.250 (modlist) / build Black Arcana 21.1.248; fingerprint do JAR do perfil não revalidado. Documento clean-room de interoperabilidade.

## Configuração e geometria

1. `FortifySpell` configura `HOLY_RESOURCE`, `COMMON`, `maxLevel=10`, cooldown-default **180 s**, `CastType.LONG`, castTime **60 ticks**, mana `80 + 10×(level−1)` = **80–170**, spell power nominal `6+(level−1)` = **6–15**. [Fonte de defaults](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/FortifySpell.java#L32-L67).
2. `radius` é constante estática **8**. `onServerPreCast` instancia `TargetedAreaEntity.createTargetAreaEntity(level,caster.position(),8,16239960,caster)` e grava `TargetAreaCastData` se `playerMagicData!=null`. Isso indica superfície de preview/target data, **não comprova** mutabilidade de área por perk nem segundo cast. [Pré-cast](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/FortifySpell.java#L80-L87).
3. `onCast` enumera `LivingEntity` dentro de `AABB(caster.position ±(8,8,8))` e só processa quem satisfaz **ambas**: `Utils.shouldHealEntity(caster,target)` e `caster.distanceTo(target)<=8`. Portanto a AABB é **broad phase cúbica**, enquanto o teste de distância limita os alvos efetivos à geometria radial por distância de entidade; não confundir 8 com tamanho do projétil ou range de mira. **Não há limite explícito de quantidade de alvos nesse método**, apesar da região finita. [Aplicação](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/FortifySpell.java#L89-L99).
4. O helper `shouldHealEntity` inclui self, regras de team/ally/tags e permite players quando o caster é player sem equipe; não generalizar para proteção PvP/claims ou consentimento. [Critérios](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/api/util/Utils.java#L532-L558).

## Efeito e causalidade de absorção

- Cada alvo elegível recebe `MobEffectRegistry.FORTIFY` por `20*120 = 2400 ticks (120 s)`, com amplifier `(int)getSpellPower(level,caster) - 1`. Para potência neutra 6–15, amplifier **5–14**. O cast envia `AbsorptionParticlesPacket` por alvo e `FortifyAreaParticlesPacket` ao redor do caster: ambos são VFX, **não** prova de HP temporário usado ou hits absorvidos. [OnCast](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/holy/FortifySpell.java#L90-L99).
- `FortifyEffect.onEffectStarted` chama `super.onEffectStarted` e depois `livingEntity.setAbsorptionAmount(getAbsorptionAmount()+(amplifier+1))`. O código **soma ao valor existente**; não executa `heal`/`SpellHealEvent` e não mede gasto efetivo de shield. Se uma reaplicação do efeito disparar `onEffectStarted` novamente, há **hipótese de acúmulo** por esse callsite; a frequência real de callbacks (novo efeito, refresh, override, relog) requer prova no servidor. [Callback](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/FortifyEffect.java#L6-L16).
- `MobEffectRegistry.FORTIFY` também registra modificador `Attributes.MAX_ABSORPTION` com `ADD_VALUE`, constante base **1** no registro; **não** inferir o resultado líquido pós-amplifier/modifiers sem a semântica de Minecraft/NeoForge. O provider é authority de ambos os canais de absorção. [Registro](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/MobEffectRegistry.java#L34-L36).
- Como `Utils.shouldHealEntity` também aceita o próprio caster, a intenção é buff de grupo incluindo self quando presente na seleção. O número real de alvos, reaplicações aceitas, proteção consumida ou expirou **não** é comprovado por source/tooltip.

## Controle de perks, bounds e Mastery

| Parâmetro | Evidência | Condição |
|---|---|---|
| Raio de seleção/visual | `radius=8` e `TargetedAreaEntity` | **C/⛔:** sem setter/hook dinâmico identificado; +raio amplia volume e custo de varredura |
| Alvos | `getEntitiesOfClass` + `shouldHealEntity` + `distanceTo` | **C/⛔:** seleção provider-owned, sem substituir filtro por aliados de outro sistema |
| Intensidade | `(int)getSpellPower-1` → `amplifier+1` | **A:** escalonamento nativo de spell power; não criar segunda reserva de absorção |
| Duração | literal `2400` ticks | **D/⛔:** não está ligada a `getSpellPower`; perk de +duração carece seam auditado |
| Causação | cast → N aplicações de status → até N callbacks e eventos de dano posteriores | **D/⛔:** um cast de área não equivale a N casts ou N XP; absorção gasta não está atribuída ao caster por prova nesta ficha |
| Reaplicação | `onEffectStarted` adiciona absorção existente | **C:** suspeita de refresh/stacking requer GameTest, sem mudança em provider |

**Work budget:** a busca é uma AABB de aresta **16 blocos**, com filtro radial; um perk que aumenta raio teria crescimento de volume cúbico e potencial número de entidades no mesmo cast. **Não** ampliar area/cap sem limite de targets e limites de CPU/memória acordados. Cooldown/custo seguem Iron's; Black Arcana não replica buff, RPG Skill Tree apenas fornece perks/gates por contrato real.

## QA físico necessário

- [ ] Conferir hash do JAR instalado, bytecode de `FortifySpell`, `FortifyEffect` e `MobEffectRegistry`, e compatibilidade loader exato.
- [ ] Testar 0, 1, múltiplos aliados, equipes, player sem equipe, summon, mob neutral/hostil, entidade no limite de 8 blocos e muitos alvos.
- [ ] Medir absorção antes/depois, atributo MAX_ABSORPTION, dano bloqueado/consumido, dispel, refresh com amp igual/maior/menor, logout/relog e fim do efeito; evitar hipótese de stacking como fato.
- [ ] Verificar ausência de dano duplicado/XP por alvo e que partícula/preview não geram cast; dedicated-server e Survival modpack.
- [ ] Auditar eventual hook real e respectivo contrato de budgets antes de expor perk de raio/duração/target-type.

**Estado:** ✅ causa rastreada na fonte; ⚠️ artefato e execução reais não aprovados; ⛔ mutabilidade externa sem contrato; Stage 06.05 🟡.
