# Farmer's Spell 'n Spellbooks 1.0.4.0 — catálogo de spells

Última auditoria: 2026-09-14

## Escopo e autoridade

Este catálogo fecha a superfície **spell-level registrada** pelo addon `farmers_spell` `1.0.4.0-1.21.1` para NeoForge 1.21.1. Conteúdo culinário, equipamentos, fluidos, receitas, entidades e efeitos do addon só entram aqui quando alteram diretamente a semântica de um spell registrado.

Presença/versão no inventário versionado do modpack:

- RPG Skill Tree sibling `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`: `farmers_spell` `1.0.4.0-1.21.1`.
- A modlist física/runtime atual continua sendo autoridade superior quando estiver disponível/versionada; este arquivo não afirma presença física posterior ao snapshot.

Fonte upstream exata auditada:

- repositório: `GLDYM/Farmers-Spell-n-Spellbook`;
- branch de release: `1.21.1`;
- commit da release 1.0.4: `3d088a0a3170e1fb93a176b86b2a7dd5f30fc1bd`, de 2026-08-14;
- `gradle.properties` desse commit declara `mod_id=farmers_spell` e `mod_version=1.0.4.0-1.21.1`;
- `neoforge.mods.toml` exige `farmersdelight`, `irons_spellbooks` e `geckolib`; Iron's é requerido em `[1.21.1-3.16.0,)`.

## Resultado

Estado: ✅ **Catalogado para o registry de spells da versão 1.0.4.0**.

Resumo fechado:

- **6** registros reais em `SpellRegistry.SPELL_REGISTRY_KEY`;
- **1** escola própria registrada: `farmers_spell:gluttony`;
- **7** `MobEffect` próprios existem no addon, mas eles não são recontados como spells; três aparecem diretamente na execução dos spells registrados (`seal_oil`, `claw_break`, `magical_ingredient`);
- `BerserkCleaverSpell.java` existe na árvore, mas o arquivo inteiro está comentado e não existe registro `berserk_cleaver` em `ModSpells`; portanto **não é spell runtime** desta release;
- `FarmersSpell` registra `ModSchools` e `ModSpells` diretamente no mod event bus; não existe gate opcional para os seis spells dentro do addon, porque Iron's é dependência obrigatória do próprio mod.

## 1. Registry canônico de spells

`ModSpells` contém exatamente os seis `DeferredHolder<AbstractSpell, AbstractSpell>` abaixo.

| ID runtime | Nome en_us | Raridade mínima | Nível máx. | Cooldown | `baseManaCost` | `manaCostPerLevel` | Tipo | Semântica observada |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `farmers_spell:goodberry` | Goodberry | Common | 1 | 10 s | 30 | 0 | Instant | em combate recente, cura o caster e aplica Luck; fora de combate, cria um Goodberry no inventário ou o derruba se não houver espaço |
| `farmers_spell:phantom_loot` | Ubiquitous | Rare | 1 | 10 s | 100 | 0 | Long | mira um mob válido e rola/concede a loot table padrão dele com contexto de ataque do jogador sem matar o alvo |
| `farmers_spell:seal_coat` | Grease Coating | Common | 5 | 35 s | 30 | 5 | Long | aplica `farmers_spell:seal_oil` por 300 ticks com amplifier `spellLevel - 1`; o efeito participa de cura reativa quando o portador recebe dano |
| `farmers_spell:bad_apple` | Rotten Apple | Common | 5 | 30 s | 50 | 0 | Long | cria uma entidade Rotten Apple estática na posição raycastada, com vida e raio de provocação escalados por nível, que força mobs próximos a alvejá-la |
| `farmers_spell:chaos_slash` | Chaotic Pastry Slash | Common | 5 | 1 s | 8 | 2 | Instant | lança projétil expansivo de slash; cada entidade atingida é danificada uma vez e recebe `farmers_spell:claw_break` por 200 ticks |
| `farmers_spell:preserve_circle` | Brining Ritual | Common | 10 | 40 s | 30 | 2 | Long | cria uma AoE persistente com raio influenciado por nível e tempo de canalização; aplica Slowed do Iron's e `farmers_spell:magical_ingredient` |

Os campos de mana acima são os valores crus configurados pela classe (`baseManaCost` / `manaCostPerLevel`); este catálogo não inventa a fórmula efetiva do host além do contrato exposto pela versão auditada.

## 2. Semântica individual

### 2.1 Goodberry — `farmers_spell:goodberry`

- escola: `farmers_spell:gluttony`;
- instantâneo, nível único;
- considera combate recente quando `getLastHurtByMob()` existe e o último timestamp está a menos de 100 ticks;
- nesse estado cura `4.0f` e aplica Luck por 200 ticks;
- fora desse estado cria `farmers_spell:goodberry`, adiciona ao inventário e faz drop se a inserção falhar.

A criação do item faz parte do efeito do spell, mas o comportamento alimentar do item é conteúdo não-spell e não é recontado como outro feitiço.

### 2.2 Phantom Loot / Ubiquitous — `farmers_spell:phantom_loot`

- escola: Gluttony; Rare; nível 1;
- seleção usa o helper de target do Iron's com alcance `32`;
- somente `Mob` passa pela condição;
- rejeita tipos na tag `farmers_spell:phantom_loot_blacklist`;
- rejeita mobs acima do limite configurado `phantomLootMaxHp` — default `100.0`, intervalo permitido `1.0..1000.0`;
- também rejeita o alvo quando **largura e altura** são ambas maiores que `3.0`;
- no cast, obtém a loot table padrão do tipo do mob, monta contexto `ENTITY` com o caster como atacante/último player e concede os itens rolados ao jogador, sem matar o mob.

Isso é catalogado como comportamento próprio do spell; nenhuma loot table externa é incorporada ao catálogo como conteúdo do addon.

### 2.3 Grease Coating — `farmers_spell:seal_coat`

- aplica `seal_oil` por 300 ticks, amplifier `spellLevel - 1`;
- `SealOilEffect` registra modificador de `ATTACK_SPEED` com amount `-0.25`, operação `ADD_MULTIPLIED_BASE`;
- em `LivingDamageEvent.Pre`, enquanto `seal_oil` estiver ativo e o cooldown interno estiver zerado, o alvo é curado em `2.0 + maxHealth * (level * 0.01)`;
- o cooldown interno dessa cura é colocado em 100 ticks.

O texto de guia da release é tratado como apresentação; a descrição acima segue a execução auditada.

### 2.4 Rotten Apple — `farmers_spell:bad_apple`

- raycasta até 30 blocos e cria `BadAppleEntity` apenas no lado servidor;
- vida máxima configurada pela entidade: `50 + 10 * spellLevel`;
- raio de taunt: `8 + 2 * (spellLevel - 1)`;
- a entidade é mantida fixa na posição de spawn, sem gravidade e sem push;
- a cada tick servidor, mobs dentro do raio passam a usar a maçã como alvo;
- `maxLifetime = 6228` ticks, salvo morte/remoção anterior.

A entidade auxiliar é parte da execução deste spell e não um spell adicional.

### 2.5 Chaotic Pastry Slash — `farmers_spell:chaos_slash`

- dano configurado pelo próprio spell como `getSpellPower(spellLevel, caster)`;
- classe base do spell define `baseSpellPower = 5` e `spellPowerPerLevel = 1`;
- lança `ChaosSlashProjectile`, que cresce de raio ao viajar e expira após 80 ticks ou ao colidir com bloco;
- cada alvo elegível é atingido no máximo uma vez por projétil;
- aplica `claw_break` por 200 ticks;
- `ClawBreakEffect` registra modificador de `ATTACK_DAMAGE` com amount `-0.015`, operação `ADD_MULTIPLIED_BASE`.

O catálogo não atribui efeitos que não estejam presentes no fluxo de código auditado.

### 2.6 Brining Ritual — `farmers_spell:preserve_circle`

- cast time efetivo é `min(20 + spellLevel * 10, 160)`;
- durante canalização, usa `TargetedAreaEntity` do Iron's como preview server-authored e atualiza o raio em torno do caster;
- raio: `1.0 + 0.5 * spellLevel + castTimeElapsed / 20.0`;
- duração da AoE: `(spellLevel * 2.5 + 10) * 20` ticks;
- a AoE tem `reapplicationDelay = 20`;
- em alvos, aplica Slowed do Iron's por 60 ticks e `magical_ingredient` por 1200 ticks no amplifier `spellLevel - 1`;
- `MagicalIngredientEffect` registra modificador de `MOVEMENT_SPEED` amount `-0.02`, operação `ADD_MULTIPLIED_TOTAL`;
- enquanto o efeito está ativo, dano `MAGIC` vanilla ou `farmers_spell:gluttony_magic` é ampliado em `(5 + level)%`;
- no drop do alvo, cada stack existente recebe uma tentativa de +1 por nível, cada tentativa com chance de 10%.

## 3. Escola e registries auxiliares

Todos os seis spells usam `farmers_spell:gluttony`. A escola própria referencia:

- focus tag `farmers_spell:gluttony_focus`;
- atributo próprio de spell power;
- atributo próprio de magic resistance;
- damage type `farmers_spell:gluttony_magic`.

O addon registra sete `MobEffect` próprios:

- `druid_heal`;
- `seal_oil`;
- `cleanse`;
- `frost_shield`;
- `claw_break`;
- `golden_armor`;
- `magical_ingredient`.

A existência desses efeitos demonstra que o addon tem conteúdo mágico além do registry de spells, porém este arquivo só fecha a **superfície spell-level**. Efeitos acionados exclusivamente por comida/equipamento não são promovidos aqui como spells.

## 4. Exclusão explícita — Berserk Cleaver

A árvore da release contém `spells/BerserkCleaverSpell.java`, mas todo o conteúdo do arquivo está dentro de comentário de bloco `/* ... */`. Além disso, `ModSpells` não declara `SPELLS.register("berserk_cleaver", ...)`.

Consequência de catálogo:

- source artifact encontrado: sim;
- classe compilável/runtime nessa release: não;
- registry ID ativo: não;
- contado entre spells: **não**.

Isso evita confundir código desativado/WIP com conteúdo disponível no jogo.

## 5. Evidência técnica upstream

Commit exato auditado: `3d088a0a3170e1fb93a176b86b2a7dd5f30fc1bd`.

Arquivos principais usados para fechar o inventário:

- `gradle.properties` — versão e mod ID;
- `src/main/resources/META-INF/neoforge.mods.toml` — dependências runtime obrigatórias;
- `src/main/java/com/chenjdy/farmers_spell/FarmersSpell.java` — registro no event bus;
- `src/main/java/com/chenjdy/farmers_spell/init/ModSpells.java` — conjunto fechado dos seis spell IDs;
- `src/main/java/com/chenjdy/farmers_spell/init/ModSchools.java` — escola Gluttony;
- as seis classes registradas em `spells/` — configuração e fluxo de cast;
- `spells/BerserkCleaverSpell.java` — evidência de conteúdo totalmente comentado/não registrado;
- `entity/BadAppleEntity.java`, `entity/ChaosSlashProjectile.java`, `entity/PreserveCircleAoe.java` — execução indireta dos spells;
- `init/ModEffects.java` e efeitos usados pelos spells;
- `event/EffectsEventHandler.java` — semântica reativa de `seal_oil` e `magical_ingredient`;
- `assets/farmers_spell/lang/en_us.json` — nomes player-facing da release.

## 6. Limite clean-room

A inspeção upstream foi usada apenas para inventariar IDs, registries, dependências e semântica necessária à catalogação/interoperabilidade. Nenhum código, asset, texto de UI, modelo, som ou implementação upstream é incorporado ao runtime do Black Arcana por este documento.

Este catálogo não cria integração com Farmer's Spell 'n Spellbooks. Qualquer bridge futura precisa confirmar o JAR físico instalado e o contrato real do provider, preservar a autoridade do Black Arcana e falhar fechado quando não houver hook seguro.
