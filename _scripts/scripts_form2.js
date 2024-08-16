let rowCount = 1;

function addRow() {
    if (rowCount < 48) {
        rowCount++;
        const table = document.getElementById('editableTable').getElementsByTagName('tbody')[0];
        const newRow = table.insertRow();

        const cell1 = newRow.insertCell(0);
        const cell2 = newRow.insertCell(1);
        const cell3 = newRow.insertCell(2);

        cell1.innerHTML = `<input type="datetime-local" id="datetime_local_${rowCount}" name="datetime_local[]" value="">`;
        cell2.innerHTML = `<input type="text" id="occurrence_${rowCount}" name="occurrence[]" value="Ocorrência ${rowCount}">`;
        cell3.innerHTML = `<button onclick="removeRow(this)">Remover</button>`;

        updateRowIds();
    }
}

function removeRow(button) {
    const row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
    rowCount--;
    updateRowIds();
}

function updateRowIds() {
    const rows = document.getElementById('editableTable').getElementsByTagName('tbody')[0].rows;
    document.getElementById('rowCountInput').value = rowCount;
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        cells[0].getElementsByTagName('input')[0].id = `datetime_local_${i + 1}`;
        cells[0].getElementsByTagName('input')[0].name = `datetime_local[]`;
        cells[1].getElementsByTagName('input')[0].id = `occurrence_${i + 1}`;
        cells[1].getElementsByTagName('input')[0].name = `occurrence[]`;
    }
}

function updateTableRows() {
    const desiredRowCount = parseInt(document.getElementById('rowCountInput').value);
    const table = document.getElementById('editableTable').getElementsByTagName('tbody')[0];

    while (rowCount < desiredRowCount) {
        addRow();
    }

    while (rowCount > desiredRowCount) {
        table.deleteRow(-1);
        rowCount--;
    }

    updateRowIds();
}
