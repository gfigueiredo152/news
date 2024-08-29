import pandas as pd

def Noroeste_Parana():
    nome = "Noroeste Paraná"
    
    Maringá = pd.DataFrame({"Cidade": ["Astorga", "Atalaia", "Bela Vista do Paraíso", "Cambé", "Centenário do Sul", "Colorado", "Floraí", "Floresta", "Guaraci", "Iguaraçu", "Itaguajé", "Ivatuba", "Lobato", "Mandaguaçu", "Mandaguari", "Marialva", "Maringá", "Munhoz de Melo", "Nossa Senhora das Graças", "Nova Esperança", "Ourizona", "Paiçandu", "Paranacity", "Presidente Castelo Branco", "Santa Fé", "Santo Inácio", "Sarandi", "São Jorge do Ivaí", "São Tomé"]})
    Paranavaí = pd.DataFrame({"Cidade": ["Amaporã", "Cruzeiro do Sul", "Diamante do Norte", "Guairaçá", "Inajá", "Itaúna do Sul", "Loanda", "Mirador", "Nova Aliança do Ivaí", "Nova Londrina", "Paraíso do Norte", "Paranapoema", "Paranavaí", "Planaltina do Paraná", "Porto Rico", "Querência do Norte", "Santa Cruz de Monte Castelo", "Santa Isabel do Ivaí", "Santa Mônica", "Santo Antônio do Caiuá", "São Carlos do Ivaí", "São João do Caiuá", "Tamboara", "Terra Rica"]})

    Maringá.Name = "Maringá"
    Paranavaí.Name = "Paranavaí"

    return nome, Maringá, Paranavaí

def Norte_Central_Parana():
    nome = "Norte Central Paraná"

    Londrina = pd.DataFrame({"Cidade": ["Alvorada do Sul", "Arapongas", "Assaí", "Bela Vista do Paraíso", "Cambé", "Centenário do Sul", "Florestópolis", "Ibiporã", "Jataizinho", "Londrina", "Miraselva", "Porecatu", "Prado Ferreira", "Primeiro de Maio", "Rolândia", "Sertanópolis", "Tamarana"]})
    Apucarana = pd.DataFrame({"Cidade": ["Apucarana", "Bom Sucesso", "Califórnia", "Cambira", "Faxinal", "Jandaia do Sul", "Kaloré", "Marilândia do Sul", "Marumbi", "Novo Itacolomi", "Rio Bom", "Sabáudia"]})
    Ivaiporã = pd.DataFrame({"Cidade": ["Arapuã", "Ariranha do Ivaí", "Borrazópolis", "Cândido de Abreu", "Cruzmaltina", "Faxinal", "Godoy Moreira", "Grandes Rios", "Ivaiporã", "Jardim Alegre", "Lidianópolis", "Lunardelli", "Mauá da Serra", "Novo Itacolomi", "Rio Branco do Ivaí", "Rosário do Ivaí", "São João do Ivaí"]})
    Cornélio_Procópio = pd.DataFrame({"Cidade": ["Assaí", "Bandeirantes", "Congonhinhas", "Cornélio Procópio", "Leópolis", "Nova América da Colina", "Nova Fátima", "Ribeirão do Pinhal", "Santa Amélia", "Santa Cecília do Pavão", "Santa Mariana", "Santo Antônio do Paraíso", "São Jerônimo da Serra", "Sapopema", "Sertaneja", "Uraí"]})
    Jacarezinho = pd.DataFrame({"Cidade": ["Barra do Jacaré", "Cambará", "Carlópolis", "Conselheiro Mairinck", "Figueira", "Guapirama", "Ibaiti", "Jaboti", "Jacarezinho", "Japira", "Joaquim Távora", "Jundiaí do Sul", "Pinhalão", "Quatiguá", "Ribeirão Claro", "Salto do Itararé", "Santana do Itararé", "Santo Antônio da Platina", "Siqueira Campos", "Tomazina", "Wenceslau Braz"]})

    Londrina.Name = "Londrina"
    Apucarana.Name = "Apucarana"
    Ivaiporã.Name = "Ivaiporã"
    Cornélio_Procópio.Name = "Cornélio Procópio"
    Jacarezinho.Name = "Jacarezinho"

    return nome, Londrina, Apucarana, Ivaiporã, Cornélio_Procópio, Jacarezinho

def Oeste_Parana():
    nome = "Oeste Paraná"

    Cascavel = pd.DataFrame({"Cidade": ["Anahy", "Assis Chateaubriand", "Boa Vista da Aparecida", "Braganey", "Cafelândia", "Campo Bonito", "Cascavel", "Catanduvas", "Céu Azul", "Corbélia", "Diamante do Oeste", "Diamante do Sul", "Entre Rios do Oeste", "Formosa do Oeste", "Guaíra", "Ibema", "Iracema do Oeste", "Jesuítas", "Lindoeste", "Marechal Cândido Rondon", "Maripá", "Nova Aurora", "Nova Santa Rosa", "Ouro Verde do Oeste", "Palotina", "Quatro Pontes", "Ramilândia", "Santa Helena", "Santa Lúcia", "Santa Tereza do Oeste", "Santa Terezinha de Itaipu", "São José das Palmeiras", "São Pedro do Iguaçu", "Toledo", "Tupãssi", "Ubiratã", "Vera Cruz do Oeste"]})
    Foz_do_Iguaçu = pd.DataFrame({"Cidade": ["Foz do Iguaçu", "Medianeira", "Missal", "Ramilândia", "Santa Terezinha de Itaipu", "São Miguel do Iguaçu", "Serranópolis do Iguaçu"]})

    Cascavel.Name = "Cascavel"
    Foz_do_Iguaçu.Name = "Foz do Iguaçu"

    return nome, Cascavel, Foz_do_Iguaçu

def Sudoeste_Parana():
    nome = "Sudoeste Paraná"

    Pato_Branco = pd.DataFrame({"Cidade": ["Ampére", "Barracão", "Bela Vista da Caroba", "Bom Jesus do Sul", "Capanema", "Chopinzinho", "Coronel Domingos Soares", "Clevelândia", "Dois Vizinhos", "Enéas Marques", "Flor da Serra do Sul", "Francisco Beltrão", "Honório Serpa", "Itapejara d'Oeste", "Manfrinópolis", "Mariópolis", "Marmeleiro", "Nova Esperança do Sudoeste", "Palmas", "Pato Branco", "Pinhal de São Bento", "Planalto", "Realeza", "Renascença", "Salgado Filho", "Salto do Lontra", "Santa Izabel do Oeste", "Santo Antônio do Sudoeste", "São Jorge d'Oeste", "Saudade do Iguaçu", "Verê"]})
    Francisco_Beltrao = pd.DataFrame({"Cidade": ["Bom Sucesso do Sul", "Francisco Beltrão", "Itapejara d'Oeste", "Marmeleiro", "Nova Esperança do Sudoeste", "Renascença", "Salgado Filho", "Santo Antônio do Sudoeste", "São Jorge d'Oeste", "Saudade do Iguaçu", "Verê"]})

    Pato_Branco.Name = "Pato Branco"
    Francisco_Beltrao.Name = "Francisco Beltrão"

    return nome, Pato_Branco, Francisco_Beltrao

def Centro_Sul_Parana():
    nome = "Centro-Sul Paraná"

    Guarapuava = pd.DataFrame({"Cidade": ["Campina do Simão", "Candói", "Cantagalo", "Goioxim", "Guarapuava", "Inácio Martins", "Laranjal", "Laranjeiras do Sul", "Marquinho", "Nova Laranjeiras", "Palmital", "Pinhão", "Porto Barreiro", "Quedas do Iguaçu", "Reserva do Iguaçu", "Rio Bonito do Iguaçu", "Turvo", "Virmond"]})
    Irati = pd.DataFrame({"Cidade": ["Fernandes Pinheiro", "Guamiranga", "Imbituva", "Ivaí", "Ivaiporã", "Mallet", "Prudentópolis", "Rebouças", "Rio Azul", "Teixeira Soares"]})

    Guarapuava.Name = "Guarapuava"
    Irati.Name = "Irati"

    return nome, Guarapuava, Irati

def Campos_Gerais_Parana():
    nome = "Campos Gerais Paraná"

    Ponta_Grossa = pd.DataFrame({"Cidade": ["Arapoti", "Carambeí", "Castro", "Curiúva", "Imbaú", "Ipiranga", "Ortigueira", "Palmeira", "Piraí do Sul", "Ponta Grossa", "Porto Amazonas", "Reserva", "São João do Triunfo", "Tibagi", "Ventania"]})

    Ponta_Grossa.Name = "Ponta Grossa"

    return nome, Ponta_Grossa

def Metropolitana_Curitiba():
    nome = "Metropolitana Curitiba"

    Curitiba = pd.DataFrame({"Cidade": ["Adrianópolis", "Agudos do Sul", "Almirante Tamandaré", "Araucária", "Balsa Nova", "Bocaiúva do Sul", "Campina Grande do Sul", "Campo do Tenente", "Campo Largo", "Campo Magro", "Colombo", "Contenda", "Curitiba", "Doutor Ulysses", "Fazenda Rio Grande", "Itaperuçu", "Lapa", "Mandirituba", "Piên", "Pinhais", "Piraquara", "Quatro Barras", "Quitandinha", "Rio Branco do Sul", "Rio Negro", "São José dos Pinhais", "Tijucas do Sul", "Tunas do Paraná"]})

    Curitiba.Name = "Curitiba"

    return nome, Curitiba

def Litoral_Parana():
    nome = "Litoral Paraná"

    Paranaguá = pd.DataFrame({"Cidade": ["Antonina", "Guaraqueçaba", "Guaratuba", "Matinhos", "Morretes", "Paranaguá", "Pontal do Paraná"]})

    Paranaguá.Name = "Paranaguá"

    return nome, Paranaguá

def Norte_Pioneiro_Parana():
    nome = "Norte Pioneiro Paraná"

    Santo_Antonio_da_Plata = pd.DataFrame({"Cidade": ["Andirá", "Barra do Jacaré", "Cambará", "Carlópolis", "Conselheiro Mairinck", "Curiúva", "Figueira", "Guapirama", "Ibaiti", "Jaboti", "Jacarezinho", "Japira", "Joaquim Távora", "Jundiaí do Sul", "Pinhalão", "Quatiguá", "Ribeirão Claro", "Salto do Itararé", "Santana do Itararé", "Santo Antônio da Platina", "Siqueira Campos", "Tomazina", "Wenceslau Braz"]})

    Santo_Antonio_da_Plata.Name = "Santo Antônio da Platina"

    return nome, Santo_Antonio_da_Plata