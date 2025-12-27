from flask import Flask, request
import os
import qrcode
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Spacer
from reportlab.lib import colors

app = Flask(__name__)
instagram_url = "https://www.instagram.com/sil.info/"
PASTA_OS = r"C:\Users\Nelsinho\Documents\OS Sil Info\PDF_OS\TXT"
os.makedirs(PASTA_OS, exist_ok=True)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OS Sil Mobile</title>
<style>
* { box-sizing: border-box; }
body { font-family: Arial; padding: 10px; margin: 0; }
h2 { text-align: center; }
label { font-weight: bold; }
input, textarea, button {
  width: 100%;
  padding: 10px;
  margin: 6px 0 12px 0;
  font-size: 16px;
}
button {
  background: #2d89ef;
  color: #fff;
  border: none;
  border-radius: 6px;
}
</style>

<script>
function buscarCEP() {
  const cep = document.getElementById('cep').value.replace(/\\D/g, '');
  if (cep.length !== 8) return;

  fetch(`https://viacep.com.br/ws/${cep}/json/`)
    .then(r => r.json())
    .then(d => {
      if (d.erro) return;
      document.getElementById('endereco').value = d.logradouro || '';
      document.getElementById('bairro').value = d.bairro || '';
      document.getElementById('municipio').value = d.localidade || '';
      document.getElementById('uf').value = d.uf || '';
    });
}
</script>

</head>
<body>

<h2>ORDEM DE SERVÇO SIL INFO</h2>

<form method="post">
<label>Cliente</label>
<input type="text" name="cliente" required>

<label>CPF</label>
<input type="tel" name="cpf" maxlength="14" placeholder="000.000.000-00"
oninput="let v=this.value.replace(/\\D/g,'').slice(0,11);
v=v.replace(/(\\d{3})(\\d)/,'$1.$2');
v=v.replace(/(\\d{3})(\\d)/,'$1.$2');
v=v.replace(/(\\d{3})(\\d{1,2})$/,'$1-$2');
this.value=v;">

<label>Endereço</label>
<input type="text" name="endereco" id="endereco">

<label>Nº</label>
<input type="tel" name="numero" id="numero" maxlength="4" placeholder="0000"
oninput="this.value=this.value.replace(/[^0-9]/g,'').slice(0,4);">

<label>Bairro</label>
<input type="text" name="bairro" id="bairro">

<label>CEP</label>
<input type="tel" name="cep" id="cep" maxlength="9" placeholder="00000-000"
oninput="let v=this.value.replace(/\\D/g,'').slice(0,8);
v=v.replace(/(\\d{5})(\\d)/,'$1-$2');
this.value=v; buscarCEP();">

<label>Telefone</label>
<input type="tel" name="telefone" id="telefone" maxlength="15" placeholder="(99) 99999-9999"
oninput="let v=this.value.replace(/[^0-9]/g,'').slice(0,11);
v=v.replace(/([0-9]{2})([0-9])/,'($1) $2');
v=v.replace(/([0-9]{5})([0-9])/,'$1-$2');
this.value=v;">

<label>Município</label>
<input type="text" name="municipio" id="municipio">

<label>UF</label>
<input type="text" name="uf" id="uf" maxlength="2" placeholder="UF"
oninput="this.value=this.value.replace(/[^A-Za-z]/g,'').toUpperCase().slice(0,2);">

<label>Produto</label>
<input type="text" name="produto">

<label>Marca</label>
<input type="text" name="marca">

<label>Modelo</label>
<input type="text" name="modelo">

<label>Série</label>
<input type="text" name="serie">

<label>Defeito</label>
<textarea name="defeito" rows="3"></textarea>

<label>Obs Cliente</label>
<textarea name="obs_cliente" rows="2"></textarea>

<label>Obs Interna</label>
<textarea name="obs_interna" rows="2"></textarea>

<button type="submit">Salvar OS</button>
</form>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        cliente = request.form.get("cliente", "").title()
        cpf = request.form.get("cpf", "")
        endereco = request.form.get("endereco", "").title()
        numero_casa = request.form.get("numero", "")
        bairro = request.form.get("bairro", "").title()
        cep = request.form.get("cep", "")
        telefone = request.form.get("telefone", "")
        municipio = request.form.get("municipio", "")
        uf = request.form.get("uf", "")
        produto = request.form.get("produto", "")
        marca = request.form.get("marca", "")
        modelo = request.form.get("modelo", "")
        serie = request.form.get("serie", "")
        defeito = request.form.get("defeito", "")
        obs_cliente = request.form.get("obs_cliente", "")
        obs_interna = request.form.get("obs_interna", "")

        arquivos = [f for f in os.listdir(PASTA_OS) if f.startswith("OS_") and f.endswith(".txt")]
        numeros = [int(f.replace("OS_", "").replace(".txt", "")) for f in arquivos if f.replace("OS_", "").replace(".txt", "").isdigit()]
        ultimo = max(numeros) if numeros else 0
        numero = ultimo + 2

        nome_arquivo = os.path.join(PASTA_OS, f"OS_{numero}.txt")

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"OS Nº {numero}\n")
            f.write(f"Cliente: {cliente}\n")
            f.write(f"CPF: \n")
            f.write(f"Endereço: \n")
            f.write(f"Bairro: \n")
            f.write(f"CEP: \n")
            f.write(f"Telefone: {telefone}\n")
            f.write(f"Município: \n")
            f.write(f"UF: \n")
            f.write(f"Produto: \n")
            f.write(f"Marca: \n")
            f.write(f"Modelo: \n")
            f.write(f"Série: \n")
            f.write(f"Defeito: {defeito}\n")
            f.write(f"Serviço 1:  - \n")
            f.write(f"Serviço 2:  - \n")
            f.write(f"Serviço 3:  - \n")
            f.write(f"Total: \n")
            f.write(f"Obs Cliente: \n")
            f.write(f"Obs Interna: \n")

        caminho_pdf = os.path.join(r"C:\Users\Nelsinho\Documents\OS Sil Info\PDF_OS", f"OS_{numero}.pdf")

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="Titulo",
            fontName="Helvetica-Bold",
            fontSize=7,
            leading=9,
            spaceAfter=4
        ))
        styles.add(ParagraphStyle(
            name="Campo",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            spaceAfter=1
        ))
        styles.add(ParagraphStyle(
            name="Valor",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            spaceAfter=2
        ))

        qr_img = qrcode.make(instagram_url)
        qr_path = os.path.join(os.getcwd(), "qr_temp.png")
        qr_img.save(qr_path)

        elementos = [
            Image(
                r"C:\Users\Nelsinho\Documents\OS Sil Info\Logo_TOPO_PDF.png",
                width=210,
                height=50
            ),
            Paragraph(
                f"ORDEM DE SERVIÇO Nº {numero}",
                ParagraphStyle(
                    name="TituloCentro",
                    parent=styles["Titulo"],
                    alignment=1,
                    spaceBefore=8,
                    spaceAfter=6,
                    fontName="Helvetica-Bold",
                    fontSize=12
                )
            ),
            Spacer(1, 8),
            Table(
                [[
                    Paragraph(f"Cliente: {cliente}", styles["Valor"]),
                    Paragraph(f"CPF: {cpf}", styles["Valor"])
                ]],
                colWidths=[195, 85],
                style=[
                    ('BACKGROUND', (0,0), (-1,-1), '#E6E6E6'),
                    ('LEFTPADDING', (0,0), (-1,-1), 2),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 3),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 3)
                ]
            ),

            Table(
                [[
                    Paragraph(f"Endereço: {endereco}", styles["Valor"]),
                    Paragraph(f"Nº: {numero_casa}", styles["Valor"])
                ]],
                colWidths=[200, 90],
                style=[
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]
            ),

            Table(
                [[
                    Paragraph(f"Bairro: {bairro}", styles["Valor"]),
                    Paragraph(f"CEP: {cep}", styles["Valor"])
                ]],
                colWidths=[200, 90],
                style=[
                    ('BACKGROUND', (0,0), (-1,-1), '#E6E6E6'),
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]
            ),

            Table(
                [[
                    Paragraph(f"Telefone: {telefone}", styles["Valor"]),
                    Paragraph(f"Município: {municipio}", styles["Valor"]),
                    Paragraph(f"UF: {uf}", styles["Valor"])
                ]],
                colWidths=[120, 120, 50],
                style=[
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]
            ),
            Table(
                [[
                    Paragraph(f"Produto: {produto}", styles["Valor"]),
                    Paragraph(f"Marca: {marca}", styles["Valor"])
                ]],
                colWidths=[200, 90],
                style=[
                    ('BACKGROUND', (0,0), (-1,-1), '#E6E6E6'),
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]
            ),

            Table(
                [[
                    Paragraph(f"Modelo: {modelo}", styles["Valor"]),
                    Paragraph(f"Nº Série: {serie}", styles["Valor"])
                ]],
                colWidths=[160, 120],
                style=[
                    ('LEFTPADDING', (0,0), (-1,-1), 2),
                    ('RIGHTPADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 2),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ]
            ),

            Table(
                [[
                    Paragraph("Defeito Reclamado:", styles["Campo"])
                ]],
                colWidths=[290],
                style=[
                    ('BACKGROUND', (0,0), (-1,-1), '#E6E6E6'),
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]
            ),

            Table(
                [[
                    Paragraph(defeito if defeito else " ", styles["Valor"])
                ]],
                colWidths=[290],
                rowHeights=[14],
                style=[
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]
            ),


            Table(
                [[
                    Paragraph("Observações:", styles["Campo"])
                ]],
                colWidths=[290],
                style=[
                    ('BACKGROUND', (0,0), (-1,-1), '#E6E6E6'),
                    ('LEFTPADDING', (0,0), (-1,-1), 7),
                    ('RIGHTPADDING', (0,0), (-1,-1), 5),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ]
            ),

            Paragraph(obs_cliente, styles["Valor"]),

            Table(
                [[ "" ]],
                colWidths=[290],
                style=[
                    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.grey),
                ]
            ),

            Spacer(1, 8),

            Paragraph(
                "ASSITÊNCIA TÉCNICA AUTORIZADA em Informática e Eletrônicos.",
                ParagraphStyle(
                    name="Servicos1",
                    parent=styles["Valor"],
                    alignment=1,
                    fontName="Helvetica-Bold",
                    fontSize=8,
                    textColor=colors.HexColor("#2d89ef")
                )
            ),

            Spacer(1, 4),

            Paragraph(
                "TVs • Notebooks • PCs • Eletrônicos e Eletrodomésticos",
                ParagraphStyle(
                    name="Servicos2",
                    parent=styles["Valor"],
                    alignment=1,
                    fontSize=7,
                    textColor=colors.grey
                )
            ),

            Spacer(1, 1),

            Table(
                [[ "" ]],
                colWidths=[290],
                style=[
                    ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.grey),
                ]
            ),

            Spacer(1, 8),

            Image(
                qr_path,
                width=40,
                height=40
            ),

            Spacer(1, 6),

            Paragraph(
                f"Santa Cruz do Sul | RS — {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                ParagraphStyle(
                    name="DataHoraRodape",
                    parent=styles["Valor"],
                    alignment=2,  # direita
                    fontSize=7,
                    textColor=colors.grey
                )
            ),

        ]

        SimpleDocTemplate(
            caminho_pdf,
            pagesize=(105 * 2.83465, 148 * 2.83465),
            rightMargin=5,
            leftMargin=5,
            topMargin=5,
            bottomMargin=5
        ).build(elementos)

        return f"""
        <h2>Comprovante de OS</h2>
        <p><b>Nº:</b> {numero}</p>
        <p><b>Cliente:</b> {cliente}</p>
        <p><b>Telefone:</b> {telefone}</p>
        <p><b>Produto:</b> {produto}</p>
        <p><b>Defeito:</b> {defeito}</p>
        <br>
        <button onclick="window.print()">Imprimir / Salvar PDF</button>
        <br><br>
        <a href="/">Nova OS</a>
        """

    return HTML_FORM

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
