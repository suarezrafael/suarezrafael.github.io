# Rafael Suarez - cartao digital

Site pessoal publicado em `https://suarezrafael.github.io/`, separado do site da RVS Tecnologia em `/rvs-tecnologia/`.

## Arquivos

- `index.html`, `styles.css`: cartao digital estatico e responsivo.
- `contact.vcf`: contato para importar no celular.
- `assets/qr.svg`: QR code da URL principal.
- `print/cartao-rafael-suarez-frente-verso.pdf`: arte vetorial de duas paginas para grafica.
- `print/cartao-rafael-suarez-frente.pdf` e `print/cartao-rafael-suarez-verso.pdf`: faces separadas.

## Impressao

Formato final: **90 x 50 mm**. O PDF tem **96 x 56 mm**, com 3 mm de sangria em cada lado. As cores do PDF sao RGB; confirme o perfil de cor e a imposicao de frente/verso com a grafica antes de imprimir um lote. A margem de seguranca do texto e de aproximadamente 4 mm alem da linha de corte.

Para regenerar os arquivos apos uma mudanca de contato ou URL:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-print.txt
.\.venv\Scripts\python.exe scripts\generate_print.py
```

O telefone foi omitido porque o numero visivel e o link telefonico do site da RVS nao coincidem. Confirme o numero antes de inclui-lo no cartao digital, no vCard ou na arte impressa.
