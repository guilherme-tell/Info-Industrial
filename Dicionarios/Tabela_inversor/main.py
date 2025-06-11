dic_inv =   {'P000': {
                    'Descrição': 'Acesso aos parâmetros',
                    'Faixa de valores': '0 a 9999',
                    'Ajuste de fábrica': '0',
                    'Ajuste do usuário':'',
                    'Propr':'',
                    'Grupos':'',
                    'Pág.':'5 - 2'
                    },
            'P001': {
                    'Descrição': 'Acesso aos parâmetros',
                    'Faixa de valores': '0 a 65535',
                    'Ajuste de fábrica': '',
                    'Ajuste do usuário':'',
                    'Propr':'',
                    'Grupos':'',
                    'Pág.':'17 - 21'
                    }
            }

for key, value in dic_inv.items():
    print(key, '->')
    for parametro, descricao in value.items():
        print(parametro, ':', descricao)

dic_inv['P000']['Descrição'] = 'banana'

print(dic_inv['P000']['Descrição'])
