// Main JavaScript functionality for the dental clinic system

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Confirmation dialogs for delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Dynamic search functionality
    const searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function(input) {
        const targetSelector = input.getAttribute('data-search');
        const targets = document.querySelectorAll(targetSelector);
        
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            targets.forEach(function(target) {
                const text = target.textContent.toLowerCase();
                if (text.includes(query)) {
                    target.style.display = '';
                } else {
                    target.style.display = 'none';
                }
            });
        });
    });

    // Dashboard stats animation
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(function(stat) {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = finalValue / 30;
        
        const timer = setInterval(function() {
            currentValue += increment;
            if (currentValue >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(currentValue);
            }
        }, 50);
    });

    // Mobile menu toggle
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Date picker enhancement
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(function(input) {
        // Set minimum date to today for future appointments
        if (input.name === 'date' || input.name === 'expected_date') {
            const today = new Date().toISOString().split('T')[0];
            input.setAttribute('min', today);
        }
    });

    // Time slot validation
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const time = this.value;
            const hour = parseInt(time.split(':')[0]);
            
            // Clinic hours: 8 AM to 6 PM
            if (hour < 8 || hour >= 18) {
                alert('Please select a time between 8:00 AM and 6:00 PM');
                this.value = '';
            }
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Loading state for forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
                this.disabled = true;
            }
        });
    });

    // Table row click navigation
    const clickableRows = document.querySelectorAll('[data-href]');
    clickableRows.forEach(function(row) {
        row.style.cursor = 'pointer';
        row.addEventListener('click', function() {
            window.location.href = this.getAttribute('data-href');
        });
    });

    // Status badge styling
    const statusBadges = document.querySelectorAll('.status-badge');
    statusBadges.forEach(function(badge) {
        const status = badge.textContent.toLowerCase().trim();
        badge.classList.remove('bg-success', 'bg-warning', 'bg-danger', 'bg-secondary');
        
        switch(status) {
            case 'completed':
            case 'paid':
                badge.classList.add('bg-success');
                break;
            case 'scheduled':
            case 'pending':
                badge.classList.add('bg-warning');
                break;
            case 'cancelled':
            case 'overdue':
                badge.classList.add('bg-danger');
                break;
            default:
                badge.classList.add('bg-secondary');
        }
    });

    // Treatment step completion
    const stepCheckboxes = document.querySelectorAll('.step-checkbox');
    stepCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const stepRow = this.closest('tr');
            if (this.checked) {
                stepRow.classList.add('completed');
            } else {
                stepRow.classList.remove('completed');
            }
        });
    });
});

// Utility functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toast = createToast(message, type);
    toastContainer.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1055';
    document.body.appendChild(container);
    return container;
}

function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    const iconMap = {
        success: 'fas fa-check-circle text-success',
        error: 'fas fa-exclamation-circle text-danger',
        warning: 'fas fa-exclamation-triangle text-warning',
        info: 'fas fa-info-circle text-info'
    };
    
    const icon = iconMap[type] || iconMap.info;
    
    toast.innerHTML = `
        <div class="toast-header">
            <i class="${icon} me-2"></i>
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    return toast;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}
