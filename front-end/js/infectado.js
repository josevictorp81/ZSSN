async function report() {
    const survivorsList = await axios
        .get('https://zssnapi.onrender.com/api/survivors/not-infected/')
        .then((res) => res.data)
        .catch((err) => err)

    const survivorRelator = document.querySelector('#survivor-relator')
    survivorsList.forEach((option) => {
        var opt = document.createElement('option')
        opt.value = option['id']
        opt.text = option['name']
        survivorRelator.appendChild(opt)
    })

    const survivorInfected = document.querySelector('#survivor-infectd')
    survivorsList.forEach((option) => {
        var opt = document.createElement('option')
        opt.value = option['id']
        opt.text = option['name']
        survivorInfected.appendChild(opt)
    })

    const submit = document.querySelector('#submit')

    submit.addEventListener('click', async () => {
        const survivorRelator =
            document.querySelector('#survivor-relator').value
        const survivorInfected =
            document.querySelector('#survivor-infectd').value

        const dataSurvivor = {
            reporter: parseInt(survivorRelator),
            infected: parseInt(survivorInfected),
        }
        console.log(dataSurvivor)
        const infectd = await axios
            .post(
                'https://zssnapi.onrender.com/api/survivor/infected/',
                dataSurvivor
            )
            .then((res) => res.data['detail'])
            .catch((err) => err)

        if (infectd) {
            document.querySelector('#message').textContent = infectd
        }
    })
}

report()
