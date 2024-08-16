// Script para calcular automaticamente o valor total da escala de Glasgow
document.querySelectorAll('select').forEach(select => {
    select.addEventListener('change', () => {
        const ocular = parseInt(document.getElementById('eye_opening').value) || 0;
        const verbal = parseInt(document.getElementById('verbal_response').value) || 0;
        const motora = parseInt(document.getElementById('motor_response').value) || 0;
        document.getElementById('total').value = ocular + verbal + motora;
    });
});

function saveFormData() {
    const form = document.getElementById('form-anamnese-3');
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

    localStorage.setItem('formData3', JSON.stringify(formObject));
    console.log('Form data saved!', formObject);
}

document.addEventListener('DOMContentLoaded', () => {
    saveFormData();
});

