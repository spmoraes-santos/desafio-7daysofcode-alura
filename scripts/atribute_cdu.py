### Produced by S P Moraes-Santos

# Define constants 
CDU_CLASSES = [
    'Generalidades. Ciência e conhecimento',        # 0xx
    'Filosofia e psicologia',                        # 1xx
    'Religião',                                      # 2xx
    'Ciências sociais',                              # 3xx
    'Classe vaga. Provisoriamente não ocupada',      # 4xx
    'Matemática e ciências naturais',                # 5xx
    'Ciências aplicadas',                            # 6xx
    'Belas artes',                                   # 7xx
    'Linguagem. Língua. Linguística',                # 8xx
    'Geografia. Biografia. História',                # 9xx
]

def mappying_class_cdu(valor):
    """
    Mapeia um número de CDU (Classificação Decimal Universal) para o nome de sua classe principal.
    """
    try:
        # Try to convert to an in
        val = int(valor)
    except (ValueError, TypeError):
        return 'Inválido'

    if 0 <= val <= 999:
        # Divide by 100
        return CDU_CLASSES[val // 100]

    return 'Fora de intervalo'
