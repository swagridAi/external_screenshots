/**
 * Screenshot to Table Frontend Script
 */

// Global variables
let cropper;
let tableData = null;

// DOM Elements
const captureBtn = document.getElementById('capture-btn');
const cropBtn = document.getElementById('crop-btn');
const extractTableBtn = document.getElementById('extract-table-btn');
const resetBtn = document.getElementById('reset-btn');
const imageContainer = document.getElementById('image-container');
const resultContainer = document.getElementById('result-container');
const loadingContainer = document.getElementById('loading-container');
const tableContainer = document.getElementById('table-container');
const statusContainer = document.getElementById('status-container');
const preview = document.getElementById('preview');
const croppedResult = document.getElementById('cropped-result');
const downloadCsvBtn = document.getElementById('download-csv-btn');
const downloadJsonBtn = document.getElementById('download-json-btn');

/**
 * Tab functionality
 */
function openTab(evt, tabName) {
  // Hide all tab content
  const tabcontent = document.getElementsByClassName("tabcontent");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].classList.remove("active");
  }
  
  // Remove active class from tab buttons
  const tablinks = document.getElementsByClassName("tablinks");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove("active");
  }
  
  // Show the selected tab and mark button as active
  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");
}

/**
 * Display status message
 */
function showStatus(message, type) {
  statusContainer.textContent = message;
  statusContainer.className = 'status-message ' + type;
  statusContainer.classList.remove('hidden');
  
  // Auto hide success and info messages after 5 seconds
  if (type === 'success' || type === 'info') {
    setTimeout(() => {
      statusContainer.classList.add('hidden');
    }, 5000);
  }
}

/**
 * Escape HTML for safe insertion
 */
function escapeHtml(unsafe) {
  if (unsafe === null || unsafe === undefined) {
    return '';
  }
  
  return String(unsafe)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Convert table data to HTML table
 */
function renderTable(data) {
  const tableOutput = document.getElementById('table-output');
  
  if (!data || !data.columns || !data.rows || data.rows.length === 0) {
    tableOutput.innerHTML = '<p>No valid table data found</p>';
    return;
  }
  
  let html = '<table>';
  
  // Header row
  html += '<thead><tr>';
  data.columns.forEach(column => {
    html += `<th>${escapeHtml(column)}</th>`;
  });
  html += '</tr></thead>';
  
  // Data rows
  html += '<tbody>';
  data.rows.forEach(row => {
    html += '<tr>';
    data.columns.forEach(column => {
      html += `<td>${escapeHtml(row[column] || '')}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody></table>';
  
  tableOutput.innerHTML = html;
}

/**
 * Convert table data to CSV
 */
function convertToCSV(data) {
  if (!data || !data.columns || !data.rows || data.rows.length === 0) {
    return '';
  }
  
  // Header row
  let csv = data.columns.join(',') + '\n';
  
  // Data rows
  data.rows.forEach(row => {
    const csvRow = data.columns.map(column => {
      const value = row[column] || '';
      // Escape quotes and wrap in quotes if contains comma or newline
      if (typeof value === 'string' && (value.includes(',') || value.includes('\n') || value.includes('"'))) {
        return '"' + value.replace(/"/g, '""') + '"';
      }
      return value;
    });
    csv += csvRow.join(',') + '\n';
  });
  
  return csv;
}

/**
 * Handle screenshot capture
 */
function captureScreenshot() {
  captureBtn.disabled = true;
  captureBtn.textContent = 'Capturing...';
  
  fetch('/request-screenshot')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Failed to capture screenshot: ${response.status}`);
      }
      return response.blob();
    })
    .then(blob => {
      preview.src = URL.createObjectURL(blob);
      imageContainer.classList.remove('hidden');
      cropBtn.classList.remove('hidden');
      resetBtn.classList.remove('hidden');
      captureBtn.textContent = 'Capture New Screenshot';
      captureBtn.disabled = false;
      
      // Initialize cropper after image loads
      preview.onload = function() {
        if (cropper) {
          cropper.destroy();
        }
        cropper = new Cropper(preview, {
          viewMode: 1,
          dragMode: 'crop',
          autoCrop: true,
          responsive: true,
          restore: false,
          guides: true,
          center: true,
          highlight: false,
          cropBoxMovable: true,
          cropBoxResizable: true,
          toggleDragModeOnDblclick: false
        });
        imageContainer.classList.add('cropping');
      };
    })
    .catch(error => {
      console.error('Error:', error);
      captureBtn.textContent = 'Capture Screenshot (Space)';
      captureBtn.disabled = false;
      showStatus(error.message, 'error');
    });
}

/**
 * Handle crop selection
 */
function cropSelection() {
  if (!cropper) return;
  
  const canvas = cropper.getCroppedCanvas({
    maxWidth: 4096,
    maxHeight: 4096
  });
  
  if (canvas) {
    croppedResult.src = canvas.toDataURL('image/png');
    resultContainer.classList.remove('hidden');
    extractTableBtn.classList.remove('hidden');
    
    // Send cropped data to server
    fetch('/save-cropped', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        image: canvas.toDataURL('image/png')
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        showStatus('Image cropped and saved successfully!', 'success');
      } else {
        showStatus('Error saving cropped image: ' + data.error, 'error');
      }
    })
    .catch(error => {
      showStatus('Error processing cropped image: ' + error.message, 'error');
    });
  }
}

/**
 * Handle table extraction
 */
function extractTable() {
  if (!croppedResult.src) {
    showStatus('No cropped image available', 'error');
    return;
  }
  
  // Show loading indicator
  loadingContainer.classList.remove('hidden');
  extractTableBtn.disabled = true;
  tableContainer.classList.add('hidden');
  
  // Send the cropped image for table extraction
  fetch('/extract-table', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      image: croppedResult.src
    })
  })
  .then(response => response.json())
  .then(data => {
    loadingContainer.classList.add('hidden');
    extractTableBtn.disabled = false;
    
    if (data.success) {
      tableData = data.table_data;
      
      // Render HTML table
      renderTable(tableData);
      
      // Render JSON view
      document.getElementById('json-output').textContent = JSON.stringify(tableData, null, 2);
      
      // Render CSV view
      document.getElementById('csv-output').textContent = convertToCSV(tableData);
      
      // Show table container
      tableContainer.classList.remove('hidden');
      showStatus('Table extracted successfully!', 'success');
    } else {
      showStatus('Failed to extract table: ' + data.error, 'error');
    }
  })
  .catch(error => {
    loadingContainer.classList.add('hidden');
    extractTableBtn.disabled = false;
    showStatus('Error during table extraction: ' + error.message, 'error');
  });
}

/**
 * Reset the application state
 */
function resetApplication() {
  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
  
  imageContainer.classList.remove('cropping');
  imageContainer.classList.add('hidden');
  resultContainer.classList.add('hidden');
  cropBtn.classList.add('hidden');
  extractTableBtn.classList.add('hidden');
  resetBtn.classList.add('hidden');
  tableContainer.classList.add('hidden');
  statusContainer.classList.add('hidden');
  
  preview.src = '';
  croppedResult.src = '';
  tableData = null;
  
  document.getElementById('table-output').innerHTML = '';
  document.getElementById('json-output').textContent = '';
  document.getElementById('csv-output').textContent = '';
}

/**
 * Download table data as JSON
 */
function downloadJson() {
  if (!tableData) return;
  
  const json = JSON.stringify(tableData, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = 'table_data_' + new Date().getTime() + '.json';
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
}

/**
 * Download table data as CSV
 */
function downloadCsv() {
  if (!tableData) return;
  
  const csv = convertToCSV(tableData);
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = 'table_data_' + new Date().getTime() + '.csv';
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
}

/**
 * Initialize event listeners
 */
function initEventListeners() {
  // Capture screenshot
  captureBtn.addEventListener('click', captureScreenshot);
  
  // Crop selection
  cropBtn.addEventListener('click', cropSelection);
  
  // Extract table
  extractTableBtn.addEventListener('click', extractTable);
  
  // Reset application
  resetBtn.addEventListener('click', resetApplication);
  
  // Download buttons
  downloadJsonBtn.addEventListener('click', downloadJson);
  downloadCsvBtn.addEventListener('click', downloadCsv);
  
  // Use spacebar as shortcut for screenshot capture
  document.addEventListener('keydown', function(event) {
    if (event.code === 'Space' && !imageContainer.classList.contains('cropping') && !captureBtn.disabled) {
      event.preventDefault();
      captureBtn.click();
    }
  });
}

/**
 * Initialize application
 */
function init() {
  console.log('Initializing Screenshot to Table application...');
  initEventListeners();
  showStatus('Press space or click "Capture Screenshot" to begin', 'info');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);