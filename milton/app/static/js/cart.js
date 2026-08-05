// MILTON — მსუბუქი localStorage-ზე დაფუძნებული კალათა.
// გლობალურ window.miltonAddToCart(product, qty)-ს იძახებს product_detail.html.
(function () {
    'use strict';

    var CART_KEY = 'miltonCart';

    function getCart() {
        try {
            var raw = localStorage.getItem(CART_KEY);
            var parsed = raw ? JSON.parse(raw) : [];
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            return [];
        }
    }

    function saveCart(cart) {
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        renderCart();
    }

    function formatPrice(value) {
        var n = parseFloat(value) || 0;
        return n.toFixed(2) + ' ₾';
    }

    function cartTotal(cart) {
        return cart.reduce(function (sum, item) {
            return sum + (parseFloat(item.price) || 0) * item.qty;
        }, 0);
    }

    function renderCart() {
        var cart = getCart();
        var countEl = document.getElementById('miltonCartCount');
        var itemsEl = document.getElementById('miltonCartItems');
        var totalEl = document.getElementById('miltonCartTotalValue');

        var count = cart.reduce(function (sum, item) { return sum + item.qty; }, 0);
        if (countEl) {
            countEl.textContent = count;
            countEl.style.display = count > 0 ? 'inline-flex' : 'none';
        }

        if (!itemsEl) return;

        if (cart.length === 0) {
            itemsEl.innerHTML = '<p id="miltonCartEmpty">' + (window.MILTON_I18N ? window.MILTON_I18N.cart_empty : 'Cart is empty') + '</p>';
        } else {
            var html = '';
            cart.forEach(function (item) {
                html += '<div class="milton-cart-row">' +
                    '<div class="milton-cart-row-info">' +
                        '<span class="milton-cart-row-name">' + item.name + '</span>' +
                        '<span class="milton-cart-row-meta">' + item.qty + ' × ' + formatPrice(item.price) + '</span>' +
                    '</div>' +
                    '<button type="button" class="milton-cart-remove" data-id="' + item.id + '">✕</button>' +
                '</div>';
            });
            itemsEl.innerHTML = html;
        }

        if (totalEl) totalEl.textContent = formatPrice(cartTotal(cart));
    }

    function openCart() {
        document.body.classList.add('milton-cart-open');
    }

    function closeCart() {
        document.body.classList.remove('milton-cart-open');
    }

    // --- საჯარო API, გამოიყენება templates-ის inline სკრიპტებიდან ---
    window.miltonAddToCart = function (product, qty) {
        qty = qty || 1;
        var cart = getCart();
        var existing = cart.filter(function (item) { return item.id === product.id; })[0];
        if (existing) {
            existing.qty += qty;
        } else {
            cart.push({ id: product.id, name: product.name, price: product.price, qty: qty });
        }
        saveCart(cart);
        openCart();
    };

    window.miltonClearCart = function () {
        saveCart([]);
    };

    window.miltonGetCartSummary = function () {
        var cart = getCart();
        var lines = cart.map(function (item) {
            return '• ' + item.name + ' — ' + item.qty + ' × ' + formatPrice(item.price);
        });
        return {
            count: cart.reduce(function (sum, item) { return sum + item.qty; }, 0),
            total: cartTotal(cart),
            text: lines.join('\n')
        };
    };

    document.addEventListener('DOMContentLoaded', function () {
        renderCart();

        var toggle = document.getElementById('miltonCartToggle');
        if (toggle) toggle.addEventListener('click', openCart);

        var closeBtn = document.getElementById('miltonCartClose');
        if (closeBtn) closeBtn.addEventListener('click', closeCart);

        var continueBtn = document.getElementById('miltonCartContinue');
        if (continueBtn) continueBtn.addEventListener('click', closeCart);

        var overlay = document.getElementById('miltonCartOverlay');
        if (overlay) overlay.addEventListener('click', closeCart);

        var itemsEl = document.getElementById('miltonCartItems');
        if (itemsEl) {
            itemsEl.addEventListener('click', function (e) {
                var btn = e.target.closest ? e.target.closest('.milton-cart-remove') : null;
                if (!btn) return;
                var id = parseInt(btn.getAttribute('data-id'), 10);
                var cart = getCart().filter(function (item) { return item.id !== id; });
                saveCart(cart);
            });
        }
    });
})();
