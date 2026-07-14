# Instruções de exportação

Os layouts editáveis estão em HTML/CSS. Cada arquivo `arte.html` contém uma ou mais áreas `.creative-frame` no tamanho correto para Instagram.

## Exportação automática

Use o script:

```powershell
& "C:\Users\vitor\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" "marketing\instagram\07_exportacao\exportar_posts.js"
```

O script tenta carregar Playwright do ambiente local. Nesta máquina, o runtime do Codex contém Playwright em:

```text
C:\Users\vitor\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules
```

Os PNGs serão criados em:

```text
marketing\instagram\07_exportacao\png
```

## Exportação manual

1. Abra qualquer `arte.html` no navegador.
2. Confira se a arte carregou com logo e texto corretos.
3. Use captura do navegador, extensão de screenshot ou ferramenta de design para exportar o elemento no tamanho original.
4. Para carrosséis, exporte cada slide separadamente.

## Observação

Não publique nem agende a partir destes arquivos. Eles são materiais para revisão humana.
