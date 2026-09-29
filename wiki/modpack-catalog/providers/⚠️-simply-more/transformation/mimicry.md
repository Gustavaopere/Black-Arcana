# Mimicry

- Provider: **Simply More** (`simplymore`)
- Physical line: `1.3.0 Alpha 5`
- Classificação: **shared player-invoked transformation action**
- Exact surface: abstract `MimicryItem` held-use path inherited by 25 registered concrete forms
- State: `EXACT ACTION / DEPLOYED FORM-STATE CONDITIONAL`

## Identidade semântica

O artefato exato contém 25 formas concretas registradas, mas nenhuma delas sobrescreve uma ação independente. Todas herdam o mesmo `use` / `onUseTick` / `getUseDuration` da base e convergem na mesma transformação Mimicry.

Por isso o catálogo conta **1 raiz compartilhada**, não 25.

## Reachability

O coletor implantado lê apenas os 25 booleans exatos `mimicry.config.<form>.disabled` em `config/simplymore/unique_effect.toml`. O estado atual dessas formas ainda não foi capturado aqui.

Aquisição/reformation e outras supressões implantadas também permanecem gates separados.

## Evidence boundary

A causalidade compartilhada e a cardinalidade das formas estão fechadas; efeitos específicos de cada forma e números de balanceamento não são inferidos.

Source: `../EXACT-ALPHA5-ARTIFACT-AUDIT.md`.
