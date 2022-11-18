let storageTemperatureUnitSelect = $('#temperature-select');
let storageTemperatureField = $('#storage-temperature');
let minStorageTemperatureC = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, '℃') * 10) / 10).toString().replace('.', ',');
let maxStorageTemperatureC = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, '℃') * 10) / 10).toString().replace('.', ',');
let minStorageTemperatureF = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, '℉') * 10) / 10).toString().replace('.', ',');
let maxStorageTemperatureF = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, '℉') * 10) / 10).toString().replace('.', ',');
let minStorageTemperatureK = (Math.round(temperature(minStorageTemperature, storageTemperatureUnit, 'K') * 10) / 10).toString().replace('.', ',');
let maxStorageTemperatureK = (Math.round(temperature(maxStorageTemperature, storageTemperatureUnit, 'K') * 10) / 10).toString().replace('.', ',');
storageTemperatureUnitSelect.on('change', changeTemperature);

function changeTemperature() {
    if (storageTemperatureUnit) {
        let temperatureUnit = storageTemperatureUnitSelect.val();
        switch (temperatureUnit) {
            case '℃': {
                minStorageTemperature = minStorageTemperatureC;
                maxStorageTemperature = maxStorageTemperatureC;
                break
            }
            case '℉': {
                minStorageTemperature = minStorageTemperatureF;
                maxStorageTemperature = maxStorageTemperatureF;
                break
            }
            case 'K': {
                minStorageTemperature = minStorageTemperatureK;
                maxStorageTemperature = maxStorageTemperatureK;
                break
            }
        }


        if (typeof minStorageTemperature === 'string' && typeof maxStorageTemperature === 'string' )
            storageTemperatureField.html(`от ${minStorageTemperature} до ${maxStorageTemperature}`);
        else if (typeof minStorageTemperature === 'string')
            storageTemperatureField.html(`${minStorageTemperature}`);
        else if (typeof maxStorageTemperature === 'string')
            storageTemperatureField.html(`${maxStorageTemperature}`);
        else
            storageTemperatureField.html('—')
    }
}

function temperature(value, old_unit, new_unit) {
    if (typeof value !== 'number')
        value = parseFloat(value);
    switch (old_unit) {
        case '℃': {
            switch (new_unit) {
                case '℃':
                    return value;
                case '℉':
                    return 9 / 5 * value + 32;
                case 'K':
                    return value + 273.15
            }
            break
        }

        case '℉': {
            switch (new_unit) {
                case '℃':
                    return 5 / 9 * (value - 32);
                case '℉':
                    return value;
                case 'K':
                    return (value + 459.67) * 5 / 9
            }
            break
        }

        case 'K': {
            switch (new_unit) {
                case '℃':
                    return value - 273.15;
                case '℉':
                    return 9 / 5 * value - 459.67;
                case 'K':
                    return value
            }
            break
        }
    }
}