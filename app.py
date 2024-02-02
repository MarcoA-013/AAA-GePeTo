import streamlit as st

import openai
import json
import requests
from datetime import datetime, timedelta

############################################
# To run this app, you just need to type: streamlit run app.py
############################################

# Define a function to generate text using the OpenAI API
def BasicGeneration(userPrompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": userPrompt}]
    )
    return completion.choices[0].message.content

# Define a function to get the Bitcoin prices from the API
def GetBitCoinPrices():
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    # Define the request headers with API key and host
    headers = {
        "X-RapidAPI-Key": "a617d6467dmshac84323ce581a72p11caa9jsn1adf8bbcbd47",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    # Parse the response data as a JSON object
    JSONResult = json.loads(response.text)
    # Extract the "history" field from the JSON response
    history = JSONResult["data"]["history"]
    # Extract the "price" field from each element in the "history" array and add to a list
    prices = []
    for change in history:
        prices.append(change["price"])
    # Join the list of prices into a comma-separated string
    pricesList = ','.join(prices)
    # Return the comma-separated string of prices
    return pricesList



# This is the main app HomePage code
st.set_page_config(page_title="AAA GePeTo", page_icon=":money_with_wings:")

st.write("""
# Bem vindo ao AAA-GePeTo :money_with_wings: :sunglasses:
""")

st.write("""
Esta aplicação usa o modelo GPT-3.5 para responder sobre vários assuntos,
# Sobre o modelo
O modelo GPT-3.5 é um modelo de linguagem de inteligência artificial desenvolvido pela OpenAI. 
O modelo é treinado em uma grande quantidade de texto da internet e pode ser usado para gerar texto
em uma variedade de estilos, incluindo notícias, ficção, poesia e muito mais.""")

#     Esta chave foi gerada em 3/5/2021 às 15:07:34 
#     openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
date = datetime.now() - timedelta(days=14)
date_string = date.isoformat("T")# + "Z"  # Convert to YouTube timestamp format

# Create input fields for API keys
openai_api_key = st.text_input("Insira sua chave de API da OpenAI aqui", type="password") # Hide the key

# Define the session_state OpenAI API key
if st.button('Enviar'):
    st.session_state.openai_api_key = openai_api_key
    openai.api_key = st.session_state.openai_api_key

# Define the session state
if 'init' not in st.session_state:
    st.session_state.init = True

##

st.write("""
## Consulte um especialista: -Trader Bitcoin
analisar as cotações do Bitcoin nos últimos 7 dias e fornecer uma análise técnica.
Esse período é limitado por conta do uso de um acesso gratuito, mas poderiam ser períodos maiores.
""")

if st.button('Analisar'):
    with st.spinner('Coletando as cotações...'):
        bitcoinPrices = GetBitCoinPrices()
        st.success('Feito!')
    with st.spinner('Analisando as cotações...'):
        chatGPTPrompt = f"""Vocë é um experiente trader de criptomoedas com mais de 10 anos de experiência, 
                    Eu vou fornecer a você uma lista de preços do Bitcoin nos últimos 7 dias,
                    para que você escreva uma análise técnica. e aqui vai o que eu quero que você escreva: 
                    Price Overview - Visão geral do preço, 
                    Moving Averages - Médias móveis, 
                    Relative Strength Index (RSI) - Índice de Força Relativa (IFR),
                    Moving Average Convergence Divergence (MACD) - Convergência e Divergência de Médias Móveis (MACD),
                    Advice and Suggestion - Conselho e Sugestão,
                    Do I buy or sell? - Eu compro ou vendo?,
                    Por favor seja o mais detalhista possível, e explique de modo que um leigo possa compreender. 
                    e certifique-se de usar cabeçalhos para cada seção.
                    Aqui está a relação dos preços: {bitcoinPrices}"""
    
        analysis = BasicGeneration(chatGPTPrompt)
        st.text_area("Análise", analysis,
                     height=500)
        st.success('Feito!')

st.write("""
## Receitas
Pedir a receita de um prato ou fornecer uma lista de ingredientes e pedir uma receita.

Para usar a aplicação, basta selecionar um assunto, dar alguns detalhes e clicar no botão 'Analisar' abaixo 
, daí é só aguardar alguns segundos enquanto a análise é gerada.

""")
col1, col2, col3 = st.columns(3)

with col1:
    recipe = st.radio(
    "Que tipo de receita você quer?",
    ('Sobremesas', 'Almoço & Jantar', 'Salgadinhos', 'Bebidas'))

with col2:
    recipe_type = st.radio(
    "Qual o estilo da receita?",
    ('Qualquer', 'Árabe', 'Mediterrâneo', 'Italiano', 'Japonês', 'Mexicano', 'Brasileiro'))

with col3:
    txt = st.text_area('Descreva aqui a sua lista de Ingredientes, com detalhes', '''
    ''')

if st.button('Pensa pra mim...'):
    with st.spinner('Botando os Bits do meu cérebro pra pensar...'):
        chatGPTPrompt = f"""Você é um experiente cozinheiro brasileiro que tem um blog de receitas caseiras, 
                    Eu vou fornecer a você uma lista de ingredientes que tenho disponível na minha cozinha,
                    para que você sugira algumas opções de receitas de {recipe}, no estilo {recipe_type} 
                    que eu possa fazer usando, se possível todos ou ao menos um dos ingredientes.
                    E aqui vai o que eu quero que você escreva:
                    Faça um breve comentário bem humorado sobre as receitas que você sugere,
                    Pelo menos três opções de preparo, cada uma com uma lista de ingredientes e modo de preparo,
                    Por favor seja o mais detalhista possível, e explique de modo que um leigo possa compreender. 
                    e certifique-se de usar cabeçalhos para cada seção.
                    Aqui está a relação dos ingredientes: {txt}"""
    
        analysis = BasicGeneration(chatGPTPrompt)
        st.text_area("Análise", analysis,
                     height=500)
        st.success('Feito!')


st.subheader(
    'by Bola8!')





    









    
    

    
    







