# Sea Swing 1.0.10 — contrato individual estático SHA-exato

A [ficha individual](enchantments/sea-swing.md) reúne os sete eixos de catálogo para design de perks: identidade, comportamento, parâmetros, alvo, custos, integração e validação. **Não** aprova hook mutador, execução física ou paridade de fonte.

**Autoridade:** JAR publisher `alexscaves-1.0.10-neoforge+1.21.1.jar` (CurseForge projeto 1645389, arquivo 8856293), 75.279.314 bytes; SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`. Fontes adjacentes de versão 1.1.1 não fornecem números para a versão física instalada.

O [manifesto estático](EXACT-SEA-SWING-STATIC-1.0.10.json), criado a partir de `javap -p -s -c`, contém métodos próprios selecionados **com todos os offsets e instruções**, dois construtores e a localização exata de `en_us.json`; confere SHA de três classfiles e todas as janelas anteriores do [manifesto de descoberta](EXACT-SEA-SWING-DISCOVERY-1.0.10.json). A [sonda estática](../../../../docs/qa/alexscaves_1010_sea_swing_static_probe.py) executa comparação de igualdade com `--seal` no JAR; os [testes](../../../../docs/qa/alexscaves_1010_sea_swing_static_probe_test.py) rejeitam identidade, janela e fluxo de aceitação corrompidos.

| Caminho | Prova selecionada | Limite |
|---|---|---|
| OrtholanceItem.hurtEnemy / acHurtEnemy | 6/49 instruções completas; gate level positivo `ifle @23`, desgaste MAINHAND 1 anterior ao gate, criação de uma WaveEntity, lifespan 5, yaw e pedido de spawn com retorno descartado | Callback sem `isClientSide` explícito; spawn efetivo não certificado |
| WaveEntity(Level,LivingEntity) e (EntityType,Level) | Dois corpos de construtor completos; owner recebido em `setOwner @18`, UUID capturado | Não assumir que o campo objeto permaneça acessível após reload |
| WaveEntity.defineSynchedData, getDimensions, onSyncedDataUpdated | Defaults SLAMMING=false, LIFESPAN=10, WAITING_TICKS=0, Y_ROT=0, WAVE_SCALE=1; dimensões escaladas e refresh quando alteradas | Datapacks, chunks, entidades externas e QA física não observados |
| WaveEntity.getSlamAmount / tick | Interpolação do slam `×0,1`; tick no servidor chama attackEntities; guardas de espera, slam/discard, gravidade, arrasto, movimento e lifespan | Duração configurada não é vida física garantida |
| WaveEntity.attackEntities | 81 instruções completas: AABB inflada 0,5D por eixo, fonte `mobProjectile`, exclusões owner/aliados/Deep One, dano `S+1` solicitado e `hurt` booleano ignorado antes de setSlamming e knockback | Não equivale a dano aceito, kill, proc ou empurrão confirmado |
| WaveEntity.read/addAdditionalSaveData e getOwner | NBT próprio só Owner(UUID)/Lifespan; getter resolve UUID no ServerLevel se chamado; `attackEntities` usa campo owner direto | Não comprovar restauração automática da autoria nem créditos de Mastery/XP após reload |

**Parâmetros-chave:** `S = 2 × getSlamAmount(1F) + 1 + waveScale`; `hurt` recebe `S+1` e o helper knockback recebe `0.1D + 0.5D × S`. Com escala default 1, dano bruto pedido `3 + 0.2 × slamProgress`. Não há adição direta por nível Sea Swing acima do predicado positivo. A AABB própria da onda, sua escala e seu movimento não devem ser confundidos com um valor de alcance de cast.

**Dados publisher:** JSON `sea_swing.json` de 360 bytes (SHA-256 `f5e7985f7941b02a47966fa1135f3fc3ceff05b60d9eee015cbb6b33c7eb9c3a`), peso2, máximoI, min-cost1/10, max-cost41/10, anvil4, slot mainhand, item tag Ortholance; campo exclusivo ausente desse recurso. Descrição oficial da localização `en_us.json` extraída, parafraseada na ficha, com SHA-256 `a2a3fab567b07ec10b3d946d4e4ce3e65417b6f9348bd49478d8a253a4232d1f`.

**Validação e limites:** `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`. Sem autorização de reexecutar hurt, gerar WaveEntity extra, cobrar custo próprio, alterar area/hitbox, reagendar hit ou acrescentar cast/raiz independente. Regras PvP, world protection, aceitação real de eventos/dano, reload em multiplayer, outcomes de spawn, compatibilidade e QA física ficam pendentes de verificação específica. Nenhuma promoção de Stage, gameplay, Java do mod ou runtime do RPG Skill Tree.

```sh
python3 docs/qa/alexscaves_1010_sea_swing_static_probe.py \
  --jar /caminho/para/alexscaves-1.0.10-neoforge+1.21.1.jar \
  --javap javap \
  --seal 'wiki/modpack-catalog/providers/✅-alexs-caves-continued/EXACT-SEA-SWING-STATIC-1.0.10.json'
```
