document.addEventListener('DOMContentLoaded', () => {
    const content = document.querySelector('.container');
    content.style.opacity = '0';
    content.style.transform = 'translateY(20px)';
    content.style.transition = 'all 0.5s ease';

    setTimeout(() => {
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
    }, 100);
});