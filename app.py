import streamlit as st
import urllib.request
from urllib.error import HTTPError
import zipfile
import io

st.set_page_config(page_title="Download de Imagens", page_icon="📦")
st.title("📦 Baixador de Imagens por SKU")

# Campo de texto para o usuário
skus_input = st.text_area(
    "Cole a lista de SKUs (separados por vírgula ou um por linha):", 
    height=150
)

# Botão de processar
if st.button("Gerar Arquivo ZIP"):
    if skus_input:
        # Organiza a lista de SKUs
        skus_input = skus_input.replace('\n', ',')
        skus = [sku.strip() for sku in skus_input.split(',') if sku.strip()]
        
        base_url = "https://evino-res.cloudinary.com/image/upload/v1744634685/products/{}-standing-front.png"
        
        # Cria um arquivo zip na memória (ideal para web apps)
        zip_buffer = io.BytesIO()
        
        with st.spinner('Baixando imagens...'):
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for sku in skus:
                    url = base_url.format(sku)
                    try:
                        with urllib.request.urlopen(url) as response:
                            zip_file.writestr(f"{sku}.png", response.read())
                    except HTTPError:
                        st.warning(f"Imagem não encontrada: {sku}")
        
        st.success("✅ Tudo pronto! Clique no botão abaixo para baixar.")
        
        # Botão final de Download
        st.download_button(
            label="📥 Baixar imagens_produtos.zip",
            data=zip_buffer.getvalue(),
            file_name="imagens_produtos.zip",
            mime="application/zip"
        )
    else:
        st.error("Por favor, insira pelo menos um SKU.")
