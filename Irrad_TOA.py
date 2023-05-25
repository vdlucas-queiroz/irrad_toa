""" Princípios Físicos de Sensoriamento Remoto | SER - 205
Aluno: Vinícius D'Lucas Bezerra e Queiroz - 361406/2022

Script em Python para calcular os valores de Irradiância e a Irradiação Solar no topo da Atmosfera (TOA) no momento da
tomada das quatro geometrias diferentes (variação de ângulo zenital e azimutal) com o App Albedo.
"""

# Importando bibliotecas

import datetime
from math import pi, cos, sin, acos
import re


# Funções auxiliares:

# Transformação de horas em horas decimais:
def convert_hour(hora):
    lista = re.split(':', hora)
    hd = float(lista[0]) + float(lista[1]) / 60 + float(lista[2]) / 3600
    return hd


# Transformação de data padrão para dia juliano(doy):
def datestdtojd(data):
    fmt = '%d-%m-%Y'
    sdtdate = datetime.datetime.strptime(data, fmt)
    sdtdate = sdtdate.timetuple()
    jdate = sdtdate.tm_yday
    return jdate


# Função Principal:

# Cálculo da Irradiação Solar Incidente sobre uma superfície horizontal no topo da atmosfera em função da latitude,
# hora local e data.
# A função retorna 3 valores: Irradiação Solar Incidente, Irradiância e Ângulo zenital solar.

def irrad_toa(latitude, longitude, local_hour, gmt, date):
    print(f'Cálculo da Irradiação Solar incidente sobre uma superfície horizontal no topo'
          f' da atmosfera terrestre num período de uma hora:\n\n')
    print(f'\t\t>>>>     Dados de entrada:     <<<< \n')

    # Dados de entrada
    # Transformação do valor da latitude para radianos:
    latitude_f = latitude * pi / 180
    print(f' >> Latitude =  {latitude}')
    print(f' >> Longitude = {longitude}')

    # Transformação do valor da hora local para horas decimais:
    local_hour_i = local_hour  # Formato 'HH:mm:ss'
    local_hour_f = convert_hour(local_hour_i)
    print(f' >> Hora Local =  {local_hour_i}')
    print(f' >> GMT =  {gmt}')

    # Printando a data na tela:
    print(f' >> Data: {date} \n\n')

    # Constantes
    es = 1367  # Constante Solar em W/m²
    es2 = es * 3.6  # Constante Solar em kJ/m².h

    print(f'\t\t>>>>     Planilha de Cálculo:     <<<< \n')  # Print do cabeçalho.

    # Cálculo do dia juliano e da relação distância média terra sol/distância terra-sol para o dia juliano.
    dn = datestdtojd(date)
    print(f'>> O dia Juliano é: dn = {dn}.\n')

    # gama: ângulo em radianos calculado para determinação do valor de correção de excentricidade.
    gama = 2 * pi * ((dn - 1) / 365)
    print(f'>> Valor de gama: gama =  {round(gama, 6)} rad ou {round(gama * 180 / pi, 6)}°\n')

    # Cálculo do fator de correção de excentricidade:
    e0 = 1.000110 + 0.034221 * cos(gama) + 0.001280 * sin(gama) + 0.000719 * cos(2 * gama) + 0.000077 * sin(2 * gama)
    print(f'>> Fator de correção de excentricidade: E0 = {round(e0, 6)}.\n')

    # Cálculo da declinação solar:
    declination = (0.006918 - 0.399912 * cos(gama) + 0.070257 * sin(gama) - 0.006758 * cos(2 * gama) + 0.000907 * sin(
        2 * gama) - 0.002697 * cos(3 * gama) + 0.00148 * sin(3 * gama))
    print(f'>> Ângulo de declinação solar: d = {round(declination, 6)}rad ou {round(declination * 180 / pi, 6)}° \n')

    # Cálculo do Tempo local Aparente (lat):
    # Equação do Tempo Solar et:
    et = (0.000075 + 0.001868 * cos(gama) - 0.032077 * sin(gama) - 0.014615 * cos(2 * gama) - 0.04089 * sin(
        2 * gama)) * 229.18
    ls = 15 * abs(gmt)  # Meridiano Padrão;
    lat = local_hour_f + ((4 * (ls - abs(longitude)) + et) / 60)  # local apparent time (lat)
    print(f'>> Tempo local aparente: LAT = {round(lat, 6)}h \n')

    # Cálculo do ângulo horário solar em radianos:
    hour_angle = (12 - lat) * pi / 12
    print(f'>> Ângulo horário solar corrigido: w = {round(hour_angle, 6)}rad ou {round(hour_angle * 180 / pi, 6)}° \n')

    # Cálculo da Irradiação solar incidente sobre uma superfície horizontal no topo da atmosfera:
    # Irradiação solar, incluindo termo multiplicativo "sin(pi/24)*24/pi"
    i0 = es2 * e0 * ((sin(declination) * sin(latitude_f))
                     + sin(pi / 24) * (24 / pi) * (cos(declination) * cos(latitude_f) * cos(hour_angle)))

    # Cálculo do ângulo zenital em função de declinação, latitude e ângulo horário solar.
    zenith_angle = acos(((sin(declination) * sin(latitude_f))
                         + (cos(declination) * cos(latitude_f) * cos(
                            hour_angle))))

    elev_angle = (pi / 2) - zenith_angle  # Ângulo de elevação solar.

    # Cálculo da Irradiância no topo da atmosfera
    e = es2 * e0 * ((sin(declination) * sin(latitude_f)) + (
                cos(declination) * cos(latitude_f) * cos(hour_angle))) / 3.6

    # Exibindo os resultados na tela:
    print(f'>> Ângulo zenital solar é : z= {round(zenith_angle, 6)}rad ou {round(zenith_angle * 180 / pi, 6)}° \n')
    print(f'>> Ângulo de elevação solar é : a = {round(elev_angle, 6)}rad ou {round(elev_angle * 180 / pi, 6)}°')
    print('\n\n \t\t>>>>     RESULTADO     <<<\n\n')
    print(
        f'>> Para latitude {latitude}°, no dia {date} (doy={dn}) às {local_hour_i},\n\n'
        f'>> A Irradiação Solar incidente sobre uma superfície horizontal no topo da atmosfera '
        f'terrestre num período de uma hora é: I0 = {round(i0, 3)}KJ/m².h \n')
    print(f'>> A Irradiância, utilizando os mesmos parâmetros tem valor de: E = {round(e, 2)}W/m²')

    # Retornando os valores de Irradiação, Irradiância e Ângulo Zenital.
    return [i0, e, zenith_angle]


# Exemplo de chamada da função irrad_toa
## irrad_toa(latitude, -longitude, 'hora local hh:mm:ss', GMT , 'data dd:mm:aaaa')
p1 = irrad_toa(-7.91073, -45.858486, '12:40:10', -3, '02-04-2022')
