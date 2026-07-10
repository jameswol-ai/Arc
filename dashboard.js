// ════════════════════════════════════════════════════════════════════════════════
// Dashboard JavaScript - Interactive Functionality
// ════════════════════════════════════════════════════════════════════════════════

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeCharts();
    initializeTasks();
    addInteractiveListeners();
});

// ════════════════  NAVIGATION  ════════════════
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Get section ID
            const sectionId = this.getAttribute('data-section');
            
            // Update section title
            const titleMap = {
                'overview': 'Overview',
                'analytics': 'Analytics',
                'tasks': 'Tasks',
                'settings': 'Settings'
            };
            document.getElementById('section-title').textContent = titleMap[sectionId];
            
            // Hide all sections
            const sections = document.querySelectorAll('.section');
            sections.forEach(section => section.classList.remove('active'));
            
            // Show selected section
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

// ════════════════  CHARTS  ════════════════
function initializeCharts() {
    // Sales Chart
    const salesCtx = document.getElementById('salesChart');
    if (salesCtx) {
        new Chart(salesCtx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6'],
                datasets: [{
                    label: 'Sales',
                    data: [12000, 19000, 15000, 25000, 22000, 30000],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    filler: {
                        propagate: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // Traffic Sources Chart
    const trafficCtx = document.getElementById('trafficChart');
    if (trafficCtx) {
        new Chart(trafficCtx, {
            type: 'doughnut',
            data: {
                labels: ['Direct', 'Organic', 'Social', 'Referral'],
                datasets: [{
                    data: [35, 25, 20, 20],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#4facfe'
                    ],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Growth Chart
    const growthCtx = document.getElementById('growthChart');
    if (growthCtx) {
        new Chart(growthCtx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Growth %',
                    data: [10, 15, 12, 25, 22, 30],
                    backgroundColor: '#667eea',
                    borderRadius: 8,
                    borderColor: '#667eea',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // User Distribution Chart
    const distributionCtx = document.getElementById('distributionChart');
    if (distributionCtx) {
        new Chart(distributionCtx, {
            type: 'radar',
            data: {
                labels: ['Desktop', 'Mobile', 'Tablet', 'Smart TV', 'Wearable'],
                datasets: [{
                    label: 'User Distribution',
                    data: [85, 75, 45, 20, 10],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
    }
}

// ════════════════  TASKS  ════════════════
function initializeTasks() {
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    
    taskCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskItem = this.closest('.task-item');
            if (this.checked) {
                taskItem.style.opacity = '0.6';
            } else {
                taskItem.style.opacity = '1';
            }
        });
    });
}

function addTask() {
    const input = document.getElementById('taskInput');
    const tasksList = document.getElementById('tasksList');
    
    if (input.value.trim() === '') {
        alert('Please enter a task');
        return;
    }
    
    const taskItem = document.createElement('div');
    taskItem.className = 'task-item';
    taskItem.innerHTML = `
        <input type="checkbox" class="task-checkbox">
        <span class="task-text">${escapeHtml(input.value)}</span>
        <button class="btn-delete" onclick="deleteTask(this)">✕</button>
    `;
    
    tasksList.appendChild(taskItem);
    
    // Add event listener to new checkbox
    const checkbox = taskItem.querySelector('.task-checkbox');
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            taskItem.style.opacity = '0.6';
        } else {
            taskItem.style.opacity = '1';
        }
    });
    
    input.value = '';
    input.focus();
}

function deleteTask(button) {
    const taskItem = button.closest('.task-item');
    taskItem.style.opacity = '0';
    setTimeout(() => {
        taskItem.remove();
    }, 300);
}

// ════════════════  INTERACTIVE LISTENERS  ════════════════
function addInteractiveListeners() {
    // Allow Enter key to add task
    const taskInput = document.getElementById('taskInput');
    if (taskInput) {
        taskInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addTask();
            }
        });
    }
    
    // Search functionality
    const searchBox = document.querySelector('.search-box');
    if (searchBox) {
        searchBox.addEventListener('input', function(e) {
            const query = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.activity-table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
}

// ════════════════  UTILITY FUNCTIONS  ════════════════
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Real-time metric updates (simulated)
function updateMetrics() {
    setInterval(() => {
        const stats = document.querySelectorAll('.stat-value');
        
        stats.forEach((stat, index) => {
            if (index === 0) { // Total Sales
                const currentValue = parseInt(stat.textContent.replace(/\D/g, ''));
                const newValue = currentValue + Math.floor(Math.random() * 500);
                stat.textContent = '$' + newValue.toLocaleString();
            }
        });
    }, 5000); // Update every 5 seconds
}

// Initialize real-time updates
updateMetrics();

// ════════════════  EXPORT FUNCTIONALITY  ════════════════
function exportData(format) {
    const rows = document.querySelectorAll('.activity-table tbody tr');
    let data = [];
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        data.push({
            activity: cells[0].textContent,
            user: cells[1].textContent,
            date: cells[2].textContent,
            status: cells[3].textContent
        });
    });
    
    if (format === 'json') {
        const json = JSON.stringify(data, null, 2);
        downloadFile(json, 'dashboard-data.json', 'application/json');
    } else if (format === 'csv') {
        const csv = convertToCSV(data);
        downloadFile(csv, 'dashboard-data.csv', 'text/csv');
    }
}

function convertToCSV(data) {
    const headers = Object.keys(data[0]);
    const csv = [headers.join(',')];
    
    data.forEach(row => {
        const values = headers.map(header => `"${row[header]}"`);
        csv.push(values.join(','));
    });
    
    return csv.join('\n');
}

function downloadFile(content, filename, type) {
    const element = document.createElement('a');
    element.setAttribute('href', `data:${type};charset=utf-8,${encodeURIComponent(content)}`);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ════════════════  THEME TOGGLE (Optional)  ════════════════
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Load theme preference
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-theme');
}

// ════════════════  RESPONSIVE SIDEBAR TOGGLE  ════════════════
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}

// ════════════════  KEYBOARD SHORTCUTS  ════════════════
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search focus
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.querySelector('.search-box').focus();
    }
    
    // Ctrl/Cmd + D for Dark mode toggle
    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        toggleTheme();
    }
});

// ════════════════  NOTIFICATIONS  ════════════════
class NotificationManager {
    static show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background-color: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#667eea'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
}

// Add animations to document
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Example usage: NotificationManager.show('Changes saved!', 'success');
