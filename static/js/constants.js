function temperature(value, old_unit, new_unit) {
    if (typeof value !== 'number')
        value = parseFloat(value)
    switch (old_unit) {
        case '℃': {
            switch (new_unit) {
                case '℃': return value
                case '℉': return 9/5 * value + 32
                case 'K': return value + 273.15
            }
            break
        }

        case '℉': {
            switch (new_unit) {
                case '℃': return 5/9 * (value - 32)
                case '℉': return value
                case 'K': return (value + 459.67) * 5/9
            }
            break
        }

        case 'K': {
            switch (new_unit) {
                case '℃': return value - 273.15
                case '℉': return 9/5 * value - 459.67
                case 'K': return value
            }
            break
        }
    }
}

function energy(value, old_unit, new_unit) {
    if (typeof value !== 'number')
        value = parseFloat(value)
    switch (old_unit) {
        case 'ккал': {
            switch (new_unit) {
                case 'ккал': return value
                case 'кДж': return 4.1868 * value
            }
            break
        }

        case 'кДж': {
            switch (new_unit) {
                case 'ккал': return 0.239006 * value
                case 'кДж': return value
            }
            break
        }
    }
}