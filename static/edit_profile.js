const Form = document.querySelector('#form')
const error = document.querySelector('#alert')

if (Form) {
    Form.addEventListener('submit', (event) => {

        let message = []
        let Contact = Form.elements.contact.value;

        let contactIsNumber = true

        for (i = 0; i < Contact.length; i++) {
            let num = parseInt(Contact[i])

            if (!(num >= 0 && num <= 9)) {
                contactIsNumber = false
                break;
            }
            console.log(num);
        }

        let Age = Form.elements.age.value;

        if (!((contactIsNumber && Contact.length === 10) || (Contact.length===0))) {
            message.push('Invalid Contact')
        }

        else if (parseInt(Age) <= 0 || parseInt(Age) >= 100) {
            message.push('Invalid Age')
        }
        if (message.length > 0) {
            event.preventDefault()
            error.classList.add('Alert')
            error.innerText = message.join(', ')
        }
        else {
            error.classList.remove('Alert')
            error.innerText = ''
        }
    })
}
