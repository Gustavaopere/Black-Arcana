# Somake Spells 1.0.9 — 7/7 classes: métodos compilados de cast e efeitos

**Evidência:** ✅ EXACT_SHA1_METHOD_REFERENCE_DISCOVERY / ⚠️ não é equivalência causal integral nem contrato de perk.

## Artefato e execução

- Publisher CurseForge File 8867079: somakespells-1.0.9-1.21.1.jar; mod ID somakespells; SHA-1 físico e publisher 171841ac9f802be9309ecc166c1d972ac6d404c0.
- [GitHub Actions Java21 #39192999780](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192999780) — SUCCESS. O gate recuperou as sete FQCN auditadas, inventariou 116 declarações de métodos de classe (incluindo 101 métodos cujo nome atende ao filtro de interesse), seus descritores JVM e referências simbólicas. Sete testes sintéticos Java21 passaram; nenhuma divergência de SHA.
- A primeira execução do mesmo trabalho [#39192927218](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39192927218) falhou fechada por limite artificial de 250 caracteres de uma referência JVM. O script passou a aceitar até 2048 caracteres por símbolo e ganhou teste negativo para rejeitar símbolos acima desse limite. Não foram removidas comparações de hash, limite de classe ou testes negativos.
- [Verificador](../../../../docs/qa/somake_109_cast_refs.py), [testes](../../../../docs/qa/somake_109_cast_refs_test.py), [workflow](../../../../.github/workflows/somake-109-cast-refs.yml). O JAR não é persistido no repositório; somente um JSON limitado de descritores e símbolos é exportado.

## Matriz por spell (métodos/callsites do classfile exato)

| Spell ID | Família de cast referenciada | Métodos do provider compilados | Relações causais estaticamente identificadas |
|---|---|---|---|
| somakespells:fragmented_requiem | CastType.LONG | onCast, getTargetCenter, spawnSwordCircle, getSwordCount, getSwordDamage | onCast referencia getTargetCenter, getSwordDamage e spawnSwordCircle; o helper instancia FragmentedSwordRainEntity e usa ServerLevel.addFreshEntity; getSwordDamage consulta getSpellPower; getSwordCount chama Mth.clamp |
| somakespells:rose_secret | CastType.INSTANT | onCast, getEffectDuration | onCast referencia ModMobEffects.ROSE_SECRET, MobEffectInstance e LivingEntity.addEffect; duração deriva de rotina que consulta getSpellPower, Math.round e Mth.clamp |
| somakespells:comforting_lullaby | CastType.CONTINUOUS | onCast, onServerCastTick, applyPulse, canReceiveLullaby, getRadius, getHealing | applyPulse referencia AABB.inflate, getEntitiesOfClass, SpellHealEvent, NeoForge.EVENT_BUS.post, Player.heal e efeito Sleepy do TunesCompat; getHealing consulta getSpellPower |
| somakespells:funeral_bloom | CastType.LONG | onCast, getRadius, getDuration, getWaveInterval, getTelegraphTicks, getMaxTargets, getImpactDamage, getWitherDuration e getWitherAmplifier | onCast usa raycastForEntity e constrói FuneralBloomControllerEntity com parâmetros calculados; getRadius consulta SchoolType.getPowerFor; getImpactDamage consulta getSpellPower; vários contadores usam Mth.clamp |
| somakespells:withered_rose_vortex | CastType.LONG | onCast, getDamagePerPulse, getRadius, getLifetimeTicks, getWitherDuration, getWitherAmplifier | onCast usa raycastForEntity e cria WitheredRoseVortexEntity; getDamagePerPulse consulta getSpellPower; getRadius consulta SchoolType.getPowerFor; getLifetimeTicks usa Mth.clamp |
| somakespells:custodia_caeli | CastType.LONG | onServerPreCast, onCast, getTargetedSigilPosition, getBlessingDuration, getMaxHealthBonusPercent, getArmorBonus, getArmorToughnessBonus | pre-cast instancia TargetedAreaCastData via TargetedAreaEntity e MagicData.setAdditionalCastData; onCast consulta TargetAreaCastData.getCenter ou getTargetedSigilPosition e constrói CustodiaCaeliSigilEntity |
| somakespells:jingle_bell | CastType.LONG | onCast, getRadius, getDamagePerPulse, getHealingAmplifier, getLifetimeTicks | onCast referencia Utils.raycastForBlock, cria BellEntity e chama TunesCompat.spawnCelestialHealingCircle; getDamagePerPulse consulta getSpellPower; lifetime utiliza Mth.clamp |

Os nomes de entidades e membros decorrem de referências JVM do JAR SHA-exato, não de reconstrução de implementação proprietária. Os nomes de CastType são constantes referenciadas pelos respectivos getters; não há medida de duração de cast ao vivo.

## Matriz de engenharia para perks — níveis de prova independentes

| Eixo | Evidência nesta auditoria | Decisão atual |
|---|---|---|
| Classe / método de entrada | 7/7 classfiles e método onCast nominal de cada classe | ✅ localizador comprovado; não prova elegibilidade de gameplay |
| Alvo e aquisição | Funeral Bloom / Withered Rose Vortex usam raycastForEntity; Custodia usa RaycastBuilder; Jingle Bell usa raycastForBlock | ⚠️ alcance exato, prioridade de bloco/entidade, LOS, PvP/claims e validade ainda não demonstrados |
| Geometria | Referências a getRadius em múltiplos spells, AABB.inflate no healing, entidades de área e helper spawnSwordCircle | ⚠️ raio, AABB, hitbox, quantidade de instâncias, limites e unidade ainda sem fórmula/consumidor downstream fechado |
| Dano e cura | getSpellPower aparece nos métodos getSwordDamage/getImpactDamage/getDamagePerPulse/getHealing; SpellHealEvent é postado em applyPulse | ⚠️ fórmulas e hooks de mutação não homologados para a versão integrada; evitar double-processing |
| Buff/debuff | Rose Secret gera MobEffectInstance; Comforting Lullaby referencia Sleepy (compat Tunes); os dois Blood spells referenciam Wither duration/amplifier | ⚠️ aplicação por entidade, stack, recast e duração efetiva dependem de análise downstream |
| Tempo, targets e work budget | getDuration, getLifetimeTicks, getWaveInterval, getMaxTargets, getTelegraphTicks e Mth.clamp presentes | ⚠️ valores, conversão ticks/segundos, ceilings e probabilidade de proc não obtidos deste gate |
| Efeitos secundários | FragmentedSwordRainEntity, FuneralBloomControllerEntity, WitheredRoseVortexEntity, CustodiaCaeliSigilEntity, BellEntity | ⛔ não duplicar dano/efeito; precisa seguir tick/hit/owner e descarte de cada entidade em auditoria própria |
| APIs para perks RPG | Ausência de contrato de mutação por jogador validado nesta inspeção | ⛔ FAIL_CLOSED; somente seleção de candidatos a futuras bridges |

## Próximos gates necessários

1. Auditar classes compiladas de entidades/effects downstream e suas rotas de tick/hit/owner; distinguir cast de dano por vítima, cura, aplicação de efeito e loops de área.
2. Recuperar constantes e dataflow exatos de métodos como getRadius, getMaxTargets, getDamagePerPulse e getLifetimeTicks sem transformar números isolados em fórmulas inventadas; registrar unidades e caps.
3. Conferir APIs públicas/eventos Iron's 3.16.3 e o boundary com RPG Skill Tree, incluindo ordem de pré-cast, cobrança, mutação e proteção de mundo.
4. Executar perfis controlados com provider carregado e depois o pack real para targeting, config, cliente, sincronização e Survival; não homologar Stage 09 com base em javap.

**Estados:** ✅ identidade 83/83 e 7/7 superfície de método explorada neste recorte; ⚠️ causalidade integral de runtime e config; ⛔ hooks mutadores não certificados. Nenhuma nova magia acrescentada e nenhuma Stage promovida.
