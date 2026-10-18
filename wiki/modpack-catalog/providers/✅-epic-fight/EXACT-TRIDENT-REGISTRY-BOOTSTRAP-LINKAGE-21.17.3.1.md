# Epic Fight 21.17.3.1 — vínculo exato ID de skill → lambda de propriedades

**Status (18/10/2026): ✅ `EXACT_PUBLISHER_COMPILER_GENERATED_ID_TO_SUPPLIER_LINKAGE` + ✅ `EXACT_PUBLISHER_COMPILED_SUPPLIER_PROPERTY_CALLSITES`; ⚠️ runtime; ⛔ adapters de perks/Mastery.** Prova em bytecode público para interoperabilidade, sem distribuir implementação, código-fonte, JAR ou assets de terceiros.

## Artefato e auditoria

- JAR: Epic Fight `21.17.3.1`, CurseForge projeto `405076`, file `8175609`; o runner exige SHA-1 `fb199b7bbea2fc402da28ab586e73f47e32f8fc0` e SHA-256 `8b882554cf10086398340fbdc741819ee72a801a3adce516c7f4768326a39526` antes de chamar `javap`. Hashes correspondem ao artefato publisher e à autoridade física histórica. Não houve novo dump do usuário.
- [GitHub Actions #39095049311](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39095049311), job `exact_skill_parameters`: **SUCCESS**. `PASS_BOUNDED_TRIDENT_ATTACK_PHASE_PROPERTIES` e `PASS_BOUNDED_TRIDENT_REGISTRY_BOOTSTRAP_LINKAGE`, sem desvios.
- Novos testes dedicados ao linkage: **10/10** autotestes, incluindo drift de ID, bootstrap index, field holder, registro, supplier, return type, duplicação e ausência de seção. As etapas anteriores também registraram **21/21**, **10/10**, **9/9** e **11/11** autotestes em seus verificadores independentes.
- JSON artifact GitHub Actions **#12124241789** (evidência compacta dos gates, sem JAR).
- [Verificador do linkage](../../../../docs/qa/epicfight_211731_trident_registry_linkage.py) · [verificador de propriedades](../../../../docs/qa/epicfight_211731_trident_attack_phase.py) · [workflow](../../../../.github/workflows/epicfight-211731-perk-binary.yml).

## Prova compilada em `EpicFightSkills`

O disassembly `javap -p -c -v` do JAR SHA-verificado mostrou esta sequência no inicializador estático e na tabela `BootstrapMethods`:

| ID exato no `DeferredRegister.register` | PC do `ldc` | `InvokeDynamic` | Bootstrap → `REF_invokeStatic` | `putstatic` holder |
|---|---:|---|---|---|
| `epicfight:wrathful_lighting` | 678 | #67 (`apply`) | `EpicFightSkills.lambda$static$40` → `WrathfulLightingSkill` | `WRATHFUL_LIGHTING` |
| `epicfight:tsunami` | 695 | #68 (`apply`) | `EpicFightSkills.lambda$static$42` → `ConditionalWeaponInnateSkill` | `TSUNAMI` |
| `epicfight:everlasting_allegiance` | 712 | #69 (`apply`) | `EpicFightSkills.lambda$static$43` → `EverlastingAllegiance` | `EVERLASTING_ALLEGIANCE` |

**Escopo da prova:** o script exige que, no initializer compilado, o literal do ID seja imediatamente seguido pelas instruções `invokedynamic → DeferredRegister.register → putstatic` com offsets crescentes, e que o índice do `InvokeDynamic` corresponda exatamente a uma entrada `LambdaMetafactory.metafactory` contendo o método sintético/return type esperado. A auditoria do construtor da mesma lambda exige os valores `AttackPhaseProperty` → float/enum → operação `ValueModifier` → `Builder.addProperty`. É uma relação **ID → supplier → argumentos de configuração** demonstrada para as três identidades, sem generalizar a outros mods ou IDs.

As chamadas e constantes compiladas comprovadas permanecem:

- Wrathful Lightning: `MAX_STRIKES_MODIFIER setter(1)` no primeiro grupo e `DAMAGE_MODIFIER setter(8)`, `MAX_STRIKES_MODIFIER setter(3)`, `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN`, tag `WEAPON_INNATE` no segundo.
- Tsunami: `ARMOR_NEGATION_MODIFIER adder(100)`, `STUN_TYPE=KNOCKDOWN`, `WEAPON_INNATE`.
- Everlasting Allegiance: `ARMOR_NEGATION_MODIFIER adder(30)`, `DAMAGE_MODIFIER multiplier(1.4)`, `STUN_TYPE=HOLD`, `WEAPON_INNATE`.

## Limites operacionais e para perks

- **Não** prova efetiva inscrição/ativação no player conectado, aplicação de `AttackPhase` em cada animação após combinação de modifiers, dano contra HP, proporção efetiva de armor negation, seleção de targets, alcance, collider, AOE, tamanho/velocidade de projétil, duração ou cooldown.
- `consumption` nos JSONs `50/50/40` é declarativo; o saldo e unidade do gauge/weapon charge precisam de settlement real. `summon_thunder`, hits de recall e variantes em água/chuva são consequências provider-owned; não contabilizar efeitos ou múltiplas fases como casts novos.
- Nenhum `ServerPlayerPatch.initialized=true` com cliente real, player `AttributeInstance`, pack completo, RPG Mastery ou adapter de retarget/damage foi homologado. Uma API de modificação segura **não** surge do fato de conseguirmos inspecionar um construtor.
- Os nomes sintéticos e offsets são específicos do binário `21.17.3.1`/compilador; mudança em release posterior requer nova auditoria fail-closed.
- A autoridade do Black Arcana continua em seu próprio runtime mágico e `WorldEffectPolicy`. O Epic Fight mantém Battle Mode/skills/attack phases/dano/recursos. O RPG Skill Tree apenas progressão/perks por fronteira realmente validada.

**Contagem:** Epic Fight 43/43 identidades core, 3/3 sobrenaturais `COUNTED_EXACT` e 40 excluídas do numerador mágico; **+0 magias, +0 adapters, +0 Stage promotions**. Global mínimo 1.857 semânticos / 1.855 estritos e denominador aberto. Stage 06.05 🟡, Stage 09 físico PENDING; PR #825 draft, sem merge.

Complemento: [propriedades binárias por fase](EXACT-TRIDENT-ATTACK-PHASE-PROPERTIES-21.17.3.1.md) e [evidência anterior de seleção de tridente e execução causal](EXACT-TRIDENT-CAUSAL-REFERENCES-21.17.3.1.md).
