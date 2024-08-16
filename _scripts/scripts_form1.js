function calcularIdade() {
    const dataNascimentoInput = document.getElementById('birth_date');
    const idadeInput = document.getElementById('age');
    const dataNascimento = new Date(dataNascimentoInput.value);
    const hoje = new Date();
    let idade = hoje.getFullYear() - dataNascimento.getFullYear();
    const mes = hoje.getMonth() - dataNascimento.getMonth();

    if (mes < 0 || (mes === 0 && hoje.getDate() < dataNascimento.getDate())) {
        idade--;
    }

    idadeInput.value = idade;
}

function saveFormData() {
    const form = document.getElementById('form-anamnese-1');
    if (!form) {
        console.error('Form not found');
        return;
    }

    const formData = new FormData(form);
    const formObject = {};

    // Captura dados de text inputs, textareas, selects, etc.
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    // Captura dados de checkboxes e radio buttons
    const inputs = form.querySelectorAll('input[type="checkbox"], input[type="radio"]');
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            formObject[input.name] = input.checked;
        } else if (input.type === 'radio') {
            if (input.checked) {
                formObject[input.name] = input.value;
            }
        }
    });

    localStorage.setItem('formData1', JSON.stringify(formObject));
    console.log('Form data saved!', formObject);
}

document.addEventListener('DOMContentLoaded', () => {
    saveFormData();
});
