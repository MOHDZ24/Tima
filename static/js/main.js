// رواق المسلم - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {

    // Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.querySelector('.nav-menu');
    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            navMenu.classList.toggle('show');
            this.classList.toggle('active');
        });
    }

    // Alert close buttons
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });

    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Wishlist button toggle
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            this.classList.toggle('active');
            const icon = this.querySelector('i');
            if (this.classList.contains('active')) {
                icon.style.color = '#dc3545';
            } else {
                icon.style.color = '#ccc';
            }
        });
    });

    // Search form with category
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        const categorySelect = searchForm.querySelector('.category-select');
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                if (this.value) {
                    window.location.href = '/category/' + this.value + '/';
                }
            });
        }
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Payment options styling
    document.querySelectorAll('.payment-option input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('.payment-option').forEach(opt => {
                opt.classList.remove('selected');
            });
            this.closest('.payment-option').classList.add('selected');
        });
    });

    // Image lazy loading fallback
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/placeholder.png';
        });
    });

    console.log('🕌 رواق المسلم - تم تحميل الموقع بنجاح');
});
