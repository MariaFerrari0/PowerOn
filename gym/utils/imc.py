def calcular_imc(peso, altura):
    peso = float(peso)
    altura = float(altura)

    if altura <= 0:
        raise ValueError("A altura deve ser maior que zero.")

    if altura > 3:
        altura = altura / 100

    return peso / (altura ** 2)


def diagnosticar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    elif imc < 35:
        return "Obesidade grau I"
    elif imc < 40:
        return "Obesidade grau II"
    else:
        return "Obesidade grau III"