# Field Extension — extensão do raycast da Galena Gauntlet (1.0.10)

**Estado:** ⚠️ **ficha individual parcial/condicionada**. Identidade JSON, tag, artefato publisher e janelas JVM selecionadas estão documentados e selados na versão **Alex's Caves Continued 1.0.10**; não há **hook mutador**, QA física, prova de compatibilidade com todo datapack ou certificação individual para perks. Marcadores: `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `perk_certification=NOT_CERTIFIED`, `mutation=NO_MUTATION`.

**Definição de escopo:** `alexscaves:field_extension` é um encantamento da **Galena Gauntlet** que modifica o parâmetro de distância da **consulta de mira nativa** de `MagneticWeaponEntity`. Não introduz magia castável própria, não transforma a arma controlada em um novo spell Black Arcana e não concede indiscriminadamente ataque, mineração ou AoE com o mesmo alcance.

## 1. Autoridade e proveniência

| Objeto | Identidade conferida |
|---|---|
| Provider e mod ID | Alex's Caves Continued / `alexscaves` |
| Versão instalada | `alexscaves-1.0.10-neoforge+1.21.1.jar` — [modlist física do RPG Skill Tree](https://github.com/Gustavaopere/neoforge-rpg-skilltree/blob/main/PROJECT-INSTRUCTIONS/modlist/modlist.md), entrada 019 |
| Plataforma | Minecraft 1.21.1 / NeoForge / Java 21 |
| Publisher JAR | **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c` |
| Enchantment ResourceKey | `alexscaves:field_extension`; recurso `data/alexscaves/enchantment/field_extension.json` |
| Recurso exato | **386 bytes**, SHA-256 `c0f2998a08abbefc53a67447ad9e899cdb43bf8a0144a38d53d5fde2b90eb43e` |
| Tag publisher | `data/alexscaves/tags/item/enchantable/galena_gauntlet.json`; **55 bytes**, SHA-256 `5f8a2dfe1222c6631122855a11ab011d916bea83d285d6ecd886a177c058c4cb` |
| Consumidor | `com/github/alexmodguy/alexscaves/server/entity/item/MagneticWeaponEntity.class`; SHA-256 `a26794c9eba89c554e812078886beda6129d5298219f685f6d0e2be315fbf071` |
| Emissor | `com/github/alexmodguy/alexscaves/server/item/GalenaGauntletItem.class`; SHA-256 `5a74328a7130704a4e2dca9e607bed4dc3a468b8bbcb6d4e238b4d2d962573b0` |
| Registry | `ACEnchantmentRegistry.class`; SHA-256 `60006fab1b3b29f5f93c8365416815a12770cf8877a059298cb4ee82f7a92f32` |

**Manifesto técnico:** [EXACT-FIELD-EXTENSION-1.0.10.json](../EXACT-FIELD-EXTENSION-1.0.10.json); [sonda read-only](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_field_extension_probe.py), [testes sintéticos](https://github.com/Gustavaopere/Black-Arcana/blob/main/docs/qa/alexscaves_1010_field_extension_probe_test.py), [workflow com selo](https://github.com/Gustavaopere/Black-Arcana/blob/main/.github/workflows/alexscaves-1010-field-extension.yml). A sonda reutiliza a auditoria publisher da [ficha Ferrous Haste](ferrous-haste.md) e do [manifesto exato Ferrous Haste](../EXACT-FERROUS-HASTE-1.0.10.json), com verificação de classe, método `tick()V`, checksum da release e igualdade integral via `--seal`. Foram selecionadas três janelas JVM delimitadas, **não um CFG completo**. Nenhum `.class` ou asset externo foi copiado ao Black Arcana.

A fonte pública de `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara versão **1.1.1**. Ela não é autoridade de paridade para o classfile 1.0.10; as constantes e offsets abaixo vêm do JAR publisher exato.

## 2. Recurso JSON 1.0.10

| Campo declarativo | Valor |
|---|---|
| `description.translate` | `enchantment.alexscaves.field_extension` |
| `supported_items` | `#alexscaves:enchantable/galena_gauntlet` |
| `weight` | **10**, peso de geração/seleção do encantamento, não probabilidade de hit |
| `max_level` | **4** |
| `min_cost` | `base=1`; `per_level_above_first=6` |
| `max_cost` | `base=41`; `per_level_above_first=10` |
| `anvil_cost` | **1** |
| `slots` | `["mainhand","offhand"]` |
| `exclusive_set` | Não declarado no JSON; regras externas/datapacks ainda podem condicionar combinações |

A tag embutida identifica `alexscaves:galena_gauntlet`. Níveis acima de IV não são homologados só porque valores alterados por datapack possam chegar a uma consulta: **o máximo IV é declarativo**, não prova de clamp interno em qualquer stack. Custos de anvil/min/max não correspondem a alcance, mana, munição, desgaste nem cooldown.

## 3. Consumidor compilado — fórmula do raycast nativo

**Método:** `MagneticWeaponEntity.tick()V`, **744 instruções**; SHA-256 do parse do método `b68e9174310dc32ea5ce7bbe627955d18e92db9e1c087d741a63cfb4ea251f41`, idêntico ao contrato exato de Ferrous Haste. Nos limites `@495–680`, `@680–930` e `@930–1005`, foram identificadas as seguintes instruções relevantes:

1. `@540–544`: guard de `isOwnerWearingGauntlet()`; o caminho ativo da entidade magnética é pré-requisito para entrar na manipulação de mira do jogador.
2. `@552–554`: inicializa local **8** com `30.0F`. Esse é o valor-base de distância da consulta nativa.
3. `@557–596`: exige controller compatível com `LivingEntity` e `LivingEntity.getUseItem()` identificando **Galena Gauntlet** ativa. Se esse ramo não se aplica, a soma do encantamento não é executada.
4. `@626`: campo `ACEnchantmentRegistry.FIELD_EXTENSION`; `@629` consulta `ACCompat.enchantLevel(useItem,FIELD_EXTENSION)`.
5. `@632–644`: pega o nível, converte para float, multiplica por **5.0F** (`@639–642`), soma ao valor-base e grava novamente o local 8 (`@644`).
6. `@656–659`: passa o local 8 convertido para `double` à operação **`ProjectileUtil.getHitResultOnViewVector(Entity,Predicate,double)`** (`@659`).

O cálculo de distância solicitado ao raycast é, nesse ramo:

`raycast_distance = 30.0F + 5.0F × enchantLevel(GalenaGauntlet, FIELD_EXTENSION)`

| Nível declarado | Distância solicitada ao raycast | Acréscimo ao valor-base |
|---:|---:|---:|
| 0 | 30 | 0 |
| I | 35 | +5 |
| II | 40 | +10 |
| III | 45 | +15 |
| IV | 50 | +20 |

**Escopo rigoroso:** são **unidades de distância passadas à consulta de mira no Minecraft**, para o ramo do usuário usando a gauntlet. Isso não certifica hit, dano, sucesso de mineração, raio esférico de AoE, alcance final de uma arma magnética, distância máxima de tether ou alcance aplicado a todas as entidades. A consulta possui `Predicate` e regras de colisão; tipo de alvo, bloqueios, line-of-sight, eventos, permissões e estado efetivo do mundo continuam sob o provider/engine. Também não equivale ao alcance do Black Arcana.

### 3.1. Outro uso do mesmo valor: ponto de espera / movimento

Se o resultado não segue o ramo elegível de `EntityHitResult` e ataque, a janela JVM registra:

- `@802–826`: obtém `Player.getEyePosition()` e `Player.getViewVector(1F)`.
- `@813–820`: calcula o escalar de movimento **`raycast_distance − 20.0F`** e chama `Vec3.scale`.
- `@823–826`: soma o vetor ao ponto dos olhos e atribui `moveTo`.

Assim, o escalar de deslocamento usado por esse **caminho de fallback** é `10 + 5×nível`, ou **10/15/20/25/30** para níveis 0/I/II/III/IV. Esse é o deslocamento ao longo do vetor de visão pedido para um ponto de referência. **Não** é a distância real percorrida em um tick, o alcance de mineração, nem o limite de distância de retorno. Em seguida, resultados de block hit podem substituir `moveTo` pelo ponto do hit.

### 3.2. Aquisição de entidade, ataque e seleção de blocos

- `@666–683`: resultado precisa ser `EntityHitResult` e `playerUseCooldown` precisa ser zero antes da seleção ofensiva.
- `@688–713`: o ponto desejado é derivado da posição e de metade da altura da entidade selecionada; o movimento nessa rota usa escalar nativo **0.2F @715–718**; **Field Extension não aumenta esse escalar**.
- `@720–760`: a arma magnética aproxima-se do alvo, usando comparação com `Entity.getBbWidth()+1.5F` e `strikeProgress`; só no ramo subsequente solicita `hurtEntity @771`. Aumentar o raio do raycast não implica ataque imediato ou dano de qualquer entidade visível.
- `@802–928`: na rota alternativa há `BlockHitResult`; o candidato a mineração só é identificado quando a distância quadrática da arma até o **centro do bloco** é menor que **2.25D** (`@877–901`). O block state precisa ser não ar para usar a localização do hit como destino (`@903–926`). **2.25 é distância ao quadrado**, não uma nova área de efeito; não multiplicar esse limite por Field Extension.
- `@930–984`: mudanças de bloco selecionado podem limpar `destroyBlockProgress`, independentemente do nível do encantamento. As operações de mineração após essa janela pertencem à rotina nativa já auditada em [Ferrous Haste](ferrous-haste.md): `getDigSpeed`, dureza, dano da ferramenta, verificações de mundo e `Level.destroyBlock`.

**Interação independente com Ferrous Haste:** `FERROUS_HASTE @608` define a flag de velocidade nativa no mesmo `tick`; não é a fonte do `+5F` por nível de Field Extension. Conforme a ficha específica, Ferrous Haste altera a escolha de cooldown após tentativa de ataque e o divisor do progresso de mineração. Os dois efeitos só se compõem quando as respectivas consultas e guards são elegíveis; compatibilidade de configurações e coexistência final devem ser verificadas no modpack.

## 4. Causalidade, recursos e limites de perk

| Eixo de alteração | Contrato de partida | Estado e limite |
|---|---|---|
| **Distância de mira/raycast** | `MagneticWeaponEntity.tick @552–659`, campo `FIELD_EXTENSION @626` | ✅ **Valor estático localizado**, ⚠️ hook de mutação não homologado; impor caps/validação de alvo antes de mudar |
| **Alcance de ataque efetivo** | `EntityHitResult`, `playerUseCooldown`, aproximação e `strikeProgress` | ⚠️ depende de alvo elegível, movimento da arma, colisão, dano aceito e outros guards; não equiparar à distância do raycast |
| **Mineração / seleção de bloco** | `BlockHitResult` e distância quadrática `< 2.25D`; `Level.destroyBlock` downstream | ⛔ não ampliar essa distância, burlar claims, remover filtros ou multiplicar drops sem contrato específico |
| **Dano / velocidade de ataque** | `hurtEntity` e `FERROUS_HASTE`, contratos distintos | ⚠️ Field Extension por si não alterou constantes de dano/cooldown nas janelas selecionadas |
| **Velocidade/movimento** | `moveTo` de fallback usa `raycast_distance-20F`; movimento provider-native | ⚠️ não tratar deslocamento desejado como velocidade linear/teleporte ou range garantido |
| **Custo e cooldown** | `GalenaGauntletItem.releaseUsing` solicita cooldown de 5 ticks; entidade controla outros intervalos | ⚠️ não converter custos do encantamento em despesa adicional; sem segunda mana nem cast duplicado |
| **Autoridade/ownership** | `GalenaGauntletItem` cria `MagneticWeaponEntity` e associa `ControllerUUID` / `WeaponStack` | ⛔ sem criar cópias ou trocar owner; associação de dano, Mastery e XP deve preservar causalidade |
| **Persistência/rede** | `WeaponStack`, `ControllerUUID`; estados de alvo/progresso e retorno nativos | ⚠️ reload, hand swap, pacote adulterado, entidade órfã e timing client-server sem QA |
| **World safety / performance** | `ProjectileUtil.getHitResultOnViewVector` sob gates de uso da gauntlet | ⛔ não aumentar varreduras por tick, fazer scans globais, contornar `WorldEffectPolicy` ou atingir alvos proibidos |

O **Black Arcana** conserva autoridade sobre seus próprios domínios, casting, Corruption, Strain, Arcane Danger, budgets e política de efeitos. O **Galena Gauntlet e a MagneticWeaponEntity** continuam sob autoridade do provider. O **RPG Skill Tree** é fonte de progressão/atributos/Mastery/perks/gates somente via contrato de interoperabilidade comprovado. Enshrouded não herda essa entidade ou sua autoridade de mira. Nenhuma nova raiz mágica, spell ID, hook executável ou integração provider-native foi adicionada.

## 5. QA e certificação pendentes

1. Confirmar o JSON com datapacks efetivos, níveis I–IV, anvil, mãos, exclusividades e mods que modificam o item em uso.
2. Testar in-game o raycast solicitado (30/35/40/45/50), LOS, obstruções, alvos aliados, PvP, mobs e modded entities, com a gauntlet ativa versus desativada.
3. Homologar o movimento/tempo da arma: seu ponto de fallback, alcance real, retorno de item, chance de hit e desempenho sob TPS baixo.
4. Verificar blocos protegidos, claims, mineração com ferramentas de vários mods, drops, negação de eventos e deduplicação de XP/Mastery; não permitir que perks alterem proteções do mundo.
5. Testar servidor dedicado, sincronização de estado, save/reload, mão principal/secundária, dimensão, desconexão e múltiplas armas controladas antes de aceitar um hook de alteração de alcance.
6. Reconstruir CFG e comprovar uma interface de alteração estável, bounds de distância e autoridade server-side. A CI estática só prova que o JAR SHA-exato conserva os bytes esperados.

**Resultado:** `SHA_EXACT_RESOURCE_AND_SELECTED_JVM_RANGE_CONSUMER` + `PARTIAL_ENCHANTMENT_DOSSIER` / ⚠️; **+1 ficha individual parcial**, **+1 ID literal rastreado**, **+0 contratos estáticos certificados adicionais**, **+0 hooks mutadores**, **+0 raízes mágicas**, **+0 promoção de Stage**. Próxima identidade alfabética: `alexscaves:flinging`.
