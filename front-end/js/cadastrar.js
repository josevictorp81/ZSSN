const post = async (data) => {
    const message = await axios
        .post('https://zssnapi.onrender.com/api/survivor/', data)
        .then((res) => console.log(res.data['detail']))
        .catch((err) => console.log(err))
    console.log(message)
    // document.querySelector(
    //     '#message'
    // ).innerHTML = `<p style="background-color: rgb(0, 250, 100) ">${message}</p>`
}

const submit = document.querySelector('#submit')

submit.addEventListener('click', async () => {
    const name = document.querySelector('#name').value
    const age = document.querySelector('#age').value
    const sex = document.querySelector('#sex').value
    const latitude = document.querySelector('#latitude').value
    const longitude = document.querySelector('#longitude').value
    const water = document.querySelector('#water').value
    const food = document.querySelector('#food').value
    const medication = document.querySelector('#medication').value
    const ammunition = document.querySelector('#ammunition').value

    const dataSurvivor = {
        name: name,
        age: parseInt(age),
        sex: sex,
        local: `${latitude}, ${longitude}`,
        resources: [
            { name: 'Água', quantity: parseInt(water) },
            { name: 'Alimentação', quantity: parseInt(food) },
            { name: 'Medicação', quantity: parseInt(medication) },
            { name: 'Munição', quantity: parseInt(ammunition) },
        ],
    }
    console.log(dataSurvivor)
    post(dataSurvivor)
})
