# Paladin Spells 1.1.1 — catálogo de spells

Última auditoria: 2026-09-14

## Escopo e autoridade

Este catálogo fecha a superfície **spell-level registrada** por `paladin_spells` `1.21.1-1.1.1` para NeoForge 1.21.1. Efeitos, entidades e handlers auxiliares só entram quando alteram diretamente a semântica de um dos spells registrados.

Presença/versão no inventário versionado do modpack:

- RPG Skill Tree sibling `docs/MODPACK_SCOPE.md`, derivado de `modlist(20260822-201255).txt`: `paladin_spells` `1.21.1-1.1.1`.
- A modlist física/runtime atual continua sendo autoridade superior quando estiver disponível/versionada; este arquivo não afirma presença física posterior ao snapshot.

Fonte pública da release auditada:

- projeto oficial: `Kaufko/Paladin-Spells`;
- branch de Minecraft 1.21: `1.21`;
- commit auditado: `31f64ccdb39d062b21cc25d434cb62d6463b486e`, de 2026-08-16;
- `gradle.properties` nesse commit declara `minecraft_version=1.21.1`, `mod_id=paladin_spells` e `mod_version=1.21.1-1.1.1`;
- o commit final corrige o crash de servidor por classe client-only, item também registrado no changelog 1.1.1;
- CurseForge publica `paladin_spells-1.21.1-1.1.1.jar` como release NeoForge 1.21.1 em 2026-08-16, file ID `8661566`.

Essa combinação fecha uma fonte pública **alinhada à release 1.1.1**. O JAR físico do modpack não foi extraído/hash-comparado nesta auditoria, portanto o catálogo não declara identidade binária entre Git commit e JAR instalado.

## Resultado

Estado: ✅ **Catalogado para o registry de spells da versão 1.1.1**.

Resumo fechado:

- **5** registros em `SpellRegistry.SPELL_REGISTRY_KEY`;
- **5** classes e somente cinco arquivos no diretório `spells/` da fonte auditada;
- todos usam a escola `irons_spellbooks:holy` do host Iron's; o addon não registra escola própria;
- **4** `MobEffect` auxiliares próprios são registrados (`taunt`, `bulwark`, `sworn_protector`, `bedrock_skin`) e não são recontados como spells;
- `PaladinSpells` registra `PaladinSpellRegistry`, efeitos, sons e entidades no mod event bus;
- Iron's Spells 'n Spellbooks é dependência requerida pelo `neoforge.mods.toml`.

Catalogação completa **não equivale a afirmar funcionamento integral de cada efeito**. A seção 3 preserva divergências encontradas no source exato da release.

## 1. Registry canônico de spells

`PaladinSpellRegistry` registra exatamente:

| ID runtime | Raridade mínima | Nível máx. | Cooldown | `baseManaCost` | `manaCostPerLevel` | Tipo | Semântica codificada |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| `paladin_spells:taunt` | Rare | 10 | 20 s | 30 | 10 | Instant | aplica efeito de taunt a mobs hostis em alcance e grava o UUID do caster como alvo forçado |
| `paladin_spells:bulwark` | Rare | 10 | 45 s | 30 | 10 | Instant | aplica o efeito `paladin_spells:bulwark` com duração escalada; ver ressalva funcional na seção 3 |
| `paladin_spells:sworn_protector` | Rare | 10 | 35 s | 30 | 15 | Instant | calcula raio, duração e percentual de redirecionamento; o handler server-side existe, mas o `onCast` auditado só grava estado/aplica efeito no lado cliente |
| `paladin_spells:bedrock_skin` | Rare | 10 | 25 s | 30 | 15 | Instant | aplica armadura e redução de dano calculada, cria uma entidade-âncora e monta o caster nela para imobilização temporária |
| `paladin_spells:ram` | Rare | 10 | 10 s | 15 | 5 | Instant | impulsiona o caster na direção do olhar, causa dano escalado por armadura/spell power/nível e aplica knockback a entidades interceptadas |

Os campos de mana e spell power citados abaixo são os valores crus das classes da release; nenhuma fórmula interna adicional do host é inventada aqui.

## 2. Semântica individual

### 2.1 Taunt — `paladin_spells:taunt`

Configuração da classe:

- `baseSpellPower = 10`;
- `spellPowerPerLevel = 5`;
- alcance codificado: `10 + getSpellPower(spellLevel, caster) * 2`;
- duração codificada em segundos: `5 + getSpellPower(spellLevel, caster)`.

Execução observada:

- procura `Mob` vivos dentro da AABB inflada e confirma distância real ao caster;
- só aplica o efeito quando o mob implementa `Enemy`;
- grava `taunt_target_uuid` no persistent data do mob;
- `TauntEffect` roda a cada tick, resolve o UUID no `ServerLevel`, chama `setTarget`, marca o mob agressivo e, quando o alvo é player, chama `setLastHurtByPlayer`;
- partículas Angry Villager são apenas apresentação auxiliar.

### 2.2 Bulwark — `paladin_spells:bulwark`

Configuração da classe:

- `baseSpellPower = 15`;
- `spellPowerPerLevel = 5`;
- cooldown 45 s, coerente com a correção declarada no changelog 1.1.1;
- duração: `min(5 + 15 * getSpellPower(...) / 100, 35)` segundos;
- amplifier aplicado ao efeito: `round(getSpellPower(...) * 10)`.

O cast server-side aplica `paladin_spells:bulwark`. Porém `BulwarkEffect` registra um modificador de `Attributes.ARMOR` com:

- amount `0.0`;
- operação `ADD_MULTIPLIED_TOTAL`.

Na fonte auditada não foi encontrado outro handler que substitua esse amount ou converta o amplifier em bônus de armor. Consequência: o catálogo registra o **efeito e a intenção/configuração observável**, mas **não afirma aumento efetivo de armor** para esta release apenas com base no source.

### 2.3 Sworn Protector — `paladin_spells:sworn_protector`

Configuração da classe:

- `baseSpellPower = 10`;
- `spellPowerPerLevel = 5`;
- nível máximo 10;
- cooldown 35 s;
- duração: `15 + 20 * getSpellPower(...) / 100` segundos;
- raio usado pelo cast: `(10 + spellLevel * 2) * 3` — a função recebe o nível como argumento, apesar do parâmetro local ser chamado `spellPower`;
- percentual de redirect é limitado a `1.0` e combina progressão normalizada de nível, spell power e armor do caster.

Existe um handler server-side `SwornProtectorEvent` que:

- só considera dano recebido por players;
- procura protetores com `SWORN_PROTECTOR_EFFECT`;
- exige `sworn_protector_range` e `sworn_protector_redirect` no persistent data;
- escolhe o protetor válido mais próximo;
- reduz o dano da vítima pelo percentual e aplica a parcela redirecionada ao protetor usando o damage type próprio `redirect`;
- impede recursão quando a fonte já é `redirect`.

Ressalva da release auditada: `SwornProtectorSpell.onCast` executa o bloco que grava os dois valores e adiciona o efeito somente quando `level.isClientSide` é verdadeiro. O handler de dano, por sua vez, retorna no cliente e exige esse estado no servidor. Portanto a cadeia server-side completa **não fica comprovada pelo source 1.1.1**; este catálogo não promove o redirecionamento como funcional sem teste runtime/JAR real.

### 2.4 Bedrock Skin — `paladin_spells:bedrock_skin`

Configuração da classe:

- `baseSpellPower = 5`;
- `spellPowerPerLevel = 2`;
- duração: `5 + getSpellPower(...)` segundos;
- redução calculada usa nível normalizado, spell power e armor, limitada a 95%.

No cast server-side:

- grava `bedrock_skin_reduction` no persistent data;
- aplica `paladin_spells:bedrock_skin` por `duration * 20` ticks;
- o efeito adiciona **+10 Armor** via `ADD_VALUE`;
- cria `BedrockSkinEntity`, define sua duração e monta o caster nela como âncora.

`BedrockSkinEvent` lê `bedrock_skin_reduction` em `LivingDamageEvent.Pre` e multiplica o dano por `(1 - reduction)` enquanto o efeito estiver ativo.

### 2.5 Ram — `paladin_spells:ram`

Configuração da classe:

- `baseSpellPower = 4`;
- `spellPowerPerLevel = 1`;
- multiplier de deslocamento: `getSpellPower(...) / 3`;
- dano: `armor * 1.25 + getSpellPower(...) + spellLevel * 2`.

Execução observada:

- usa a direção do olhar do caster, com suporte a um cast-data interno que pode girar a direção 90° para um dos lados;
- cria impulso e também ajusta `deltaMovement` do caster;
- constrói uma AABB ao longo do vetor de carga e atinge entidades vivas diferentes do caster;
- causa dano via `mobAttack(entity)` e knockback `1.5`;
- sincroniza impulso por `ImpulseCastData` para o caminho client cast.

## 3. Divergências release-facing preservadas

O changelog 1.1.1 declara correções de duração de Sworn Protector, cooldown de Bulwark, crash de servidor por classe client-only e remoção do marcador WIP de dois spells. Essas declarações são evidência de intenção/release notes, não substituem a implementação observada.

Duas divergências relevantes permanecem na fonte auditada:

1. **Bulwark:** o spell calcula spell power/amplifier, mas o `MobEffect` registrado possui modificador de Armor com amount `0.0`. Nenhum segundo caminho de armor foi observado no escopo auditado.
2. **Sworn Protector:** o handler de redirecionamento é server-side, porém `onCast` adiciona o efeito e persistent data apenas sob `level.isClientSide`.

Estado de catálogo desses casos: ✅ inventariados e documentados. Estado de eficácia runtime: ⚠️ **não promovido sem execução física da release/JAR**.

Isso evita transformar texto promocional ou changelog em resultado de teste.

## 4. Registries auxiliares

A release registra quatro efeitos próprios:

- `paladin_spells:taunt`;
- `paladin_spells:bulwark`;
- `paladin_spells:sworn_protector`;
- `paladin_spells:bedrock_skin`.

Eles são mecanismos auxiliares dos cinco spells e não aumentam a contagem spell-level.

Todos os cinco spells usam `SchoolRegistry.HOLY_RESOURCE`; não há `DeferredRegister<SchoolType>` próprio necessário para o catálogo desta release.

## 5. Evidência técnica usada

Fonte upstream auditada: `Kaufko/Paladin-Spells@31f64ccdb39d062b21cc25d434cb62d6463b486e`, branch `1.21`.

Arquivos principais:

- `gradle.properties` — Minecraft, mod ID e versão exatos;
- `changelog.md` — escopo declarado da 1.1.1;
- `src/main/resources/META-INF/neoforge.mods.toml` — dependências runtime;
- `PaladinSpells.java` — wiring dos registries;
- `registry/PaladinSpellRegistry.java` — conjunto fechado dos 5 spell IDs;
- os cinco arquivos em `spells/` — configuração e cast;
- `registry/PaladinEffectsRegistry.java` — quatro efeitos auxiliares;
- `effects/TauntEffect.java`, `effects/BulwarkEffect.java`, `effects/BedrockSkinEffect.java`, `effects/SwornProtectorEffect.java`;
- `events/BedrockSkinEvent.java` e `events/SwornProtectorEvent.java`.

Release pública cruzada: CurseForge file ID `8661566`, `paladin_spells-1.21.1-1.1.1.jar`, NeoForge 1.21.1, upload em 2026-08-16.

## 6. Limite clean-room

A inspeção upstream foi usada para inventário, contratos observáveis e interoperabilidade documental. Nenhum código, asset, som, ícone, texto de UI ou implementação upstream é incorporado ao runtime Black Arcana por este documento.

Este catálogo não cria integração com Paladin Spells. Qualquer provider/bridge futuro deve confirmar o JAR físico instalado e hooks reais, preservar a autoridade do Black Arcana e falhar fechado quando um efeito externo não puder ser provado.