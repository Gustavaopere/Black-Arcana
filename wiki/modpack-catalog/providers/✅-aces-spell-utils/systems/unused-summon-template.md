# ExampleSummonSpell — template de summon NÃO registrado

**Classe:** `ExampleSummonSpell extends AbstractSummonSpell`. **Identificador declarado:** `aces_spell_utils:example_summon_spells` (plural). **Estado:** ⚠️ classe de demonstração não utilizada, sem `registerSpell` nesta versão. A presença do ResourceLocation não estabelece magia disponível no jogo.

## Parâmetros declarados no source

| Campo | Valor declarado | Interpretação autorizada |
|---|---|---|
| Escola default | Iron's NATURE | Configuração de exemplo; sem registro ativo |
| Raridade mínima | LEGENDARY | DefaultConfig do exemplo |
| Nível máximo | 1 | Configuração do exemplo |
| Cooldown default | 200 segundos | Do `DefaultConfig`, não cooldown observado em jogo |
| Tipo de cast | `CastType.LONG` | Tipo declarado pelo exemplo |
| `castTime` | 80 | Campo Java; efetividade dependente do host |
| `baseManaCost` / `manaCostPerLevel` | 200 / 20 | Campos declarados; cobrança efetiva não testada |
| `baseSpellPower` / `spellPowerPerLevel` | 10 / 5 | Campos declarados; não são dano confirmado |
| `summonTimer` | 12.000 ticks | Constante em `onSummoningCast`; 10 min nominais a 20 TPS |
| Quantidade solicitada | `spellLevel` | Um `SummonedSkeleton` construído por iteração, se executado |
| Posição proposta | X/Z = eyePosition + gaussian × 3; Y = eyePosition.Y | Dispersão aleatória, não raio máximo garantido |

## Targeting, efeitos e integração

Na execução hipotética de `onSummoningCast`, tenta gerar `SummonedSkeleton(level, caster, true)` por `spawnHelper`, retorna `summonTimer` e associa o cast data do Iron's. A distribuição gaussiana de X/Z **não** fixa um alcance máximo ou AOE de impacto; quantidade gerada, lifetime efetivo, custos transacionais e regras de spawn dependem do helper/host. Não há projétil, dano ou hitbox diretamente definidos nesta classe.

**Não colocar em árvore de perks como spell desbloqueável:** o source comenta explicitamente que não é utilizado. O exemplo pode orientar perguntas sobre `spawnHelper`, mas nenhuma integração deve reproduzir o corpo de um mod nem disparar spawn adicional.

**Fonte exata:** [`spells/ExampleSummonSpell.java`](https://github.com/AceTheEldritchKing/Aces_Spell_Utils/blob/a0b2f4c2fcfa938c8e47239279c77c2ef82647ac/src/main/java/net/acetheeldritchking/aces_spell_utils/spells/ExampleSummonSpell.java).

**Proveniência:** AceTheEldritchKing/Aces_Spell_Utils @ `a0b2f4c2fcfa938c8e47239279c77c2ef82647ac`, source `1.2.7.2-1.21.1`. O catálogo físico referencia `aces_spell_utils-1.2.7.2-1.21.1.jar`, sem prova independente de paridade classfile. Build desta revisão usa Iron's `3.16.2`, versus pack `3.16.3`.

**Gate:** `source_pinned=true`; `mutating_hook=NOT_VERIFIED`; `physical_qa=NOT_TESTED`; `COMPLETE_PERK_READY=false`. Não gera spell registrado, proc, atributo, perk ou adapter novo. Black Arcana preserva seu runtime mágico; Iron's controla casting/mana/cooldown dos seus spells; RPG Skill Tree controla progressão somente via contrato real.
