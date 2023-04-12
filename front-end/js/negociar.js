async function negociate() {
    const submit = document.querySelector('#submit')

    var survivors = await axios
        .get('https://zssnapi.onrender.com/api/survivors/')
        .then((res) => res.data)
        .catch((err) => err)

    const negociatorList = document.querySelector('#survivor-negociator')
    survivors.forEach((element) => {
        var opt = document.createElement('option')
        opt.value = element['id']
        opt.text = element['name']
        negociatorList.appendChild(opt)
    })

    const targetList = document.querySelector('#survivor-target')
    survivors.forEach((element) => {
        var opt = document.createElement('option')
        opt.value = element['id']
        opt.text = element['name']
        targetList.appendChild(opt)
    })

    submit.addEventListener('click', async (evento) => {
        const survivorNegociator = document.querySelector(
            '#survivor-negociator'
        ).value
        const negociatorWater =
            document.querySelector('#negociator-water').value
        const negociatorFood = document.querySelector('#negociator-food').value
        const negociatorMedication = document.querySelector(
            '#negociator-medication'
        ).value
        const negociatorAmmunition = document.querySelector(
            '#negociator-ammunition'
        ).value

        const survivorTarget = document.querySelector('#survivor-target').value
        const targetWater = document.querySelector('#target-water').value
        const targetFood = document.querySelector('#target-food').value
        const targetMedication =
            document.querySelector('#target-medication').value
        const targetAmmunition =
            document.querySelector('#target-ammunition').value

        const dataSurvivor = {
            negotiator: parseInt(survivorNegociator),
            target: parseInt(survivorTarget),
            negotiator_resources: [
                { name: 'Água', quantity: parseInt(negociatorWater) },
                { name: 'Alimentação', quantity: parseInt(negociatorFood) },
                { name: 'Medicação', quantity: parseInt(negociatorMedication) },
                { name: 'Munição', quantity: parseInt(negociatorAmmunition) },
            ],
            target_resources: [
                { name: 'Água', quantity: parseInt(targetWater) },
                { name: 'Alimentação', quantity: parseInt(targetFood) },
                { name: 'Medicação', quantity: parseInt(targetMedication) },
                { name: 'Munição', quantity: parseInt(targetAmmunition) },
            ],
        }

        const res = await axios
            .post(
                'https://zssnapi.onrender.com/api/resources/negotiate/',
                dataSurvivor
            )
            .then((res) => res.data)
            .catch((err) => console.log(err))

        console.log(res)
    })
}

negociate()
/*
submit.addEventListener('click', async (evento) => {
    const survivorNegociator = document.querySelector(
        '#survivor-negociator'
    ).value
    const negociatorWater = document.querySelector('#negociator-water').value
    const negociatorFood = document.querySelector('#negociator-food').value
    const negociatorMedication = document.querySelector(
        '#negociator-medication'
    ).value
    const negociatorAmmunition = document.querySelector(
        '#negociator-ammunition'
    ).value

    const survivorTarget = document.querySelector('#survivor-target').value
    const targetWater = document.querySelector('#target-water').value
    const targetFood = document.querySelector('#target-food').value
    const targetMedication = document.querySelector('#target-medication').value
    const targetAmmunition = document.querySelector('#target-ammunition').value

    const dataSurvivor = {
        negotiator: parseInt(survivorNegociator),
        target: parseInt(survivorTarget),
        negotiator_resources: [
            { name: 'Água', quantity: parseInt(negociatorWater) },
            { name: 'Alimentação', quantity: parseInt(negociatorFood) },
            { name: 'Medicação', quantity: parseInt(negociatorMedication) },
            { name: 'Munição', quantity: parseInt(negociatorAmmunition) },
        ],
        target_resources: [
            { name: 'Água', quantity: parseInt(targetWater) },
            { name: 'Alimentação', quantity: parseInt(targetFood) },
            { name: 'Medicação', quantity: parseInt(targetMedication) },
            { name: 'Munição', quantity: parseInt(targetAmmunition) },
        ],
    }

    console.log(dataSurvivor)
    await axios
        .post('http://127.0.0.1:8000/api/survivor/', dataSurvivor, {
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then((res) => console.log(res))
        .catch((err) => console.log(err))
})*/
