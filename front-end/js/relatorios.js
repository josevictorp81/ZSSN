async function graphs() {
    // porcentagem de infectados
    const infected = await axios
        .get('https://zssnapi.onrender.com/api/survivors/percentage-infected/')
        .then((res) => res.data['detail'])
        .catch((err) => console.log(err))
    const notInfected = await axios
        .get(
            'https://zssnapi.onrender.com/api/survivors/percentage-not-infected/'
        )
        .then((res) => res.data['detail'])
        .catch((err) => console.log(err))

    const ctx = document.querySelector('#chart')
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Infectados', 'Não infectados'],
            datasets: [
                {
                    data: [infected, notInfected],
                    borderWidth: 1,
                    backgroundColor: ['rgb(255, 0, 0)', 'rgb(0, 250, 0)'],
                },
            ],
        },
    })

    // média dos recursos
    const resources = await axios
        .get(
            'https://zssnapi.onrender.com/api/resources/mean-amount-resources/'
        )
        .then((res) => res.data)
        .catch((err) => console.log(err))

    document.querySelector('#water').innerText = resources['Água']
    document.querySelector('#food').innerText = resources['Alimentação']
    document.querySelector('#medication').innerText = resources['Medicação']
    document.querySelector('#ammunition').innerText = resources['Munição']

    // sobreviventes infectados
    const infectedSurvivors = await axios
        .get('https://zssnapi.onrender.com/api/survivors/infected/')
        .then((res) => res.data)
        .catch((err) => console.log(err))

    console.log(infectedSurvivors)

    const infectedList = document.querySelector('#survivor-infected-list')
    infectedSurvivors.forEach((element) => {
        var opt = document.createElement('option')
        opt.value = element['id']
        opt.text = element['name']
        infectedList.appendChild(opt)
    })

    // pontos perdidos
    button = document.querySelector('#btn-points')
    button.addEventListener('click', async () => {
        const suvivorId = document.querySelector(
            '#survivor-infected-list'
        ).value
        const lostPoints = await axios
            .get(
                `https://zssnapi.onrender.com/api/survivor/${suvivorId}/lost-points/`
            )
            .then((res) => res.data['detail'])
            .catch((err) => console.log(err))
        console.log(lostPoints)
        document.querySelector('#points').innerText = lostPoints
    })
}

graphs()
