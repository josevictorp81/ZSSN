function listTable(lista) {
    console.log(lista)
    let tbody = document.querySelector('#tbody')

    for (let i = 0; i < lista.length; i++) {
        let tr = tbody.insertRow()

        let td_name = tr.insertCell()
        let td_age = tr.insertCell()
        let td_sex = tr.insertCell()
        let td_local = tr.insertCell()
        let td_infected = tr.insertCell()

        td_name.innerText = lista[i].name
        td_age.innerText = lista[i].age
        td_sex.innerText = lista[i].sex
        td_local.innerText = lista[i].local
        // console.log(lista[i].infected)
        // if (lista[i].infected === true) {
        //     td_infected.innerText = 'Infectado'
        // } else {
        //     td_infected.innerText = 'Não Infectado'
        // }
    }
}
async function getSurvivors() {
    const survivors = axios
        .get('https://zssnapi.onrender.com/api/survivors/')
        .then((res) => listTable(res.data))
        .catch((err) => {
            console.log(err)
        })
}

getSurvivors()
