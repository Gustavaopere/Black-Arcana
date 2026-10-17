# Thunder Fanburst

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT`, `legendary_spellbooks:thunder_fanburst` / `dev.higurashi.legendary_spellbooks.common.spells.lightning.ThunderFanburstSpell`; [Java 21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179), [dossiê](../EXACT-BINARY-SPELLS-0.3.2.md). Dados numéricos source-pinned; execução/Survival ⚠️; +0.

- ID: `legendary_spellbooks:thunder_fanburst`
- School: Lightning
- Levels: 1–10
- Min rarity: Common
- Cooldown: 8 s
- Mana neutral: 55 / 60 / 65 / 70 / 75 / 80 / 85 / 90 / 95 / 100
- Spell power neutral: 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11
- Bolt count: 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12
- Lifetime field: 30 / 35 / 40 / 45 / 50 / 55 / 60 / 65 / 70 / 75 ticks
- Estado Black Arcana: `JÁ EXISTE / SEM ALTERAÇÃO PLANEJADA`

## Contract

Dispara o fanburst de bolts/lightning entities pelo provider. O count usa `min(2 + spellLevel,20)` e o lifetime `min(25 + 5 × spellLevel,100)`.

## Acquisition

Pool do Cloud Golem: níveis 3–10, weight 10. O Stormbound Grimoire possui afinidade específica com esta spell.

## QA

No source 0.3.2, o mapa SUNNY do Stormbound concede +1 nível a Thunder Fanburst, mas o tooltip constrói a linha correspondente como +2. O runtime `AffinityData` é authority do pin; validar a apresentação na build instalada.

## Regra para o Black Arcana

Não corrigir a divergência por override de nível no Black Arcana. Integrations devem observar o nível final provider-native.

## Source

`ThunderFanburstSpell.java`, `StormboundSpellbookItem.java` @ source pin 0.3.2.

## Engenharia causal para perks — 17/10/2026

**Prova:** `legendary_spellbooks` 0.3.2, JAR `legendary_spellbooks-1.21.1+neo-0.3.2.jar` SHA-1 `bda5b1fbe50ad834a6a76ad36789743c1057ebf5`, registro 30/30 COUNTED_EXACT ([Java21 #38453654179](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38453654179)). Mecânicas a seguir são **SOURCE_CAUSALITY** do pin `Higurashi34m/Legendary-Spellbooks@62ced2f2b2693aa841251473cbbd726fdd928ed3`; igualdade byte-a-byte de código e execução com Iron's 3.16.3/Legendary Monsters 2.2.2 **não verificadas**. Nenhum adapter RPG homologado.

| Eixo | Contrato factual observado | Limite para perks |
|---|---|---|
| Cast / stats | Níveis 1–10, cooldown 8s, mana 55+5×(nível−1), power 2+(nível−1). Uma conjuração cria boltsCount=min(2+level,20)=**3..12** tentativas de ElectricityEntity. | Criação de múltiplos efeitos não altera spell count. |
| Cono/direção | Fan de 70° com distância inicial 1.5, orientado ao yaw do caster; findGround(level,pos,4,4) para cada ponto. ElectricityEntity recebe caster, vetor de direção X/Z, Y 0, dano=getSpellPower, yaw e lifetime. | Largura final/velocidade e hitbox são propriedade de Legendary Monsters, sem adapter de retarget. |
| Lifetime | getLifeTick=min(25+level×5,100) =30..75 ticks para 1..10. Dano via entity externa, sem chamada hurt direta no onCast examinado. | Não inferir Lightning DamageType; verificar PvP, claims e evento de dano físico. |

**Âncoras:** [ThunderFanburstSpell.java](https://github.com/Higurashi34m/Legendary-Spellbooks/blob/62ced2f2b2693aa841251473cbbd726fdd928ed3/src/main/java/dev/higurashi/legendary_spellbooks/common/spells/lightning/ThunderFanburstSpell.java#L27-L82).

**QA e fail-closed:** QA 12 bolts, owner, side, collision, lifetime 30/75 e dano aceito; evitar double XP por bolt. Não usar simples onCast/trigger como settlement e nunca duplicar custo, objeto mágico ou fonte de dano. **+0 novos spells, +0 adapters.**
