# Contrato de fichas técnicas — magias, poderes e habilidades para perks

**Escopo:** Black Arcana cataloga ações mágicas e superfícies de interoperabilidade de mods instalados. Para engenharia de perks, também são objetos de pesquisa habilidades não mágicas (por exemplo, Epic Fight), **sem alterar o numerador semântico de magia**. Este documento complementa `wiki/TEMPLATE-SPELL.md`, o ledger `SEMANTIC-MAGIC-COVERAGE.md` e os dossiês individuais; não substitui runtime, Stage STATUS, source ou testes.

## 1. Identidade reproduzível e provenance

Para cada ficha individual (inclusive quando a constatação é negativa), registrar:

- `provider`, `mod_id`, `registry_id` real, tipo de objeto (spell, glyph, ritual, focus, action, skill, passive, relic ability, etc.), escola/categoria, dono da identidade e relações parent/child;
- Minecraft, loader, **versão e nome exatos do JAR físico**, SHA-1/SHA-256 quando disponíveis; URL de publicação e referência de modlist; source commit/tag pinado **se comprovadamente compatível**;
- classe e método declarantes reais, registry/constructor/factory, recurso JSON e permissões/licença de consulta; links permanentes para **linhas reais quando disponíveis**;
- fonte oficial da **descrição para jogador**, com resumo original/parafraseado para preservar clean-room. Distinguir nome de exibição de ID e nunca reproduzir textos proprietários extensos;
- `SOURCE_PINNED`, `RELEASE_BOUNDED`, `COUNTED_EXACT`, `CONDITIONAL`, `EXCLUDED` ou `UNKNOWN` por **objeto**, sem converter identificação binária em prova de execução.

Se uma evidência se aplicar só a um campo, apontar a fonte **nesse campo**. Defaults no source não equivalem a valores da config implantada.

## 2. Pipeline causal obrigatório por habilidade

Documentar as transições que realmente forem verificadas e marcar as demais `NÃO VERIFICADO`:

1. **Ingresso:** keybind, item, scroll, skillbook, API, trigger, client packet, evento e gate de progressão; aquisição no Survival e contextos de ativação.
2. **Pré-validação no servidor:** alvo válido, distância, LOS, facção/PvP, dimensão/chunk, autorização/protection, cooldown/charges, resource availability.
3. **Custos e recursos:** mana, Source, sangue, soul/spirits, stamina, vida, itens, fuel, buffers, reservas, pagamentos, refund/commit, owner e ordem causal.
4. **Lançamento/canalização:** cast time, wind-up, charge, duração, ticks, cast type, animação, interrupt, recast, número de projéteis, cooldown e quando cada etapa é aplicada.
5. **Resolução de alvo:** self/entity/block/ray/projectile/cone/cylinder/area/linked; filtros e geometria efetiva; ponto de origem, raio, largura, altura, profundidade, máximo de alvos, ordenação e hit detection.
6. **Efeito terminal:** dano efetivamente aplicado e `DamageType`/tags; power/level formulas, críticos, knockback, healing, status effects, duração, periodicidade, amplificador, aoE, entidades invocadas, lifecycle, eventos, impacto em blocos/mundo e consequências persistentes.
7. **Eventos derivados:** child-casts, procs, DOT, on-hit/on-kill, callbacks, detonações, bonus hits, rollback e boundaries de deduplicação. O que já está incluído no dano/ação pai **não** é nova identidade.
8. **Saída:** valores resolvidos, state sync, cooldown final, failure modes, exceções, logs/telemetria e testes disponíveis.

Usar unidades explícitas (`ticks`, `s`, `blocks`, `health points`, porcentagem) e separar `base`, `por nível`, `máximo`, `config default`, `config efetiva`, `fórmula`. Para projéteis, distinguir **dimensão de hitbox** (`width/height/AABB`), raio visual, velocidade, aceleração, lifetime, pierce, spread, knockback e explosão. Um tamanho visual não é necessariamente a colisão.

## 3. Matriz para implementação de perks

Toda ficha deve conter uma linha por eixo pertinente (e `N/A` nos não pertinentes):

| Eixo | Valores a localizar | Mudança desejável e evidência exigida |
|---|---|---|
| Dano/tipo | damage formula, tags, source, crit e resistências | bônus, conversão elemental e caps; provar ponto **anterior** ao settlement |
| Alcance | max range, raycast, LOS, teleport safe destination | bônus de alcance sem contornar proteção/loaded-chunk |
| Targeting | kind, filtros, equipe, entity/block, seleção e retarget | single→multi/AOE exige resolver seguro, geometria e limites; nunca inferir hook |
| Área | radius vs dimensions vs block grid, max targets | cap, budget, procs, performance, griefing |
| Projétil | entidade, spawn, AABB, escala, velocidade, lifetime, pierce | separar render scale de hitbox e spawn-server; validar sync |
| Tempo | cast/channel, cooldown, duração, DOT tick, charge | escolher ponto correto; não rearmar procs e não duplicar cast |
| Custos | resource owner, reserva, pagamento, refunds | descontos sujeitos a política transacional; sem segunda mana |
| Summons | owner, cap, duração, AI e custo | não duplicar entidades nem ownership; bounded |
| Estados/mundo | buffs, debuffs, mutações, rollback | respeitar WorldEffectPolicy e proteção do provider |

Para **cada eixo**: `valor/fórmula`, `constante/config`, `classe#método + referência`, `fase server/client`, `boundary real`, `compatibilidade`, `limite`, `teste` e `estado`. Status da superfície:

- `CONFIG_NATIVE`: o provider oferece configuração suportada para o parâmetro exato; não presumir mutabilidade por jogador/perk.
- `HOOK_VERIFICADO`: método/API/evento/boundary público verificado com signature e fase; ainda requer teste do adapter.
- `CONTRATO_CONDICIONAL`: a superfície existe sob versão/config/modpack/condição específica que ainda não foi fechada.
- `SEM_HOOK_SEGURO`: não há extensão confirmada; marcar **⛔ fail-closed**, não substituir efeito por cast paralelo.
- `NÃO_VERIFICADO`: localizar a evidência antes de especificar implementação.

Uma API capaz de **observar** eventos não é automaticamente uma API capaz de **alterar** o cálculo antes do settlement. Um atributo de dano genérico também não prova que tipo de dano, alvo, tamanho ou velocidade sejam mutáveis.

## 4. Ownership dos três projetos

- **Black Arcana:** authority de seu casting, rituais, domains, hazards, Strain, Corruption, Arcane Danger, world safety e estado persistente. Integra mods externos por adapters e contratos reais.
- **RPG Skill Tree:** progression, atributos, Mastery, perks, gatilhos e gates. Perks só alteram runtime de terceiros por seam real e validado, preservando custos, efeitos e autoria do provider.
- **Enshrouded:** continua authority do próprio Shroud/exposure/progressão ambiental e efeitos próprios. Afinidade temática não concede uma bridge mágica; exigir contrato e validação no repo do owner.
- **Providers externos (Iron's, Ars, Epic Fight, Goety etc.):** seguem donos de seus pipelines e recursos. Evitar aplicar dano, mana, stamina, cooldown ou on-hit uma segunda vez.

Para conversão `target único → área`, `alteração de tipo de dano` e `redimensionamento de projétil`, manter **⛔ SEM_HOOK_SEGURO** até que o método/evento e os side effects do provider demonstrem modificação pré-settlement sem duplicação.

## 5. Definição de concluído e medição

Acompanhar eixos independentes por mod; **não misturá-los**:

- **Cobertura de identidade:** `identidades inventariadas / denominador confirmado da versão`. Pode ser 100% quando o registry foi fechado, mesmo que gameplay seja desconhecido.
- **Cobertura de ficha:** `fichas individuais existentes / identidades alvo`; ficheiros agregados não contam como ficha individual.
- **Cobertura técnica para perks:** `fichas com parâmetros aplicáveis, origem do valor e pipeline causal auditados / fichas aplicáveis`, exigindo lista de campos com `N/A` ou `NÃO VERIFICADO` explícitos. Não contar um link de classe como causalidade verificada.
- **Capacidade de implementação:** `perks com hook real e contrato/tipagem verificados / perks propostos`. Denominador em aberto => `—%`.
- **Aceite físico:** testes em JAR físico/servidor/Survival/cliente são dimensão separada; CI verde de registry não implica integração jogável.

**Barra global solicitada:** usar `objetos tecnicamente concluídos / universo total aplicável` apenas quando ambos forem auditados no mesmo escopo; de outro modo exibir **mínimo confirmado + barra indeterminada (—%)**. Não converter `164/164 diretórios`, `35/39 provas binárias` ou `1.856 objetos mínimos` em 100% do conteúdo. **Barra por mod:** nomear a dimensão (identidade, ficha, técnica ou aceitação) e o status de PR/main.

## 6. Fluxo de auditoria e entrega

1. Reconciliar `main`, `plans/STATUS.md`, modlist física sibling e PRs concorrentes; registrar SHAs.
2. Confirmar ID, versão física e cardinalidade com registry/JAR/source versionado; marcar variações opcionais, datapack e config.
3. Escrever fichas individuais; associar cada valor aos símbolos reais da versão correta; aproveitar auditorias já existentes, sem copiar código/assets.
4. Priorizar primeiro **target, alcance, área, dano/type, hitbox, tempo, cooldown, custos, procs e limites**; não transformar `NÃO VERIFICADO` em conjectura.
5. Construir matriz por perk e só implementar adapters depois de validar hooks reais, ownership e ordem causal.
6. Testar conforme o contrato afetado: unidade, registry/JAR, GameTest, servidor dedicado, Survival/cliente e coexistência. Revalidar a `main` imediatamente antes de merge.

Arquivos canônicos correlatos: `wiki/modpack-catalog/meta/SEMANTIC-MAGIC-COVERAGE.md`, `wiki/modpack-catalog/meta/CATALOG-COVERAGE-CURRENT.md`, `docs/catalog/GLOBAL-MAGIC-CATALOG.md`, `plans/DECISIONS.md` e `plans/STATUS.md`.