async function update() {
    const survivorsList = await axios
        .get('https://zssnapi.onrender.com/api/survivors/not-infected/')
        .then((res) => res.data)
        .catch((err) => [])

    console.log(survivorsList)

    const survivorRelator = document.querySelector('#survivor-update')
    survivorsList.forEach((option) => {
        var opt = document.createElement('option')
        opt.value = option['id']
        opt.text = option['name']
        survivorRelator.appendChild(opt)
    })

    const submit = document.querySelector('#submit')
    const message = ''

    submit.addEventListener('click', async () => {
        const survivor = document.querySelector('#survivor-update').value
        const latitude = document.querySelector('#latitude').value
        const longitude = document.querySelector('#longitude').value

        const data = {
            local: `${latitude}, ${longitude}`,
        }

        const message = await axios
            .put(
                `https://zssnapi.onrender.com/api/survivor/${survivor}/update-local/`,
                data
            )
            .then((res) => {
                if (res.statusCode === 200) {
                    return 'Ultimo local atualizado.'
                }
            })
            .catch((err) => console.log(err))

        document.querySelector('#message').innerText = message
    })
}

document.querySelector('#message').innerText = message

update()
