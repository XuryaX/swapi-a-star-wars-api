const datasetListElement = document.getElementById('dataset-list');
const datasetDetailsElement = document.getElementById('dataset-details');
const gridElement = document.getElementById('grid');
const buttonsContainer = document.getElementById('buttons');

let currentPage = 1;
let isLastPage = false;
let isLoading = false;
let datasetId = '';

fetchDatasets()

function fetchDatasets() {
  fetch('/api/data/list')
    .then(response => response.json())
    .then(datasets => {
      datasets.forEach(dataset => {
        const datasetCard = createDatasetCard(dataset);
        datasetListElement.appendChild(datasetCard);
      });
    })
    .catch(error => console.error(error));
}

function createDatasetCard(dataset) {
  const datasetCard = document.createElement('div');
  datasetCard.classList.add('dataset-card');
  datasetCard.innerText = `ID: ${dataset.id}\nNumber of Files: ${dataset.num_files}\nCreated At: ${dataset.created_at}`;
  datasetCard.addEventListener('click', () => showDatasetDetails(dataset.id));
  return datasetCard;
}

function createCellElement(text) {
  const cellElement = document.createElement('div');
  cellElement.classList.add('cell');
  cellElement.innerText = text;
  return cellElement;
}

function renderGrid(data, withCheckbox, scrolledLoad) {

  if(!scrolledLoad) {
    gridElement.innerHTML = '';
    const headerElement = createHeaderElement(Object.keys(data[0]), withCheckbox);
    gridElement.appendChild(headerElement);  
  }
  data.forEach(row => {
    const rowElement = createRowElement(row);
    gridElement.appendChild(rowElement);
  });
}

function createHeaderElement(keys, withCheckbox) {
  const headerElement = document.createElement('div');
  headerElement.classList.add('row');
  keys.forEach(key => {
    const cellElement = document.createElement('div');
    cellElement.classList.add('cell');

    if(withCheckbox){
      const checkboxElement = document.createElement('input');
      checkboxElement.type = 'checkbox';
      checkboxElement.classList.add('column-checkbox');
      checkboxElement.value = key;
      cellElement.appendChild(checkboxElement);
    }
  
    const labelElement = document.createElement('label');
    labelElement.for = key;
    labelElement.innerText = key;
    cellElement.appendChild(labelElement);
    headerElement.appendChild(cellElement);
  });
  return headerElement;
}

function getSelectedColumns() {
  const selectedColumns = [];
  const columnCheckboxes = document.querySelectorAll('.column-checkbox:checked');
  columnCheckboxes.forEach(checkbox => {
    selectedColumns.push(checkbox.value);
  });
  return selectedColumns;
}


function createRowElement(row) {
  const rowElement = document.createElement('div');
  rowElement.classList.add('row');
  Object.keys(row).forEach(key => {
    const cellElement = createCellElement(row[key]);
    rowElement.appendChild(cellElement);
  });
  return rowElement;
}

function createCellElement(text) {
  const cellElement = document.createElement('div');
  cellElement.classList.add('cell');
  cellElement.innerText = text;
  return cellElement;
}

function showDatasetDetails(datasetId) {
  currentPage = 1;
  isLastPage = false;
  isLoading = false;
  datasetListElement.innerHTML = ''
  gridElement.innerHTML = '';

  function handleScroll() {
    const lastRow = gridElement.querySelector('.row:last-child');
    if (lastRow) {
      const lastRowRect = lastRow.getBoundingClientRect();
      if (lastRowRect.bottom <= window.innerHeight && !isLoading && !isLastPage) {
        isLoading = true;
        currentPage += 1;
        fetchData(datasetId, currentPage, true);
      }
    }
  }

  function getValueCounts() {
    const selectedColumns = getSelectedColumns();
    if (selectedColumns.length > 0) {
      isLoading = true;
      fetch(`/api/explore/value_count/${datasetId}/${selectedColumns.join(',')}`)
        .then(response => response.json())
        .then(data => {
          renderGrid(data['data'], false, false);
          isLoading = false;
        })
        .catch(error => console.error(error));
    }
  }


  window.removeEventListener('scroll', handleScroll);
  fetchData(datasetId, currentPage);
  window.addEventListener('scroll', handleScroll);

  const valueCountButton = document.createElement('button');
  valueCountButton.setAttribute('id', 'valueCountButton');
  valueCountButton.innerText = 'Get value counts';
  valueCountButton.addEventListener('click', getValueCounts);

  buttonsContainer.appendChild(valueCountButton);

  function getSelectedColumns() {
    const selectedColumns = [];
    const columnCheckboxes = document.querySelectorAll('.column-checkbox:checked');
    columnCheckboxes.forEach(checkbox => {
      selectedColumns.push(checkbox.value);
    });
    return selectedColumns;
  }

  function createRowElementForValueCount(row) {
    const rowElement = document.createElement('div');
    rowElement.classList.add('row');
    const valueElement = createCellElement(row.value);
    const columnsElement = createCellElement(`${row.column1}: ${row[row.column1]}, ${row.column2}: ${row[row.column2]}`);
    rowElement.appendChild(valueElement);
    rowElement.appendChild(columnsElement);
    return rowElement;
  }
}

function fetchData(datasetId, page, scrolledPage) {
  isLoading = true;
  fetch(`/api/explore/${datasetId}/${page}`)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        renderGrid(data, true, scrolledPage);
        isLoading = false;
      } else {
        isLastPage = true;
      }
    })
    .catch(error => console.error(error));
}

function showOriginalGrid() {
  gridElement.innerHTML = '';
  const element = document.getElementById('valueCountButton');
  if (element !== null) {
    element.remove();
  }
  fetchDatasets();
}

function loadData() {
  fetch('/api/data/fetch_and_process/', {
    method: 'POST'
  })
  .then(data => {
    console.log(data);
    showOriginalGrid()
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}