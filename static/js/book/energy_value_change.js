let energyValueUnitSelect = $('#energy-value-select');
let energyValueField = $('#energy-value');
let energyValueKkal = (Math.round(energy(energyValue, energyValueUnit, 'ккал') * 10) / 10).toString().replace('.', ',');
let energyValueKDz = (Math.round(energy(energyValue, energyValueUnit, 'кДж') * 10) / 10).toString().replace('.', ',');
energyValueUnitSelect.on('change', changeEnergy);

function changeEnergy() {
    if (energyValueUnit) {
        let energyUnit = energyValueUnitSelect.val();
        switch (energyUnit) {
            case 'ккал': {
                energyValueField.html(energyValueKkal);
                break
            }
            case 'кДж': {
                energyValueField.html(energyValueKDz);
                break
            }
        }
    }
}

function energy(value, old_unit, new_unit) {
    if (typeof value !== 'number')
        value = parseFloat(value);
    switch (old_unit) {
        case 'ккал': {
            switch (new_unit) {
                case 'ккал':
                    return value;
                case 'кДж':
                    return 4.1868 * value
            }
            break
        }

        case 'кДж': {
            switch (new_unit) {
                case 'ккал':
                    return 0.239006 * value;
                case 'кДж':
                    return value
            }
            break
        }
    }
}