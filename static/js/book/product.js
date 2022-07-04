let storageTemperatureUnitSelect = $('#temperature-select')
let storageTemperatureField = $('#storage-temperature')
let minStorageTemperatureC = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, '℃') * 10) / 10).toString().replace('.', ',')
let maxStorageTemperatureC = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, '℃') * 10) / 10).toString().replace('.', ',')
let minStorageTemperatureF = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, '℉') * 10) / 10).toString().replace('.', ',')
let maxStorageTemperatureF = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, '℉') * 10) / 10).toString().replace('.', ',')
let minStorageTemperatureK = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, 'K') * 10) / 10).toString().replace('.', ',')
let maxStorageTemperatureK = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, 'K') * 10) / 10).toString().replace('.', ',')
storageTemperatureUnitSelect.on('change', changeTemperature)

let energyValueUnitSelect = $('#energy-value-select')
let energyValueField = $('#energy-value')
let energyValueKkal = (Math.round(energy(energyValue, energyValueUnit, 'ккал') * 10) / 10).toString().replace('.', ',')
let energyValueKDz = (Math.round(energy(energyValue, energyValueUnit, 'кДж') * 10) / 10).toString().replace('.', ',')
energyValueUnitSelect.on('change', changeEnergy)

function changeEnergy() {
    if (energyValueUnit) {
        let energyUnit = energyValueUnitSelect.val()
        console.log(energyUnit)
        switch (energyUnit) {
            case 'ккал': {
                energyValueField.html(energyValueKkal)
                break
            }
            case 'кДж': {
                energyValueField.html(energyValueKDz)
                break
            }
        }
    }
}

function changeTemperature() {
    if (storageTemperatureUnit) {
        let temperatureUnit = storageTemperatureUnitSelect.val()
        switch (temperatureUnit) {
            case '℃': {
                minStorageTemperature = minStorageTemperatureC
                maxStorageTemperature = maxStorageTemperatureC
                break
            }
            case '℉': {
                minStorageTemperature = minStorageTemperatureF
                maxStorageTemperature = maxStorageTemperatureF
                break
            }
            case 'K': {
                minStorageTemperature = minStorageTemperatureK
                maxStorageTemperature = maxStorageTemperatureK
                break
            }
        }


        if (typeof minStorageTemperature === 'string' && typeof maxStorageTemperature === 'string' )
            storageTemperatureField.html(`от ${minStorageTemperature} до ${maxStorageTemperature}`)
        else if (typeof minStorageTemperature === 'string')
            storageTemperatureField.html(`${minStorageTemperature}`)
        else if (typeof maxStorageTemperature === 'string')
            storageTemperatureField.html(`${maxStorageTemperature}`)
        else
            storageTemperatureField.html('—')
    }
}
