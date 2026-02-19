gsap.registerPlugin(ScrollTrigger);

const toggle = document.querySelector(".theme-toggle");

if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}

toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    localStorage.setItem(
        "theme",
        document.body.classList.contains("dark") ? "dark" : "light"
    );
});


// ================= LOADER =================
function loader() {
    const cursor = document.querySelector(".cursor");
    const offsetX = 20;
    const offsetY = 20;


    // Cursor follow
    window.addEventListener("mousemove", (e) => {
        gsap.to(cursor, {
            left: e.clientX + offsetX,
            top: e.clientY + offsetY,
            duration: 0.15,
        });
    });


    // Timeline for loader
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.to(".loader-text span", {
        opacity: 1,
        y: 0,
        stagger: 0.08,
        duration: 0.8
    })
        .to(".loader-line", {
            width: "100%",
            duration: 1.5
        }, "-=0.2")
        .to(".loader", {
            y: "-100%",
            duration: 1.2,
            ease: "power4.inOut"
        })
        .add(() => {
            // Unlock page
            document.body.classList.remove("loading");
            gsap.to(cursor, { opacity: 1, duration: 0.5 });

            // Start nav and hero animation after loader
            navAnimation();
            heroAnimation();
        });

    // Loader subtext animation
    gsap.from(".loader-subtext", {
        opacity: 0,
        y: 10,
        duration: 0.8,
        delay: 0.8
    });
}

loader();

// ================= NAVBAR ANIMATION =================
function navAnimation() {
    const navTL = gsap.timeline({
        defaults: { ease: "power3.out" }
    });
    gsap.set("nav", {
        opacity: 1,
        visibility: "visible"
    });

    navTL.from("nav", {
        y: -80,
        opacity: 0,
        duration: 1
    })
        .from(".logo", {
            scale: 0.5,
            opacity: 0,
            duration: 0.6
        }, "-=0.4")
        .from(".menu li", {
            y: 20,
            opacity: 0,
            stagger: 0.15,
            duration: 0.5
        }, "-=0.3")
        .from(".buttons button", {
            y: 20,
            opacity: 0,
            stagger: 0.2,
            duration: 0.5
        }, "-=0.4")
        .from(".menuicon", {
            rotate: 90,
            scale: 0,
            opacity: 0,
            duration: 0.4
        }, "-=0.3");
}

// ================= HERO ANIMATION =================
function heroAnimation() {
    const heroTL = gsap.timeline({ defaults: { ease: "power3.out" } });

    heroTL
        .fromTo(".herologo", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.8 })
        .fromTo(".hero-title", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7 }, "-=0.4")
        .fromTo(".tagline", { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5 })
        .fromTo(".status", { opacity: 0 }, { opacity: 1, duration: 0.4 })
        .fromTo(".scroll-down", { y: -10, opacity: 0 }, { y: 0, opacity: 0.6, duration: 0.6 });
}

// ================= MENU BUTTON =================

function Menubtn() {
    const openMenu = document.getElementById("openMenu");
    const closeMenu = document.getElementById("closeMenu");
    const aside = document.getElementById("asideMenu");

    openMenu.onclick = () => {
        gsap.killTweensOf(openMenu);

        gsap.to(openMenu, {
            rotate: 90,
            duration: 0.3,
            ease: "power2.out"
        });

        aside.classList.add("show");
        openMenu.style.display = "none";
    };

    closeMenu.onclick = () => {
        // reset icon safely
        gsap.killTweensOf(openMenu);

        gsap.set(openMenu, { rotate: 0 });

        aside.classList.remove("show");
        openMenu.style.display = "block";
    };
}

Menubtn();


// ================= HEADER SCROLL =================
function scrollHeader() {
    window.addEventListener("scroll", () => {
        const header = document.querySelector("header");
        if (window.scrollY > 0) {
            header.classList.add("scrolled");
        } else {
            header.classList.remove("scrolled");
        }
    });
}

scrollHeader();

// ================= HOVER EFFECTS =================
document.querySelectorAll(".menu li a").forEach(link => {
    link.addEventListener("mouseenter", () => gsap.to(link, { y: -3, duration: 0.2 }));
    link.addEventListener("mouseleave", () => gsap.to(link, { y: 0, duration: 0.2 }));
});

document.querySelectorAll(".buttons button").forEach(btn => {
    btn.addEventListener("mouseenter", () => gsap.to(btn, { scale: 1.08, duration: 0.25 }));
    btn.addEventListener("mouseleave", () => gsap.to(btn, { scale: 1, duration: 0.25 }));
});

// ================= MOBILE MENU ICON =================
const menuIcon = document.getElementById("openMenu");
if (menuIcon) {
    menuIcon.addEventListener("click", () => {
        gsap.to(menuIcon, { rotate: 90, duration: 0.3, yoyo: true, repeat: 1 });
    });
}


// ========== Contact section   ===================
gsap.from(".contact-left h2, .contact-left p", {
    y: 30,
    opacity: 0,
    duration: 0.8,
    stagger: 0.2,
    scrollTrigger: {
        trigger: ".contact-section",
        start: "top 80%"
    }
});

gsap.from(".contact-info div", {
    x: -30,
    opacity: 0,
    stagger: 0.15,
    scrollTrigger: {
        trigger: ".contact-info",
        start: "top 85%"
    }
});

gsap.from(".contact-right form", {
    y: 40,
    opacity: 0,
    duration: 0.9,
    scrollTrigger: {
        trigger: ".contact-right",
        start: "top 85%"
    }
});





// Footer Section 

gsap.from(".footer-inner > div", {
    y: 40,
    opacity: 0,
    stagger: 0.2,
    duration: 0.8,
    ease: "power3.out",
    scrollTrigger: {
        trigger: ".footer",
        start: "top 85%"
    }
});

gsap.from(".footer-bottom", {
    opacity: 0,
    duration: 0.6,
    delay: 0.4,
    scrollTrigger: {
        trigger: ".footer",
        start: "top 90%"
    }
});



// Form Section


const form = document.getElementById("contactForm");
const formMessage = document.getElementById("formMessage");
const submitBtn = document.getElementById("submitBtn");

let isSubmitting = false;

function showMessage(message, type = "error") {
    formMessage.innerText = message;
    formMessage.classList.add("show");
    formMessage.style.color = type === "success" ? "green" : "red";

    setTimeout(() => {
        formMessage.classList.remove("show");
        formMessage.innerText = "";
    }, 5000);
}

if (form) {
    const url = form.dataset.url;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        if (isSubmitting) return; // 🔥 Prevent multiple clicks

        isSubmitting = true;
        submitBtn.disabled = true;
        submitBtn.innerText = "Sending...";

        const formData = new FormData(form);

        fetch(url, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    showMessage("Message sent successfully!", "success");
                    form.reset();
                } else {
                    showMessage(data.errors.join(", "), "error");
                }
            })
            .catch(() => {
                showMessage("Something went wrong!", "error");
            })
            .finally(() => {
                isSubmitting = false;
                submitBtn.disabled = false;
                submitBtn.innerText = "Send Message";
            });
    });
}
