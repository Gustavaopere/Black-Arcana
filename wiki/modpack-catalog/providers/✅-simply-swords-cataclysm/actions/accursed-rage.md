# Accursed Rage

- Provider: **Simply Swords: Cataclysm** (`simplycataclysm`)
- Physical line: `1.0.2+1.21.1+neoforge`
- Material owner: **Cursium**
- Classificação: **supernatural weapon ability / hit-triggered**
- Source surface: `CursiumSwordItem`
- State: `SOURCE-PINNED IDENTITY / DEPLOYED STARTUP CONDITIONAL`

## Identidade semântica

Raiz provider-owned de combate associada à família Cursium. O source pin fecha Accursed Rage como uma única habilidade; o estado de rage e o bônus de dano são partes da mesma causalidade, não identidades adicionais.

O efeito `accursed_rage` é machinery de estado e adiciona +0 ao denominador.

## Reachability

A ativação atual depende do valor efetivo de `accursedRageChance` no STARTUP config implantado.

- `0` => trait desabilitado;
- valor não-zero => candidato ativo, sujeito ao restante da validação provider-native.

O default do source não substitui o valor implantado.

## Evidence boundary

A identidade e seu gate estão fechados. Chance efetiva, amplificadores, duração e fórmula de dano permanecem fora desta ficha enquanto não houver evidência específica.

Source: `../SOURCE-1.0.2-ABILITY-INVENTORY.md`.
