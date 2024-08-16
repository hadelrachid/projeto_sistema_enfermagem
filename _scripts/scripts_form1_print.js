function loadFormData() {
    const formObject = JSON.parse(localStorage.getItem('formData1'));
    console.log('Loaded formObject from localStorage:', formObject);
    if (formObject) {
        for (const [key, value] of Object.entries(formObject)) {
            const elements = document.querySelectorAll(`[name=${key}]`);
            console.log(`Updating elements with name ${key} to value ${value}`);

            elements.forEach(element => {
                if (element.type === 'checkbox') {
                    element.checked = value === 'true' || value === true;
                } else if (element.type === 'radio') {
                    element.checked = element.value === value;
                } else if (element.tagName === 'SELECT') {
                    const option = element.querySelector(`option[value="${value}"]`);
                    if (option) {
                        option.selected = true;
                    }
                } else {
                    element.value = value;
                }
            });
        }
    } else {
        console.warn('No form data found in localStorage');
    }
}

document.addEventListener('DOMContentLoaded', loadFormData);
