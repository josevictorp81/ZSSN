async function inventory() {
    const survivors = await axios
        .get('https://zssnapi.onrender.com/api/survivors/')
        .then((res) => res.data)
        .catch((err) => err)

    var survivorIventory = document.querySelector('#survivor-inventory')
    survivors.forEach((element) => {
        var opt = document.createElement('option')
        opt.value = element.id
        opt.text = element.name
        survivorIventory.appendChild(opt)
    })

    const submit = document.querySelector('#submit')

    submit.addEventListener('click', async () => {
        const survivorRelator = document.querySelector(
            '#survivor-inventory'
        ).value

        const invent = await axios
            .get(
                `https://zssnapi.onrender.com/api/resources/${survivorRelator}/survivor/`
            )
            .then((res) => res.data)
            .catch((err) => console.log(err))

        console.log(invent)
        document.querySelector('#negociator-water').value = invent[0].quantity
        document.querySelector('#negociator-food').value = invent[1].quantity
        document.querySelector('#negociator-medication').value =
            invent[2].quantity
        document.querySelector('#negociator-ammunition').value =
            invent[3].quantity
    })
}

inventory()
