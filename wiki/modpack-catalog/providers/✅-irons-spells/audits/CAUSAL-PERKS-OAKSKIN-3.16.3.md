# Iron's 3.16.3 — Oakskin: mitigação no incoming damage, velocidade e origem do elixir

**Identidade:** `irons_spellbooks:oakskin` · Nature · níveis 1–8 · Iron's 1.21.1-3.16.3. ✅ identidade entre as 110 já catalogadas; 🟡 dossiê de causalidade suplementar; ⚠️ fonte fixa examinada, **sem auditoria binária própria nem GameTest desta tranche**; ⛔ alteração de multiplicadores/ordem de damage events sem boundary validado. **+0 magia nova.**

**Proveniência:** `iron431/irons-spells-n-spellbooks@e4056af90302d37eb1739f5ff05020b020e6e252`, Minecraft 1.21.1; [descrição do provider](https://iron.wiki/spells/). Esta ficha descreve interoperabilidade em clean-room, não código reutilizável. O snapshot físico da modlist registra NeoForge **21.1.250**; o `gradle.properties` do Black Arcana referencia 21.1.248. O JAR instalado e a execução física não foram revalidados aqui.

## Root de cast / parâmetros nominais

1. `OakskinSpell` registra `oakskin`, `Nature`, `COMMON`, nível máximo **8**, cooldown default **90 s**. Constructor: `CastType.INSTANT`, `castTime=0`, `baseManaCost=25`, `manaCostPerLevel=10` → **25–95 mana** para níveis 1–8; `baseSpellPower=20` e `spellPowerPerLevel=3` → **20–41 unidades nominais** antes dos multiplicadores. [Fonte de defaults](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/OakskinSpell.java#L32-L67). O custo/tempo real pertence ao pipeline e às configurações de Iron's.
2. O `onCast` é **self**, sem raycast, alvo remoto, projétil, AoE ou raio mutável. Remove `OAKSKIN` e `OakskinData` preexistentes e reaplica `MobEffectRegistry.OAKSKIN` por `(int)(getSpellPower(level,caster)*20)` **ticks**, com `amplifier=2` fixo. Dispara `OakskinParticlesPacket` e `super.onCast`; não são casts adicionais. [Fonte de cast e amplifier](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/spells/nature/OakskinSpell.java#L84-L105).
3. Duração default neutra **400–820 ticks = 20–41 s**; esta faixa não fixa a duração no modpack com atributos/config. Não inferir aumento da redução percentual com **nível**: neste método o amplifier é sempre `2`, enquanto spell power escala principalmente **duração**.

## Cadeia de dano e atributos

- `OakskinEffect.reduceDamage(LivingIncomingDamageEvent)` localiza `OAKSKIN` na **vítima** e multiplica `event.getAmount()` por `1 - getReductionAmount(amplifier,victim)` usando `setAmount`. O listener opera em **dano recebido**, não no evento raiz de cast nem em dano causado. Partículas por ocorrência não são evidência de HP efetivamente reduzido. [Evento](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/OakskinEffect.java#L37-L49).
- Fórmula de redução na fonte: `min(0.75f, (0.10f + 0.05f * amplifier) * multiplier)`. Com amplifier `2` e `multiplier=1`, resulta **20%**; limite local **75%**. `multiplier` é obtido de `SpellRegistry.OAKSKIN_SPELL.get().getEntityPowerMultiplier(victim)`; caso `OakskinData.hasFromElixir(victim)`, é forçado a **1**. Não assumir redução constante de 20% sob outros atributos, nem que percentagem mostrada seja mitigação líquida após armadura/outros listeners. [Fórmula e elixir](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/OakskinEffect.java#L51-L64).
- `MobEffectRegistry.OAKSKIN` registra modificador de `Attributes.MOVEMENT_SPEED` usando `ADD_MULTIPLIED_TOTAL`, `-OakskinEffect.SLOWNESS_MAGNITUDE`; magnitude estática `0.25` (**−25%** no modificador da velocidade). É um segundo canal do **mesmo** buff, distinto do listener de dano. [Registro do efeito](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/registries/MobEffectRegistry.java#L43-L48), [constantes](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/OakskinEffect.java#L21-L25).
- `OakskinData` lê/escreve/remove o attachment `OAKSKIN_FROM_ELIXIR`. A remoção do efeito chama `OakskinData.remove`; a própria aplicação do spell também limpa essa origem. Interação entre elixir, renovação e logout é dependente do lifecycle físico e **não** está demonstrada por leitura de fonte. [Attachment](https://github.com/iron431/irons-spells-n-spellbooks/blob/e4056af90302d37eb1739f5ff05020b020e6e252/src/main/java/io/redspace/ironsspellbooks/effect/OakskinData.java#L7-L23).

## Matriz de perk / causalidade

| Eixo | Ponto de extensão observado | Classificação |
|---|---|---|
| Tempo do buff | `getSpellPower` calcula ticks | **A condicionado:** atributos nativos podem afetar potência/duração; não existe nesta fonte setter separado de duração por perk |
| Mitigação | listener `LivingIncomingDamageEvent.setAmount` | **B observado como listener provider**, não como autorização de mutar seus valores; ordem/precedência externa ⚠️ |
| Mobilidade | modifier `MOVEMENT_SPEED` do efeito | **A:** usar atributos nativos contratados; duplicação de slow no RPG ⛔ |
| Elixir ↔ spell | `OakskinData` + remove/reapply | **C:** integração de origem e persistência exige teste de refresh/elixir |
| Troca de alvo, área ou bônus duplo | cast exclusivamente self | **D/⛔:** sem seam real, não substituir seleção nem aplicar redução adicional |
| Mastery | 1 cast → 1 buff → N eventos de dano recebido | **D/⛔:** N eventos não equivalem a N casts; não premiar partículas ou hits vetados |

**Dedupe e segurança:** um `LivingIncomingDamageEvent` pode ser reprocessado por outros mods; observar redução proposta não prova dano aceito/HP perdido. Não criar pipeline paralelo, segundo custo nem proc ofensivo ao receber dano. Recomenda-se um único token de cast admitido do Iron's, caso seja realmente verificável, e um identificador de evento/hit para evitar double-counting; ambos **NÃO VERIFICADOS** neste caminho.

## QA físico pendente

- [ ] Conferir no JAR **instalado** o mod ID, versão, SHA e equivalência com `OakskinSpell`, `OakskinEffect`, `MobEffectRegistry`, `OakskinData`.
- [ ] Medir redução real: damage permitido vs cancelado, zero amount, power neutral/alto, cap 75%, dano indireto/DoT, resistência e outros listeners.
- [ ] Testar ciclo elixir → spell → remoção antecipada → refresh/relog e eventual preservação ou limpeza do attachment; demonstrar velocidade −25% no servidor.
- [ ] Confirmar custos/cooldown e um único crédito de Mastery em cast aceito, não a cada hit; servidor dedicado/cliente/Survival e políticas PvP/claims.

**Estado:** fonte versionada ✅; classfile exato deste caminho ⚠️ pendente; runtime e integração condicionados, Stage 06.05 🟡, sem promoção.
