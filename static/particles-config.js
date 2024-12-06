// Load the tsParticles configuration
tsParticles.load("tsparticles", {
    particles: {
        number: {
            value: 10, // Adjust the number of particles
            density: { enable: true, value_area: 400 },
        },
        color: {
            value: ["#ffffff", "#e2b5fe" + "#b5d6fe", "#ffd2e9"], // Soft glowing colors
        },
        shape: {
            type: "star",
        },
        opacity: {
            value: 0.25, // Lower opacity for a diluted effect
            random: true, // Randomize opacity
        },
        size: {
            value: 9, // Larger particles for a glow
            random: true, // Randomize size
            anim: { enable: true, speed: 1, size_min: 3, sync: false }, // Subtle animation
        },
        move: {
            enable: true,
            speed: 1, // Slow and gentle movement
            direction: "none",
            random: false,
            straight: false,
            out_mode: "out",
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: "#ffffff", // Soft white for lines
            opacity: 0.1, // Low opacity for subtle connections
            width: 1,
        },
    },
    interactivity: {
        detect_on: "canvas",
        events: {
            onhover: { enable: true, mode: "repulse" },
            onclick: { enable: true, mode: "push" },
            resize: true,
        },
        modes: {
            repulse: { distance: 100, duration: 0.4 },
            push: { particles_nb: 4 },
        },
    },
    retina_detect: true,
});
