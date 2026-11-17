# Alex's Mobs Continued 2.1.13 — ciclo de vida do portal do Dimensional Carver

**Escopo:** auditoria do classfile publisher SHA-exato, read-only, de `ItemDimensionalCarver` e `EntityVoidPortal`. **Estado:** 🟡 descoberta parcial. **Não** é certificação estática de todas as dependências, QA física, API/hook de perk ou prova de segurança do teleporte.

## Autoridades

- Modlist física do sibling, linha 021: `alexsmobs-2.1.13-neoforge+1.21.1.jar`, mod ID `alexsmobs`, Minecraft 1.21.1 / NeoForge / Java 21.
- Publisher CurseForge projeto 1635121, file 8856498: SHA-1 `50ddafdf3d12b33331e4eecb4ab514ae451baadd`; SHA-256 `eef0b4d36f1e40292b23f90ad3052e2e9aace3a33c6a48c65b8b5f2b061ab6c8`; 27.452.738 bytes.
- Auditoria de referência do mesmo JAR: [EXACT-2.1.13-ARTIFACT-AUDIT.md](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-2.1.13-ARTIFACT-AUDIT.md), prova non-merge PR #511 (GitHub Actions `36949047824`), e [controle de operandos](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-CONTROL-OPERANDS-2.1.13.md).
- **A fonte pública `2.2.3` não é autoridade para o JAR `2.1.13`.** Tampouco a última release `2.2.4` altera a versão física documentada na modlist.

## Lacuna técnica e motivo

O cartão individual [Dimensional Carver Passage](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/actions/dimensional-carver-passage.md) documenta `onPortalOpen` atribuindo lifespan inicial de **1200 ticks**, controle de âncora, ray trace inicial de 1,5 bloco e cooldowns de 40/200 ticks. Porém **atribuição inicial não comprova duração efetiva**. Faltam especialmente a implementação exata de `EntityVoidPortal`, seus decrementos, invalidação, lifecycle de destino/entidade e eventual serialização, além de avaliação física de teleport/claims.

## Procedimento de coleta

[Probe read-only](alexsmobs_213_carver_portal_lifecycle_probe.py) e [12 regressões sintéticas](alexsmobs_213_carver_portal_lifecycle_probe_test.py) implementam:

1. Gate estrito de SHA-1, SHA-256, tamanho, versão JVM 65 e paths de classe `ItemDimensionalCarver` e `EntityVoidPortal` do artefato instalado;
2. Inspeção de todos os seis métodos próprios conhecidos do Carver (sem publicação de corpos completos) e descoberta **limitada** dos métodos de ciclo de vida do portal a partir do bytecode real;
3. Registros compactos de métodos, digest das instruções JVM, desvios, referências simbólicas e seus vizinhos imediatos, com limites explícitos de quantidade e bytes;
4. Manifesto JSON SHA-exato fixado **após** conferência da descoberta, replay de CI com `--snapshot` e manutenção dos índices globais sem promoção.

O [workflow](../../.github/workflows/alexsmobs-213-carver-portal-lifecycle.yml) obtém o mesmo publisher usado na prova #511, sem comitar bytes de terceiros, executa testes sob Java 21 e conferências de índices.

## Gates não satisfeitos nesta primeira coleta

`static_perk_contract=NOT_CERTIFIED`, `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `mutation=NO_MUTATION`. A ação é dependente da cadeia do Void Worm para obtenção normal; os parâmetros da config *implantada* e overrides permanecem `NOT_VERIFIED`.

**Proibido inferir:** dimension hopping arbitrário; bypass de claim; destino validado pelo servidor; tempo efetivo de vida igual ao valor inicial; aceitação do spawn; cardinalidade do teleporte; logout/save/reload; hook mutador; ou QA real apenas de um callsite.

Após a descoberta, qualquer afirmação substantiva nova deve indicar offset/descritor e classe revisados do classfile 2.1.13, com limites claros. Não editar Raygun/X-Ray ou os índices 80/81 do Alex's Caves.

## Resultado verificado — JAR 2.1.13 / CI #44013379631

A [descoberta física executada em Java 21](https://github.com/Gustavaopere/Black-Arcana/actions/runs/44013379631) terminou com **14/14 regressões sintéticas**, validação SHA-1/SHA-256/tamanho da versão da modlist, classes JVM major 65, inspeção de **duas classes**, **23 métodos com ABI/descritor/hash**, **121 referências selecionadas**, checagem dos índices existentes e nenhuma mutação. A evidência compilada está selada em [EXACT-CARVER-PORTAL-LIFECYCLE-2.1.13.json](../../wiki/modpack-catalog/providers/✅-alexs-mobs-continued/EXACT-CARVER-PORTAL-LIFECYCLE-2.1.13.json). Os hashes SHA-256 individuais são:
- `ItemDimensionalCarver.class`: `36295a531101875388114059940f6161d0afc808118c2344def04d732db88e6f`, 12 métodos declarados, sete method entries selecionadas (dois overloads de `getUseDuration`);
- `EntityVoidPortal.class`: `09796124461bfdde10766ca0e53c00f68ec00a6b13d79289c7c1a5c8652e29b5`, 24 métodos declarados, 16 method entries selecionadas; `tick()V` tem **418 instruções JVM e 34 desvios**.

### Duração e descarte: início não equivale a vida efetiva

1. O `ItemDimensionalCarver.onPortalOpen` escreve lifespan inicial **1200** via `EntityVoidPortal.setLifespan @4` (confirmado também por manifesto anterior).
2. **Fallback distinto da classe portal:** `EntityVoidPortal.tick` invoca `Entity.tick @1`, consulta `tickCount @5`, `if_icmpne @9 → 26`. Quando `tickCount == 1`, consulta `getLifespan @13`; se o valor for zero (`ifne @16 → 26` não salta), grava `setLifespan(2000) @23`. **2000 é fallback condicionado no primeiro tick quando o lifespan é zero**, não a duração sempre atribuída ao Carver.
3. O `tick` executa `getLifespan @858`, `iconst_1 @861`, `isub @862` e `setLifespan @863`: decremento de 1 no caminho alcançado. `getLifespan @925`, `ifgt @928 →938`, `Entity$RemovalReason.DISCARDED @932` e `Entity.remove @935` mostram o caminho de descarte quando o contador resultante não é positivo.
4. Há **outro modificador interno**: quando um candidato à interação passa pelo ramo de `EntityVoidWormPart` (`instanceof @687`) e o lifespan é menor que 22 (`getLifespan @694; bipush 22 @697; if_icmpge @699 →853`), o método incrementa lifespan por 1 (`@704–709`). Isso impede inferir um número fixo de ticks de vida apenas de `onPortalOpen` e do decremento final. Não foi reconstruída uma prova completa das condições externas desse ramo.

### Targeting, teleporte e gates de lado lógico

O fluxo do `EntityVoidPortal.tick` possui gate `Level.isClientSide @537 / ifne @540 →856`: o grupo de consulta/teleporte examinado aparece no ramo não-cliente. Ele exige `getDestination @553 != null` (`ifnull @556 →856`), `getLifespan @560 > 20` (`if_icmple @565 →856`) e `tickCount >20` (`if_icmple @574 →856`). Esse `20` é um **gate de janela de utilização**, não um cooldown próprio do BA. O código também consulta `Entity.isOnPortalCooldown @627` e possui exclusões por classe e tags; sem reconstrução de todas as condições, não presumir targeting universal.

O item em `onUseTick` instancia `EntityVoidPortal @265`, inicializa posição, `setAttachmentFacing @318`, tenta `Level.addFreshEntity @327`, invoca `onPortalOpen @341`, chama `AMCompat.hurtAndBreak @351` e `AMCompat.addCooldown @375`. São callsites nativos ordenados; **`addFreshEntity` retorna booleano e o relatório não comprova que seu resultado tenha sido tratado como gate de aceitação** (a chamada é seguida de `pop @330` no recorte). Não concluir spawn aceito, teleporte bem-sucedido ou durabilidade duplicada.

O portal contém `teleportEntityFromDimension(Entity,ServerLevel,BlockPos,boolean)` com quatro branches e referências a `AMTeleportQueue.PLAYERS`, `setPortalCooldown`, `ServerLevel.addFreshEntity` e descarte da entidade de origem. Esse método é uma fronteira importante de movimentação entre dimensões, mas a semântica de `AMTeleportQueue`, transferências interdimensionais e efeitos no multiplayer são **NÃO VERIFICADOS neste recorte**.

### Estado serializado e sincronização

`EntityVoidPortal.getLifespan`/`setLifespan`, `getDestination`/`setDestination`, orientação de anexo e `defineSynchedData` acessam `SynchedEntityData`. A classe implementa **`readAdditionalSaveData(CompoundTag)` (86 instruções, 5 branches)** e **`addAdditionalSaveData(CompoundTag)` (67 instruções, 3 branches)**. Os métodos observados referenciam as chaves `AttachFace`, `Lifespan`, `ExitDimension` e os acessores `DESTINATION`, `ATTACHED_FACE`, `LIFESPAN`.

Portanto existe um **caminho compilado de serialização/reidratação** para parte do estado; isso **não é QA de save/reload** e não demonstra persistência de todos os dados, resolução de dimensões removidas, ausência de portal órfão, sincronização de rede ou segurança sob logoff.

### Impacto e limites

**Dados verificáveis para ficha:** valor inicial de 1200 (Carver); fallback 2000 restrito ao primeiro tick e valor zero; decremento/discard de lifespan; exceção de incremento no caminho `EntityVoidWormPart`; gates servidor/destino/lifespan/idade; presença do caminho nativo de teleporte entre dimensões e das rotinas NBT/synched data.

**Não certificável com esta evidência:** teleporte efetivamente aceito em todos os targets, segurança de world claims, config de obtenção por Void Worm, interações exatas de `AMTeleportQueue`, salvamento em jogo, owner/persistence de viagem, falhas de spawn, e safe hook de modificador de range/tempo/cooldown.

**Resultado final desta etapa:** enriquecimento estático do Carver, sem promover a ficha a ✅. `static_perk_contract=NOT_CERTIFIED`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `NO_MUTATION`. A matriz de três ações de Alex's Mobs mantém `0/3` certificados, 1 `COUNTED_EXACT` e 2 `CONDITIONAL`.
