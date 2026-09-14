# ISS: Magic From The East 1.1.5 — catálogo de spells

Última auditoria: 2026-09-14

## Escopo e autoridade

Este catálogo fecha a superfície **spell-level registrada** por `iss_magicfromtheeast` `1.1.5` para NeoForge 1.21.1. O objetivo é inventariar os spells ativos, as escolas próprias relevantes e a semântica pública observável da release sem transportar para ela alterações posteriores do repositório.

Presença/versão no inventário versionado do modpack:

- RPG Skill Tree sibling `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`: `iss_magicfromtheeast` `1.1.5`.
- A modlist física/runtime atual continua sendo autoridade superior quando estiver disponível/versionada; este arquivo não afirma identidade binária com um JAR físico atual que não foi fornecido nesta tranche.

Release pública oficial:

- projeto CurseForge: `Magic From The East`, project ID `1224162`;
- arquivo: `iss_magicfromtheeast-1.1.5.jar`;
- file ID: `7385201`;
- loader: NeoForge;
- Minecraft: 1.21.1;
- tipo: Release;
- upload: 2025-12-27.

Fonte pública alinhada à release:

- repositório oficial: `WarPhan78/ISS_MagicFromTheEast-1.21.x`;
- commit auditado: `f2a095cbbc89f8d8428dca758140663adf54ae88`;
- data do commit: 2025-12-27;
- mensagem do commit: `Small fix before 1.1.5 release`;
- `gradle.properties` nesse commit declara `minecraft_version=1.21.1`, `mod_id=iss_magicfromtheeast`, `mod_version=1.1.5` e dependência de Iron's `1.21.1-3.14.8`.

Essa combinação é usada como boundary da release. O HEAD público de 2026 ainda preserva `mod_version=1.1.5`, mas contém alterações posteriores em múltiplas classes de spells, entidades e escolas; por isso ele **não** é usado como snapshot semântico da release.

## Resultado

Estado: ✅ **Catalogado para o registry de spells da release 1.1.5**.

Resumo fechado:

- **22/22 spells ativos** em `SpellRegistry.SPELL_REGISTRY_KEY`;
- **11** spells na escola `iss_magicfromtheeast:symmetry`;
- **11** spells na escola `iss_magicfromtheeast:spirit`;
- **3** escolas próprias registradas na release: `symmetry`, `spirit` e `dune`;
- `dune` possui **0 spells ativos** em `MFTESpellRegistries` nessa release;
- `LaunchSpell` e `QigongControllingSpell` aparecem apenas em linhas de registro comentadas e **não são contados como runtime**;
- nenhuma fórmula numérica de spell é importada do HEAD 2026, porque várias classes mudaram após a release.

## 1. Registry canônico da release

`MFTESpellRegistries` cria um `DeferredRegister<AbstractSpell>` sobre `SpellRegistry.SPELL_REGISTRY_KEY` e registra cada spell pelo valor de `spell.getSpellName()`.

### 1.1 Symmetry — 11 spells

| # | Spell ID | Nome público da release | Semântica pública observável |
| ---: | --- | --- | --- |
| 1 | `iss_magicfromtheeast:sword_dance` | Sword Dance | Conjura espadas mágicas ao redor do caster; após atraso, elas avançam contra o último alvo ferido. |
| 2 | `iss_magicfromtheeast:bagua_array_circle` | Bagua Array Circle | Cria um círculo Bagua em uma área; a descrição oficial cita dano contra undead e Reversal Healing para o dono. |
| 3 | `iss_magicfromtheeast:dragon_glide` | Dragon Glide | Projeta uma força em forma de dragão à frente do caster, causando dano ao longo do trajeto e podendo romper magic shield. |
| 4 | `iss_magicfromtheeast:jade_judgement` | Jade Judgement | Invoca uma grande lâmina/Dao de jade com impacto em área. |
| 5 | `iss_magicfromtheeast:jiangshi_invoke` | Jiangshi Invoke | Invoca três Jiangshi para auxiliar em combate. |
| 6 | `iss_magicfromtheeast:underworld_aid` | Impermanence's Verdict | Invoca quatro Impermanence em uma área; a descrição oficial cita debuffs e dano com componente dependente da vida perdida do alvo. |
| 7 | `iss_magicfromtheeast:punishing_heaven` | Punishing Heaven | Invoca um Jade Executioner aliado. |
| 8 | `iss_magicfromtheeast:drapes_of_reflection` | Drapes Of Reflection | Cria uma drape mágica de jade descrita como capaz de defletir projéteis. |
| 9 | `iss_magicfromtheeast:cloud_ride` | Magic Cloud | Invoca uma nuvem mágica temporariamente montável. |
| 10 | `iss_magicfromtheeast:nephrite_slash` | Nephrite Slash | Executa um corte mágico de jade e faz cristais de nephrite emergirem do solo. |
| 11 | `iss_magicfromtheeast:jade_bullet` | Jade Bullet | Lança um projétil de jade que causa dano e produz uma pequena onda de choque no impacto. |

### 1.2 Spirit — 11 spells

| # | Spell ID | Nome público da release | Semântica pública observável |
| ---: | --- | --- | --- |
| 1 | `iss_magicfromtheeast:soul_catalyst` | Soul Catalyst | Após o cast, libera uma barragem de soul skulls; a descrição oficial cita aplicação de Soulburn ao acertar. |
| 2 | `iss_magicfromtheeast:soul_burst` | Soul Burst | Produz uma explosão de soul fire na posição do caster e afeta alvos dentro da área. |
| 3 | `iss_magicfromtheeast:spirit_challenging` | Spirit Challenging | Extrai parte da alma do alvo para um desafio; o dano na alma pode ser transferido ao dono e sair da zona/destruir a alma pode gerar debuff. |
| 4 | `iss_magicfromtheeast:bone_hands` | Bone Hands | Invoca Spirit Bone Hands do solo para atacar alvos em alcance. |
| 5 | `iss_magicfromtheeast:calamity_cut` | Devastating Cut | Executa um corte com a arma; a descrição oficial relaciona sua força à arma usada. |
| 6 | `iss_magicfromtheeast:kitsune_pack` | Kitsune Pack | Invoca um grupo de Kitsune aliados; a descrição oficial cita Soulburn nas mordidas. |
| 7 | `iss_magicfromtheeast:revenant_of_honor` | Revenant of Honor | Invoca um Spirit Samurai aliado. |
| 8 | `iss_magicfromtheeast:ashigaru_squad` | Ashigaru Squad | Invoca um esquadrão de Spirit Ashigaru. |
| 9 | `iss_magicfromtheeast:phantom_charge` | Phantom Charge | Invoca samurais montados que executam uma carga contra a formação inimiga. |
| 10 | `iss_magicfromtheeast:anchoring_kunai` | Anchoring Kunai | Fornece três kunai; a descrição oficial cita dano e aplicação de Anchored Soul. |
| 11 | `iss_magicfromtheeast:splitting_shuriken` | Splitting Shuriken | Lança uma spirit shuriken que se divide em projéteis menores após acertar o alvo. |

## 2. Registros comentados não contados

No registry exato da release existem duas linhas de registro desativadas por comentário:

- `LaunchSpell`;
- `QigongControllingSpell`.

Elas não produzem `Supplier<AbstractSpell>` ativo e não entram no denominador 22/22.

## 3. Escolas próprias da release

`MFTESchoolRegistries` registra três `SchoolType` no commit de release:

| School ID | Estado na release | Spells ativos neste catálogo |
| --- | --- | ---: |
| `iss_magicfromtheeast:symmetry` | ✅ registrada | 11 |
| `iss_magicfromtheeast:spirit` | ✅ registrada | 11 |
| `iss_magicfromtheeast:dune` | ✅ registrada | 0 |

A ausência de spells Dune ativos é observada diretamente em `MFTESpellRegistries`, cuja seção `//DUNE SPELLS` está vazia.

## 4. Drift pós-release que não é incorporado

O repositório continuou recebendo mudanças mantendo o mesmo número `1.1.5`. Comparando `f2a095c...` com o HEAD auditado de 2026 (`13208302...`), há 16 commits posteriores e diversas mudanças em classes de spells, entidades, efeitos e registries.

Uma divergência material é a escola Dune:

- em `f2a095c...`, `DUNE_RESOURCE` e o `SchoolType` Dune são registrados ativamente;
- no HEAD 2026 auditado, o registro de Dune foi comentado.

Consequência: este documento preserva **Dune registrada, 0 spells**, que é o estado da release 1.1.5 usada pelo snapshot, e não o estado posterior do source.

## 5. Limites deste catálogo

Este catálogo fecha o inventário spell-level e a semântica pública da release, mas não afirma sem uma auditoria class-by-class do commit de release:

- custo de mana;
- cooldown;
- raridade;
- nível mínimo/máximo;
- cast time/cast type;
- fórmulas de dano, duração, alcance ou scaling;
- identidade binária entre `f2a095c...` e o JAR físico atual do modpack;
- provider/hook de integração com Black Arcana.

As descrições de comportamento acima vêm das chaves `*.guide` do `en_us.json` da própria release e foram resumidas; elas não substituem tracing runtime nem afirmam detalhes que a descrição pública não fornece.

## 6. Evidência técnica usada

- CurseForge oficial `Magic From The East`, project ID `1224162`, file ID `7385201`, `iss_magicfromtheeast-1.1.5.jar`, NeoForge 1.21.1, Release, 2025-12-27.
- `WarPhan78/ISS_MagicFromTheEast-1.21.x@f2a095cbbc89f8d8428dca758140663adf54ae88`:
  - `gradle.properties` — versão, Minecraft, mod ID e dependência Iron's;
  - `MFTESpellRegistries.java` — 22 registros ativos e dois comentados;
  - `MFTESchoolRegistries.java` — três escolas registradas, incluindo Dune;
  - `assets/iss_magicfromtheeast/lang/en_us.json` — IDs, nomes públicos e descrições `guide` da release.
- comparação `f2a095c... -> 13208302...` — evidência de drift pós-release, usada somente para impedir que alterações posteriores sejam retroativamente atribuídas à 1.1.5.

## 7. Limite clean-room

Nenhum código, asset ou implementação de Magic From The East foi copiado para o runtime Black Arcana. O repositório público é usado como fonte factual para registry, versão e comportamento documentado da release.

Qualquer integração futura deve confirmar o JAR físico presente, hooks reais e contratos da versão instalada. Sem boundary seguro, o Black Arcana permanece fail-closed.