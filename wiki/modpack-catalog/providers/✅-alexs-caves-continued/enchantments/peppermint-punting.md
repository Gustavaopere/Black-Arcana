# Peppermint Punting — `alexscaves:peppermint_punting` (Alex's Caves Continued 1.0.10)

**Contrato técnico estático individual:** ✅ `STATIC_TECHNICAL_CATALOG_ONLY` / `SHA_EXACT_BINARY_BEHAVIOR`, condicionado à CI que verifica este recorte no JAR SHA-exato. **Hook mutador:** `NOT_VERIFIED`; **QA física:** `NOT_TESTED`; **integração:** `NO_MUTATION`. A ficha fecha a influência deste encantamento no Peppermint Cast e em sua trajetória nativa delimitada; não fecha Multiple Mint, Seekcandy, Spell Lasting, renderer, outros addons ou a totalidade do provider.

## 1. Identidade, origem e descrição original

- **Provider:** Alex's Caves Continued (`alexscaves`), versão **1.0.10**, Minecraft **1.21.1**, NeoForge / Java 21; modlist sibling `alexscaves-1.0.10-neoforge+1.21.1.jar`.
- **JAR publisher:** CurseForge projeto `1645389`, arquivo `8856293`, **75.279.314 bytes**, SHA-1 `6960b299a39a039ac8a5eb9b07be4ad0e3e0a570`, SHA-256 `36ae0a3cbd028df466a37c671ba2fdf021c060ca1c9c1c32e9f2e95bffae0e7c`.
- **JSON:** `data/alexscaves/enchantment/peppermint_punting.json`, **370 bytes**, SHA-256 `ebe5a66b3d69d1d4384149959893712a7458ed9acfcc9064fa58fd16e8ba412b`.
- **Tag de suporte:** `data/alexscaves/tags/item/enchantable/sugar_staff.json`, SHA-256 `eb9f84b401224aba54ba91a239e4dd5b775d82012cecf9b03e8f9608e12b11fc`, contendo somente `alexscaves:sugar_staff`.
- **Descrição literal `en_us.json`:** “Peppermints bounce directly ahead instead of around the attacker”. Tradução explicativa: peppermints tomam trajetória direta para a frente, em vez de orbitar o usuário. O texto é uma descrição do provider; não quantifica distância percorrida ou hits aceitos.
- **Classe produtora:** `com/github/alexmodguy/alexscaves/server/item/SugarStaffItem.class`, SHA-256 `d670f887debdfb95f93a52b0c58b3033154a9aa20777fb8bd2a1673ee1407c3f`.
- **Entidade consumidora:** `com/github/alexmodguy/alexscaves/server/entity/item/SpinningPeppermintEntity.class`, SHA-256 `655e607acf3d22a9caf6be93d9010f7a11c3836e4c680b04878110e61aca4f90`.

O [probe JSON e consumidor](../../../../../docs/qa/alexscaves_1010_peppermint_punting_probe.py) confirmou os valores publisher. O [manifesto binário Multiple Mint](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json), auditado contra o **mesmo** JAR físico, já contém o classfile `SugarStaffItem.use` completo e os consumidores de movimento, targeting, custo, dano e persistência. A [prova individual compacta](../EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json) **reutiliza** essas âncoras sem copiar bytecode; a [ação nativa Peppermint Cast](../actions/sugar-staff-peppermint-cast.md) permanece canônica. O snapshot público `Codx-org/AlexsCavesContinued@523308608422ab8e31974befa7111ecdf495dd37` declara 1.1.1 e não é autoridade para parâmetros do JAR 1.0.10.

## 2. Dados do encantamento no JAR 1.0.10

| Campo publisher | Valor literal | Significado delimitado |
|---|---|---|
| `description.translate` | `enchantment.alexscaves.peppermint_punting` | Chave de tradução |
| `supported_items` | `#alexscaves:enchantable/sugar_staff` | Tag embarcada identifica Sugar Staff |
| `weight` | **2** | Peso declarado, não chance de ativação/dano |
| `max_level` | **1** | Um nível normal publicado |
| `min_cost` | `base=1, per_level_above_first=12` | Nível I: **1** |
| `max_cost` | `base=41, per_level_above_first=10` | Nível I: **41** |
| `anvil_cost` | **4** | Custo declarativo do encantamento, não desgaste por cast |
| `slots` | `mainhand` | Slot declarado |
| `effects` / `exclusive_set` | Não presentes neste JSON | Ausência não prova compatibilidade universal ou ausência de execução em Java |

A registry usa `PEPPERMINT_PUNTING` e o consumer consulta `ACCompat.enchantLevel(stack, PEPPERMINT_PUNTING)`. O predicado compilado em `SugarStaffItem.use @260–268` é **`L > 0`**, não uma multiplicação por L. O método não faz clamp próprio do nível; valores forçados fora do domínio I não estão homologados. A aquisição da Sugar Staff via loot da Licowitch e as tags de encantamento são tratadas na ficha [Peppermint Cast](../actions/sugar-staff-peppermint-cast.md) e no manifesto comum; presença de tags no publisher não comprova aquisição em Survival do modpack.

## 3. Gatilho nativo e diferenças de movimento

`SugarStaffItem.use(Level,Player,InteractionHand)` executa o corpo de spawn/custo sob a guarda `!level.isClientSide()` (`@7–11`). O uso **sem agachar** seleciona Peppermint Cast (`@35–37 → @186`); agachado seleciona Hex. O producer continua usando a mesma quantidade de tentativas `N=3+level(MULTIPLE_MINT)`, com `startAngle=i×360/N` enviado a cada peppermint, independentemente da decisão de Punting. O encantamento Punting não acrescenta peppermints nem muda essa divisão.

**Para cada instância**, antes da inserção, `use` testa Punting em `@262–268`. Parâmetros selecionados:

| Configuração nativa | Sem Peppermint Punting (`L=0`) | Com Punting (`L>0`) |
|---|---|---|
| `setStraight` | **false** (`@314–315`) | **true** (`@273–274`) |
| `setYRot` | `180+(i−1)×30` graus (inteiro antes de float; `@320–332`) | `180F + player.getYHeadRot() + (i−1)×15F` graus (`@279–295`) |
| `setSpinSpeed` no item | **12F** (`@337–339`) | **8F** (`@300–302`) |
| Cooldown inicialmente selecionado no loop | **80 ticks** (`@201–203`) | **20 ticks** (`@305–307`) |
| Raio inicialmente escrito | **3.5F**, ambos (`@381–383`) | **3.5F**, ambos |
| Lifespan de cast | **80 ticks**, ambos (`@410–412`) | **80 ticks**, ambos |

`i` inicia em zero; as fórmulas de yaw registram exatamente o operand `(i−1)`, **não** um espaçamento simétrico reorganizado pelo Black Arcana. A ordem de spawn obedece ao loop nativo, que invoca `Level.addFreshEntity @418` e descarta o booleano em `@421`. São **tentativas**, não projéteis aceitos, hits, DPS ou número de mortes.

**Interação com Seekcandy:** quando a aquisição prévia encontra alvo e `level(SEEKCANDY)>0`, o ramo `@342–377` atribui `seekingEntityId`, troca o speed solicitado no item para **50F** e substitui o cooldown do loop por **50 ticks**. Essa substituição pode prevalecer sobre os **20 ticks** de Punting; não remove explicitamente `setStraight(true)`. Portanto a simples combinação dos nomes não prova trajetória homing final ou compatibilidade física entre os efeitos. A aquisição via `SeaStaffItem.getClosestLookingAtEntityFor(...,32D)` é independente de Punting; **32D não significa alcance máximo garantido do peppermint**.

## 4. Consumidor: trajetória, colisão e dano

A classe `SpinningPeppermintEntity` tem dimensões declaradas **0,8 × 0,4 bloco** em `ACEntityRegistry`. Esses tamanhos são da entidade, não do raio de órbita, da trajetória reta ou da geometria da área de dano.

**Sobrescritas no tick.** No começo de `tick()`, o provider define `setSpinRadius(3F)` (`@63–65`) e `setSpinSpeed(7F)` (`@69–71`), depois captura `getSpinAroundPosition` em um local (`@75–78`). Ramos posteriores podem substituir estado de targeting/radius. Por isso **8F, 12F, 50F e 3.5F são parâmetros iniciais escritos pelo item**, não uma velocidade/raio permanentemente preservados. Um hook que só substituísse `setSpinSpeed` antes do tick não estaria comprovadamente efetivo após essa escrita.

**Movimento straight (`@465–599`).** `isStraight()` seleciona a ramificação; seu processamento de velocidade/movimento é guardado por `Level.isClientSide` (`@473–479`), com trabalho físico no lado não cliente. Usa vetor local `(0,0,−0.01F×getSpinSpeed())`, rotacionado por `−radians(getYRot())`, **somado** ao delta atual. Se tem gravidade, escala o delta por aproximadamente **0.9** e soma **−0.08D** no Y (`@527–552`). Com `verticalCollision`, acrescenta componente vertical aproximadamente **+0.9** e multiplica X/Z por **0.4D** (`@556–585`), então chama `move(SELF, delta)` (`@588–596`). O resultado depende de colisões, tick, nível, gravidade e mundo; não prometer distância retilínea fixa nem movimento constante.

**Movimento orbital alternativo (`@602–733`).** Usa centro capturado, ângulo inicial `startAngle+spinAngle`, raio limitado por `min(1,tickCount/30)×spinRadius` e delta de retorno `(destino−posição)×(0.05D×getSpinSpeed())`, com incremento de `spinAngle`. Trata-se de um branch diferente; Punting positivo escolhe straight no consumer, não altera o multiplicador da órbita.

**Targeting e dano.** `hurtEntities()` consulta `LivingEntity` na **AABB própria** do peppermint, sem inflação radial adicional no método. Exclui owner e aliados nos ramos nativos; Licowitch utiliza seu filtro `isFriendlyFire`. Solicita dano **3F** por `DamageSources.mobProjectile(peppermint,owner)` via `ACCompat.hurt @145`. Apenas retorno true leva ao knockback solicitado `0.30000001192092896D`. Após percorrer candidatos, se houve **qualquer** hit aceito e o ID de seeking não é −1, chama `discard`; não exige que o alvo efetivamente atingido seja o ID selecionado. Punting não fornece DamageType novo, um ataque AoE, uma mudança de PvP/claims, um bônus de dano ou um segundo callback de spell.

## 5. Custo, lifecycle e estado persistido

O cooldown é um pedido ao `ACCompat.addCooldown(Player,stack,ticks)` por **Item** ao final do loop, e não um custo por peppermint, por alvo ou por level. Valores possíveis no caminho observado: **80** sem Punting; **20** com Punting positivo; **50** se o ramo elegível de Seekcandy substitui o anterior. Isso não garante cooldown efetivo sob configs externas ou eventos da engine. Ao final, pede **1 ponto de desgaste de durabilidade** por `ACCompat.hurtAndBreakUsedHand`; a Sugar Staff declara **100** de durabilidade nominal. Não há mana ou stamina adicionadas pelo encantamento nesse consumer.

A entidade usa default lifespan **200**, mas o item escreve **80** no cast. O contador `despawnsIn` começa em −1, é inicializado a partir de `getLifespan` no primeiro tick e decrementado em ticks positivos. O ramo servidor solicita `discard` quando já não positivo, **sem return imediato**; movimento e `hurtEntities` podem seguir no mesmo corpo de tick. Não declarar 80 chamadas garantidas de dano, 80 ticks completos de alcance ou proc garantido por entidade.

O NBT trata `DespawnsIn`, `Straight`, `Lifespan`, UUID de owner, `AroundX/Y/Z`, `SpinSpeed`, `SpinRadius`, `StartAngle` e `SpinAngle`. **Não salva `SEEKING_ENTITY`**. O write do centro usa X/Y/Z, mas o read do classfile constrói **`Vec3(AroundX,AroundZ,AroundZ)`** apesar de verificar a presença de `AroundY`. É uma leitura de bytecode já observada no [contrato Multiple Mint](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.md), não um bug reproduzido em mundo real. Reentrada, continuação do Punting após save/restart e coerência de render/sync requerem QA física.

## 6. Contrato de integração e prova

Possíveis campos observáveis para futuras perks: `direction_mode` (`STRAIGHT` versus órbita), `initial_yaw_formula`, `initial_spin_speed`, `tick_spin_speed_overwrite`, `cooldown_selection`, `projectile_dimensions`, `native_damage_source`, `owner_and_allies`, `persistent_straight` e `seek_state`. Nenhum deles foi certificado como API mutadora.

Não substituir a seleção de `Straight` ou `YRot` por eventos duplicados, nem executar outro `hurt`, outra recarga, outro ciclo de dano, outra entidade ou outro débito. Modificações futuras exigem hook real demonstrado, autorização do servidor, filtros de owner/claims/PvP, limites/deduplicação de casts, persistência, QA de lado lógico e compatibilidade com addons/datapacks. O Black Arcana não assume o runtime nativo do Sugar Staff, e o RPG Skill Tree só pode conceder bônus/gates por contratos comprovados.

**Evidência estática:** [JSON 1.0.10 SHA-exato](../EXACT-PEPPERMINT-PUNTING-CONTRACT-1.0.10.json), [consumer Multiple Mint já auditado](../EXACT-MULTIPLE-MINT-CONTRACT-1.0.10.json), [sonda publisher](../../../../../docs/qa/alexscaves_1010_peppermint_punting_probe.py) e [testes de regressão](../../../../../docs/qa/alexscaves_1010_peppermint_punting_cards_test.py). A certificação é somente **`STATIC_TECHNICAL_CATALOG_ONLY`**, `SHA_EXACT_BINARY_BEHAVIOR`; `mutating_hook=NOT_VERIFIED`, `physical_qa=NOT_TESTED`, `NO_MUTATION`, universo do provider não encerrado.
