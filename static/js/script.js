const nav = document.getElementById('menu')
const btn = document.getElementById('menu-btn')

btn.addEventListener('click', () => {
    btn.classList.toggle('open')
    nav.classList.toggle('navbar-md')
    nav.classList.toggle('navbar')
})