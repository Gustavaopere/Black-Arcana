# Missile — engenharia de perks, Not Enough Glyphs 4.6.2

**ID de registro:** `arsomega:glyph_missile` · **Classe:** `alexthw.not_enough_glyphs.common.glyphs.forms.MethodMissile` · **Mana default (fonte):** **20** · **Tier:** II · **Estado:** ✅ fallback porque arsomega ausente; ⚠️ config/execução.

**Fonte 4.6.2:** [common/glyphs/forms/MethodMissile.java](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/forms/MethodMissile.java), [registro condicional](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/init/ArsNouveauRegistry.java) e [prefixo de IDs](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/glyphs/CompatRL.java). Pin `45604dd18d9d2e3e7ca80a2c616b3309f42aca77`. Defaults do source não equivalem ao débito efetivo do servidor.

## Mecanismo causal e números verificáveis

- `summonProjectiles` cria `1+count(Split)` instâncias `MissileProjectile`, com velocidade `max(0.1,0.75+accMultiplier/2)`, `Dampen` ativa gravidade e `maxAge=(int)max(5,30+7*durationMultiplier)` **em ticks**, não segundos. `MethodMissile.buildConfig` declara `max_lifespan=60` segundos mas o método de criação **não lê esse campo** diretamente.
- [`MissileProjectile.java`](https://github.com/Alexthw46/NotEnoughGlyphs/blob/45604dd18d9d2e3e7ca80a2c616b3309f42aca77/src/main/java/alexthw/not_enough_glyphs/common/spell/MissileProjectile.java) publica `SpellProjectileHitEvent` cancelável; ignora owner; processa impacto em bloco ou entidade, com ramificações de `IPrismaticBlock`, portal e Target Block. Ao exceder `maxAge`, chama `ExplodeMissile` antes de descartar.
- `activateSpellAtPos` busca todas as `LivingEntity` na AABB com semi-eixos `5+1.3*aoe` em X/Z e `2+aoe` em Y; exclui caster do contexto. Resolver é aplicado a **cada** entidade; se nenhuma e `activateOnEmpty=true`, emite hit de bloco sintético. `maxAge` e `aoe` são gravados em NBT.
- Augments declarados: Pierce, Split, Accelerate, Sensitive, Reduce Time, Extend Time, AOE, Dampen. Evento de hit/projétil não dá licença a segunda cobrança nem a Mastery múltipla; deduplicar launch→projectiles→effects.

## Interoperabilidade e evidência

- **Authority:** Ars Nouveau/Not Enough Glyphs/Sauce executam a spell, calculam custo e liquidam efeitos. Black Arcana não deve repetir o cast, aplicar o mesmo dano/efeito novamente nem criar outro ledger de mana. RPG Skill Tree só assume progressão, Mastery e perks através de um contrato real.
- **Perks:** parâmetros nativos identificados no código-fonte **não** são hooks comprovados. API/evento de mutação para esta identidade: **NÃO VERIFICADO**; adapter RPG: **⛔ NÃO IMPLEMENTADO (fail-closed)**. Requer caps/budgets, identidade causal e testes antes de alterar alcance, custo, dano ou número de efeitos.
- **Estado:** código-fonte público declarado 4.6.2 localizado, mas corpos compilados no JAR físico, configurações SERVER efetivas, execução dedicada/GameTest, claim/PvP, Save/Restart e Survival **⚠️ NÃO TESTADOS neste lote**. O pacote físico indicado no catálogo é `not_enough_glyphs-1.21.1-4.6.2.jar`, SHA-1 registrado `32eea2c478a346ee7499f6a0db156241116f73e9`. Nenhuma identidade nova.
- **Clean-room:** apenas fatos, parâmetros e localizadores; sem cópia de implementação ou assets.

[Matriz 4.6.2](../../../PERK-ENGINEERING-MATRIX-4.6.2.md) · [Padrão global](../../../../../meta/PERK-READY-TECHNICAL-STANDARD.md).
