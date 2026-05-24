// main.js — students will add JavaScript here as features are built

(function () {
    var overlay  = document.getElementById('demo-modal');
    var iframe   = document.getElementById('demo-iframe');
    var openBtn  = document.getElementById('open-demo-modal');
    var closeBtn = document.getElementById('demo-modal-close');

    if (!overlay || !iframe || !openBtn) return;

    function openModal() {
        iframe.src = iframe.getAttribute('data-src');
        overlay.classList.add('is-open');
        overlay.setAttribute('aria-hidden', 'false');
        closeBtn.focus();
    }

    function closeModal() {
        iframe.src = '';
        overlay.classList.remove('is-open');
        overlay.setAttribute('aria-hidden', 'true');
        openBtn.focus();
    }

    openBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
    });

    closeBtn.addEventListener('click', closeModal);

    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeModal();
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
            closeModal();
        }
    });
}());
