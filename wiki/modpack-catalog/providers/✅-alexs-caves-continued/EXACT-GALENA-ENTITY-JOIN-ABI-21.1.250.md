# Galena Gauntlet — ABI oficial de entrada de entidades (NeoForge 21.1.250)

**Estado:** ⚠️ subcontrato de interoperabilidade **estático, parcial e somente leitura**. Este dossiê **não** certifica o objeto Galena, hooks mutadores, aplicação de efeitos, segurança do mundo ou QA física. `static_contract=NOT_CERTIFIED` · `mutating_hook=NOT_VERIFIED` · `physical_qa=NOT_TESTED` · `NO_MUTATION` · `provider_universe_closed=false` · `semantic_magic_roots_delta=0`.

## 1. Fronteira e fonte primária exata

A origem da hipótese é **nativa do JAR publisher Alex's Caves Continued 1.0.10**, já auditado: `GalenaGauntletItem.onUseTick` solicita `ItemStack.setCount(0)` sobre a arma oposta **antes** de `ACCompat.createEntity` e de `Level.addFreshEntity`; a janela descarta com `pop` o booleano devolvido por `addFreshEntity`. Ver [dossiê de retorno/drop](EXACT-GALENA-GAUNTLET-RETURN-DROP-1.0.10.md), [pontes ACCompat](EXACT-GALENA-ACCOMPAT-COMBAT-BRIDGES-1.0.10.md) e [ficha individual](equipment/galena-gauntlet.md). Esses fatos não demonstram perda real da arma nem um problema reproduzido em gameplay.

Para delimitar **a possível influência de um evento da engine**, foi lido independentemente o pacote oficial de **NeoForge 21.1.250**, sem executar o Minecraft transformado:

| Artefato Maven oficial | Tamanho | SHA-256 | Entradas ZIP |
|---|---:|---|---:|
| `neoforge-21.1.250-universal.jar` | 3.551.255 B | `1f9cc68fe9ec0416475d34ce76e95a696b9721d5d338168563dab0632c3d2956` | 2.521 |
| `neoforge-21.1.250-sources.jar` | 1.796.948 B | `a2811d794544ec67dc3fa43b900158f058ea534881ba1c160373554384311a0d` | 1.978 |

Fonte: [Maven oficial do NeoForge 21.1.250](https://maven.neoforged.net/releases/net/neoforged/neoforge/21.1.250/). O SHA-256 do arquivo de fonte `net/neoforged/neoforge/event/entity/EntityJoinLevelEvent.java` nesse `sources.jar` é `63f3a66ce430bc4ca49ae03190733f95baad7387a85c5417450d9947acca929f`; **não** se copia o corpo da implementação. O artefato `universal` possui os classfiles auditados abaixo. O `userdev` da mesma versão tem um escopo próprio de patches NBT, documentado [separadamente](EXACT-GALENA-ENGINE-PATCH-FOOTPRINT-21.1.250.md), sem equivalência à execução transformada.

## 2. Classe do evento, construtores e acesso à entidade

A reprodução com Java 21, `javap -p -s`, produziu o relatório de **11.559 bytes**, SHA-256 `405abfa11ac03c82efbd63995ff8ccbce5596d3f1e360f5f95392762d3856d12`. [CI de descoberta #45180679053](https://github.com/Gustavaopere/Black-Arcana/actions/runs/45180679053), job `137713362339`, concluiu com sucesso o censo e a verificação de marcadores fail-closed. A [sonda](../../../../docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_probe.py), [manifesto SHA-exato](EXACT-GALENA-ENTITY-JOIN-ABI-21.1.250.json) e [checker adversarial](../../../../docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_checks.py) possibilitam reprodução; a revisão final da PR deve validar o novo checker na HEAD definitiva.

**`net.neoforged.neoforge.event.entity.EntityJoinLevelEvent`**: classfile SHA-256 `644af7ec062b1497050a50ecb1936aadcf097eb63afd6fa7d56fc7a063e4fe20`, **quatro métodos declarados**, e sua declaração indica a interface `ICancellableEvent`.

| Método declarado | Assinatura JVM | Leitura restrita da ABI |
|---|---|---|
| Construtor `EntityJoinLevelEvent(Entity, Level)` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/level/Level;)V` | Recebe entidade e nível |
| Construtor `EntityJoinLevelEvent(Entity, Level, boolean)` | `(Lnet/minecraft/world/entity/Entity;Lnet/minecraft/world/level/Level;Z)V` | Há um parâmetro booleano; seu significado e default não foram provados apenas pela assinatura |
| `getLevel()` | `()Lnet/minecraft/world/level/Level;` | Acesso declarado ao nível |
| `loadedFromDisk()` | `()Z` | Acesso declarado a booleano, sem confirmação de como todos os caminhos da engine o preenchem |

**`EntityEvent`**: classfile SHA-256 `23e99c7a8e2a144ed15c3c755c6a81403bd677215ccb6c967f6f95fd2d25d86e`, **dois métodos declarados**: `<init>(Entity)` com descriptor `(Lnet/minecraft/world/entity/Entity;)V` e `getEntity()` com `()Lnet/minecraft/world/entity/Entity;`. A referência à entidade na API **não** certifica controller persistido, casting bem-sucedido ou causalidade por jogador.

**`EventHooks`**: classfile SHA-256 `f810377f87c95c04bb4de7a7ac68e8f4862f9ca33a34cc74e067e65e2a92d66b`, **114 métodos declarados**; nenhum método de nome contendo `join` consta no subconjunto selecionado pela sonda, que filtra nomes contendo `join` ou `entity`. Isso **não** prova que o evento não seja emitido por outras classes da engine, nem define sua ordem relativa a `Level.addFreshEntity`. A análise precisa de implementação e callsites reais de Minecraft/NeoForge para afirmar disparo, cancelamento e side.

## 3. Matriz de interoperabilidade para a Gauntlet

| Questão de perícia técnica | O que está provado | O que continua não verificado |
|---|---|---|
| Elegibilidade / cadastro de hook | Evento existe no classfile e sua declaração inclui `ICancellableEvent` | Evento disparado no percurso exato `MagneticWeaponEntity`, ordem, lado servidor, fase e handlers concorrentes |
| Identidade / owner | A API possui `getEntity()` na classe base e `getLevel()` no evento | UUID real do controller após reload, entidade persistida no nível e identidade de jogador confirmada |
| Spawn e integridade da arma | A Gauntlet pede limpeza da stack antes de `addFreshEntity` e descarta retorno booleano | Resultado efetivo do spawn, rollback, cancelamento pela event bus, restituição/duplicação e conservação |
| Itens devolvidos | Publisher usa `Player.addItem` com fallback para `Entity.spawnAtLocation` | Inventário e drop efetivamente aceitos, eventos de pickup, transação entre save/reload e ausência de perda |
| Dano/target/world safety | Publisher usa `ACCompat.hurt`, `Level.destroyBlock` e lógica própria de owner | Dano liquidado, permissão PvP/claim, quebra autorizada e integração com `WorldEffectPolicy` |
| Perks / Mastery | Os métodos fornecem **possível observabilidade de entrada da entidade** | Um boundary seguro, deduplicado e server-authoritative para modificar range/dano/targets/custos ou conceder XP |

Um evento cancelável pode ser utilizado por **outros mods**, incluindo proteção e compatibilidade, porém não é autorização implícita para alterar o fluxo nativo, compensar inventário ou recriar entidade. Interceptar o spawn após a stack já estar zerada, sem contrato de rollback, **pode introduzir perda ou duplicação**; isso é **avaliação de risco**, não defeito confirmado.

## 4. Reprodução e pendências bloqueantes

```sh
# Utilizar somente os JARs oficiais com os SHA-256 registrados acima.
python3 docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_probe.py \
  --universal /caminho/neoforge-21.1.250-universal.jar \
  --sources /caminho/neoforge-21.1.250-sources.jar \
  --javap /caminho/java21/bin/javap \
  --output /diretorio-novo/galena-entity-join-report.json

python3 docs/qa/alexscaves_1010_galena_neoforge_entity_join_abi_checks.py \
  --report /diretorio-novo/galena-entity-join-report.json \
  --manifest 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-GALENA-ENTITY-JOIN-ABI-21.1.250.json' \
  --adversarial
```

A CI verifica a integridade dos downloads contra os checksums publicados pelo Maven e os digests SHA-exatos do relatório. O teste adversarial ataca mudanças de versão/classe/assinatura e falsas promoções de status; **não** executa gameplay. O relatório JSON detalhado é um artefato temporário da CI; manifesto e checker permanecem versionados.

**Próximas provas necessárias:** (1) callsites reais de emissão/cancelamento e retorno de `Level.addFreshEntity` em Minecraft 1.21.1 / NeoForge 21.1.250 transformados; (2) teste servidor dedicado/cliente em negação de spawn e claims; (3) inventário cheio, falha de spawn, logout, reload, troca de dimensão e drop; (4) verificação da paridade do JAR físico instalado com o publisher; (5) avaliação de event listeners de outros mods na modlist. Até então, **`NO_MUTATION` / fail-closed**, contrato da Galena ⚠️ parcial, **130/134** contratos no recorte e **nenhum novo root** ou incremento do índice global.
