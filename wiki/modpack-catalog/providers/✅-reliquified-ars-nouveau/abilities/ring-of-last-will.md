## Engenharia causal adicional — source 0.8.1 (2026-10-13)

**Limite da prova:** o binário físico tem SHA-1 `4be1f4b0fd7fbec6618596e2e7c3705db88a7579` e a identidade `AbilityTemplate` foi comprovada em auditoria Java 21; os comportamentos detalhados abaixo foram lidos do source público versionado `Octo-Studios/reliquified_ars_nouveau@125e1e3a723d8bc7050026e0670f8ac49535c8bc`, declarado 0.8.1. **Não foi demonstrada equivalência byte-a-byte das implementações de métodos ao JAR físico.** Defaults são templates do Relics, não configuração efetiva/estado de jogador.

**Habilidade:** `last_will` (Last Will); item `reliquified_ars_nouveau:ring_of_last_will`, classe [`RingOfLastWillItem.java`](https://github.com/Octo-Studios/reliquified_ars_nouveau/blob/125e1e3a723d8bc7050026e0670f8ac49535c8bc/src/main/java/it/hurts/shatterbyte/reliquified_ars_nouveau/items/ring/RingOfLastWillItem.java), handlers de `LivingIncomingDamageEvent`, `PlayerTickEvent.Post` e `LivingDamageEvent.Pre`.

### Interceptação de dano potencialmente letal

- No servidor, o handler retorna se não é `ServerPlayer`, dano `<=0` ou quando `event.getAmount()<player.getHealth()`. Portanto o **teste de letalidade é uma comparação numérica nesse estágio do evento**, não prova de morte depois de mitigação de todos os providers.
- Encontra Curios Ring of Last Will equipados e percorre cada stack; ignora o que tem `gameTime < RING_OF_LAST_WILL_COOLDOWN_UNTIL`. Para o primeiro elegível, agenda `RewindEvent(player,gameTime,60)` no `EventQueue` do Ars, envia efeito cliente, **cancela** o evento de dano, grava `REWIND_UNTIL=gameTime+60` e cooldown `gameTime + max(1,round(max(0,cooldownStat)*20))`, incrementa XP `fatal_rewind` e retorna do handler depois de tratar os modifiers. Unidade usada na gravação é tick.
- Se `vengeful_strike` habilitado e atacante é `LivingEntity` viva distinta do jogador, salva UUID de vingança no data component. Em `LivingDamageEvent.Pre` posterior, exige jogador como origem e origem direta, dano positivo e UUID alvo igual ao salvo. Aplica `event.setNewDamage(baseDamage*(1+totalBonus))` com cada bônus clamped `[0,10]`, consome/removendo o UUID de cada stack correspondente e concede XP `revenge_hit`. **Não** é dano adicional confirmado fora do callback.
- `death_paralysis` aplica `RelicsMobEffects.PARALYSIS` ao atacante por `max(1,round(paralysis_duration*20))` ticks; `immortal_aftershock` aplica `RelicsMobEffects.IMMORTALITY` no caster com duração calculada da mesma forma.
- Synergy opcional `illusionary_rewind` com Illusionist's Mantle (condições de Relics): cria `EntityDummy` com owner UUID e `ticksLeft=60`, aplica `VANISHING` ao player e, no tick, redireciona mobs vivos ao dummy dentro de `taunt_radius`. Isso envolve gameplay de IA/entidade, não somente VFX.

### Limites e QA

- O caminho usa explicitamente `event.setCanceled(true)` e o timed event `RewindEvent` pertence ao Ars Nouveau. A recuperação efetiva de posição/vida e persistência pós-death exigem inspeção e teste host; não se declara ressurreição garantida nem replay protection intermod.
- Um dano letal interceptado, agendamento de rewind, vingança posterior e sinergia com clone **não** são quatro raízes de habilidade; o `AbilityTemplate.builder("last_will")` é um só.
- QA de ordem entre providers, bypass damage, void, totem, PvP, safe location, desconexão, restart e stack duplicado é obrigatório antes de qualquer perk que altere fatal prevention/HP.


### Implicações para Black Arcana e RPG

- Reliquified Ars Nouveau/Relics são autoridades do item, habilidade, ranks, experiência, efeitos e dados; Ars Nouveau mantém autoridade por mana, resolver, spell context e spells. Black Arcana não repete cast, recurso ou consequência. RPG Skill Tree só pode consultar/conceder perks mediante boundary comprovado.
- **Perk A:** estatísticas nativas e eventos *observados na fonte* não autorizam escrita arbitrária. **Perk B:** nenhum evento de integração Black Arcana/RPG com garantia de causalidade foi homologado. **Perk C/D:** adapter/rate caps e token de cast exigem contrato, **⛔ fail-closed** até confirmação.
- QA pendente: instância física atual de Relics 0.12.8, Ars Nouveau 5.13.1, Curios atual, config, save/restart, multiplayer, equipamento duplicado, eventos cancelados, custos e Mastery. Nenhum GameTest ou Survival desse item foi executado nesta etapa.
- **Clean-room:** relatamos fatos de execução em nossas palavras; não copiamos código-fonte/asset do provider para o Black Arcana.

[Matriz desta etapa](../PERK-ENGINEERING-MATRIX-0.8.1.md) · [Índice do provider](../README.md).
