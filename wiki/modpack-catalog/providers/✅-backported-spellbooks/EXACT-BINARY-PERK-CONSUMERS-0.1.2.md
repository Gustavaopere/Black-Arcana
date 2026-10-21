# Backported Spellbooks 0.1.2 — três caminhos compilados relevantes para perks

**18/10/2026 · ✅ `EXACT_PUBLISHER_BYTECODE_BOUNDED_METHODS` · ⚠️ execução de habilidades, danos, tempo real e compatibilidade de host NÃO VERIFICADOS · ⛔ adapters RPG/Black Arcana sem boundary.**

## Artefato e execução reproduzível

- Versão publicada/filename: `backportedspellbooks-0.1.2.jar`; metadata NeoForge embutida **`0.1.0`**, discrepância já registrada. Mod ID `backportedspellbooks`. CurseForge projeto **1543731**, arquivo **8158731**.
- O [workflow Java21 #39131725388](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131725388) terminou em **SUCCESS** com **8/8 autotestes**, `PASS_BACKPORTED_012_BOUNDED_COMPILED_PERK_CONSUMERS`, `deviations=[]`. Validou **SHA-1 `747847c1f38c73250ebac05ea06b41a381187850`** e tamanho físico **209.868 bytes** antes de inspecionar as classes. Não é um dump novo do filesystem do jogador; é igualdade exata do JAR publisher com o hash do último snapshot físico.
- Relatório JSON [artefato **#12138535465**](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131725388/artifacts/12138535465), sem redistribuição do JAR oficial.
- [Verificador Python de método delimitado](../../../../docs/qa/backported_012_perk_consumer_bytecode.py) e [workflow](../../../../.github/workflows/backported-spellbooks-012-perk-bytecode.yml). Confronta métodos físicos via `javap -p -c`, sem importar o código de execução de terceiros ao Black Arcana. Autotestes negativos alteram cardinalidade, proprietário das chamadas, constante aritmética, armazenamento da sessão e hash.
- A tentativa anterior [#39131655290](https://github.com/Gustavaopere/Black-Arcana/actions/runs/39131655290) aprovou os oito testes e o gate do JAR, mas falhou na publicação do relatório porque havia uma barra invertida no **nome do artefato CI**. O problema do workflow foi corrigido e a segunda execução completou com sucesso. A falha não foi do JAR, nem da magia.

## Provas binárias delimitadas

| Provider method | Evidência no binário 0.1.2 | Conclusão restrita |
|---|---|---|
| `SulfurCloudProjectile.tick()` | Exatamente **duas** instruções `invokespecial ...tick:()V` com mesmo proprietário compilado antes de `createParticleSphere()` | As duas invocações ao método pai estão no corpo compilado. **Não** prova duplicação exata de física, lifetime, hit cadence ou dano aplicado no mundo, que dependem do host e estado da entidade |
| `SulfurReleaseSpell.getWitherAmplifier(int,LivingEntity)` | Sequência `iload_1; iconst_2; isub; ireturn` sem instruções extras | O método físico devolve **`spellLevel-2`**. Para parâmetro `spellLevel=1`, resultado do **método** é **-1**. O tratamento do amplificador negativo pelo `MobEffectInstance` e Iron's/NeoForge não foi testado |
| `ResinSpraySpell.onCast(...)` | Callsite ordenado de `MagicData.isCasting`, `getCastingSpellId`, `getAdditionalCastData`, `EntityCastData.getCastingEntity` com checks de `instanceof EntityCastData` e `AbstractConeProjectile` | O método compilado contém caminho para consultar sessão e o tipo do projétil; condições observadas **no bytecode**, não em jogador |
| `ResinSpraySpell.onCast(...)` | `AbstractConeProjectile.setDealDamageActive` precede `new ResinSprayProjectile`, `Level.addFreshEntity` e `MagicData.setAdditionalCastData` | Os caminhos de reativação e criação/registro estão presentes e em ordem. A presença de ambos **não prova** que uma cast real sempre reutiliza só uma entidade, nem fornece hook externo para estender a sessão |

## Consequências para o padrão de dossiê técnico

**Sulfur Clouds:** a ficha passa a registrar o `super.tick` duplicado como **fato binário**, mas o efeito temporal concreto ainda é ⚠️. Três projéteis source-pinned por cast não autorizam três créditos de Mastery. A leitura de `hitsPerTick`, coleção `victims`, `lifetime=100`, velocidade e event hooks dos projéteis ainda depende de prova causal mais profunda no JAR e QA de mundo.

**Sulfur Release:** `spellLevel-2` é um parâmetro binário confirmado, com amplitude negativa no nível 1 na saída do método. Não inferir que a entidade recebe buff/debuff com nível negativo sem observar o consumidor `MobEffectInstance`, normalização, datapack e aplicação real. Duração, raio, friendly fire e LOS permanecem como valores source-pinned da mesma data da release, **não** automaticamente promovidos por este gate.

**Resin Spray:** estado de casting e `additionalCastData` são host-native de Iron's. Uma perk de duração/intervalo de dano, quantidade ou alvo **não** deve clonar o projétil nem registrar novo cast por callback de continuação. `setDealDamageActive` no classfile não constitui API pública de integração; sem teste de intenção/início/continuação/cancelamento, callback causal ou hook seguro, ficar **⛔**.

## Autoridades e pendências

- Iron's possui casting, mana, cooldown, `MagicData`, networking e lifecycle de `AbstractConeProjectile`.
- Backported Spellbooks possui as seis definições semânticas, execução específica, projéteis e efeitos.
- RPG Skill Tree só pode prover progressão, perks, Mastery e gates por contrato; Black Arcana mantém apenas o próprio runtime mágico. Não dobrar mana, procs, damage settlement, casts nem Mastery.

**Não provados:** execução com player conectado, efeito de `super.tick` no host Iron's 3.16.3, amplificador normalizado, valores finais de dano ou vida, velocidade e alcance, compatibilidade full modpack, fonte↔JAR completamente equivalente, configuração efetiva e estabilidade de API. O gate é **estático**, não a aceitação Stage 09.

**Barras:** global **—%** (piso 1.857 semânticos / 1.855 estritos, denominador integral aberto); Backported Spellbooks **6/6 IDs registrados** e **6/6 fichas source-pinned**, **3/6 identidades com os consumidores especificamente auditados neste novo gate**. Os 3/6 não representam metade da integração. **+0** novas magias, **+0** adapters. Stage 06.05 🟡, Stage 09 físico ⚠️ PENDING, PR #825 draft, sem merge.
